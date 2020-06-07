# pylint: disable=wildcard-import, unused-wildcard-import, redefined-outer-name, missing-function-docstring
from http import HTTPStatus
from unittest.mock import MagicMock, patch

import pytest
from flask import Flask
from hamcrest import *
from app.blueprint import Books
from app.model import Book
from marshmallow import EXCLUDE
from marshmallow.exceptions import ValidationError


@pytest.fixture(scope='module')
def app() -> Flask:
    return Flask(__name__)


def test_get_books(app: Flask):
    book_service = MagicMock()
    expected_books = [{
        'title': 'Freakonomics',
        'genre': 'Economics'
    }, {
        'title': 'The Lord of the Rings',
        'genre': 'Novel'
    }]
    book_service.get_books.return_value = [
        Book(**book) for book in expected_books]

    with patch('app.blueprint.books.BookService', return_value=book_service):
        blueprint = Books()
        with app.test_request_context('/api/books'):
            response = blueprint.books()

    assert_that(response.status_code, equal_to(HTTPStatus.OK))
    assert_that(response.is_json,
                'books should be returned in JSON format')
    matchers = [has_entries(book) for book in expected_books]
    assert_that(response.json, contains_inanyorder(*matchers))
    book_service.get_books.assert_called_once()


def test_add_book(app: Flask):
    book_service = MagicMock()
    book_id = 'some-id'

    def mock_add_book(book: Book):
        book.uid = book_id
        return book_id

    book_service.add_book.side_effect = mock_add_book
    book_to_add = {
        'title': 'Freakonomics',
        'genre': 'Economics'
    }

    with patch('app.blueprint.books.BookService', return_value=book_service):
        blueprint = Books()
        with app.test_request_context('/api/books', method='POST', json=book_to_add):
            response, status_code, headers = blueprint.books()

    assert_that(status_code, equal_to(HTTPStatus.CREATED))

    expected_headers = {
        'ETag': instance_of(str),
        'Location': f'/api/books/{book_id}'
    }
    assert_that(headers, has_entries(expected_headers))

    expected_json = {
        'id': book_id
    }
    assert_that(response, has_entries(expected_json))

    matcher = has_properties(book_to_add)
    book_service.add_book.assert_called_once_with(
        match_equality(matcher))


def test_get_book_when_book_found(app: Flask):
    book_service = MagicMock()
    book_id = 'some-id'
    expected_book = {
        'title': 'Freakonomics',
        'genre': 'Economics',
        'uid': book_id
    }

    book_service.get_book.return_value = Book(**expected_book)

    with patch('app.blueprint.books.BookService', return_value=book_service):
        blueprint = Books()
        with app.test_request_context(f'/api/books/{book_id}'):
            response = blueprint.book(book_id)

    assert_that(response.status_code, equal_to(HTTPStatus.OK))
    assert_that(response.is_json,
                'book should be returned in JSON format')
    assert_that(response.json, has_entries(expected_book))


def test_get_book_when_book_not_found(app: Flask):
    book_service = MagicMock()
    book_service.get_book.return_value = None

    with patch('app.blueprint.books.BookService', return_value=book_service):
        blueprint = Books()
        with app.test_request_context('/api/books/some-id'):
            _, status_code = blueprint.book('some-id')

    assert_that(status_code, equal_to(HTTPStatus.NOT_FOUND))


def test_add_book_not_json(app: Flask):
    with patch('app.blueprint.books.BookService'):
        blueprint = Books()
        with app.test_request_context('/api/books', method='POST', data='some book'):
            _, status_code = blueprint.books()

    assert_that(status_code, equal_to(
        HTTPStatus.UNSUPPORTED_MEDIA_TYPE))


def test_add_book_invalid_book(app: Flask):
    with patch('app.blueprint.books.BookService'):
        blueprint = Books()
        invalid_book = {
            'some unknown property': 'value'
        }
        with app.test_request_context('/api/books', method='POST', json=invalid_book):
            _, status_code = blueprint.books()

    assert_that(status_code, equal_to(HTTPStatus.UNPROCESSABLE_ENTITY))


def test_update_book_valid_json_updates_book(app: Flask):
    book_service = MagicMock()
    updated_book_payload = {
        'title': 'The Lord of the Rings',
        'genre': 'Novel'
    }
    existing_book = Book(title='The Lord of the Rings', genre='Biography')
    book_service.get_book.return_value = existing_book

    book_schema = MagicMock()

    with patch('app.blueprint.books.BookService', return_value=book_service), \
            patch('app.blueprint.books.BookSchema', return_value=book_schema):
        blueprint = Books()
        with app.test_request_context('/api/books/some-id', method='PUT',
                                      json=updated_book_payload):
            response, status_code, headers = blueprint.book('some-id')

    assert_that(status_code, equal_to(HTTPStatus.OK))
    book_schema.load.assert_called_once_with(
        updated_book_payload, instance=existing_book, unknown=EXCLUDE)
    book_service.commit_changes.assert_called_once()


def test_update_book_invalid_book_returns_error_code(app: Flask):
    book_service = MagicMock()
    book_service.get_book.return_value = 'some book'
    updated_book_payload = {
        'invalid': 'book'
    }

    book_schema = MagicMock()
    book_schema.load.side_effect = ValidationError('bobbob')

    with patch('app.blueprint.books.BookService', return_value=book_service), \
            patch('app.blueprint.books.BookSchema', return_value=book_schema):
        blueprint = Books()
        with app.test_request_context('/api/books/some-id', method='PUT',
                                      json=updated_book_payload):
            response, status_code = blueprint.book('some-id')

    assert_that(status_code, equal_to(HTTPStatus.UNPROCESSABLE_ENTITY))


def test_update_book_invalid_json_returns_error_code(app: Flask):
    book_service = MagicMock()
    book_service.get_book.return_value = 'some book'
    updated_book_payload = 'not json'

    book_schema = MagicMock()
    book_schema.load.side_effect = ValidationError('bobbob')

    with patch('app.blueprint.books.BookService', return_value=book_service), \
            patch('app.blueprint.books.BookSchema', return_value=book_schema):
        blueprint = Books()
        with app.test_request_context('/api/books/some-id', method='PUT',
                                      data=updated_book_payload):
            response, status_code = blueprint.book('some-id')

    assert_that(status_code, equal_to(HTTPStatus.UNSUPPORTED_MEDIA_TYPE))
