from http import HTTPStatus
from tempfile import mkstemp
from unittest.mock import patch, MagicMock

from hamcrest.library.integration.match_equality import match_equality
from hamcrest.library.object.hasproperty import has_properties
from hamcrest.core import assert_that, equal_to, instance_of
from hamcrest.library.collection.isdict_containingentries import has_entries
from hamcrest.library.collection.issequence_containinginanyorder import contains_inanyorder

from app import create_app
from app.model import Book


def create_test_client():
    _, db_path = mkstemp()

    app = create_app({
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'TESTING': True
    })

    return app.test_client()


def test_get_books():
    book_service = MagicMock()
    expected_books = [{
        'title': 'Freakonomics',
        'genre': 'Economics'
    }]
    book_service.return_value.get_books.return_value = [
        Book(**book) for book in expected_books]

    with patch('app.BookService', book_service):
        test_client = create_test_client()

    response = test_client.get('/api/books')
    assert_that(response.status_code, equal_to(HTTPStatus.OK))
    assert_that(response.is_json,
                'books should be returned in JSON format')
    matchers = [has_entries(book) for book in expected_books]
    assert_that(response.json, contains_inanyorder(*matchers))
    book_service.return_value.get_books.assert_called_once()


def test_add_book():
    book_service = MagicMock()
    book_id = 'some-id'

    def mock_add_book(book: Book):
        book.uid = book_id
        return book_id

    book_service.return_value.add_book.side_effect = mock_add_book
    book_to_add = {
        'title': 'Freakonomics',
        'genre': 'Economics'
    }

    with patch('app.BookService', book_service):
        test_client = create_test_client()

    response = test_client.post('/api/books', json=book_to_add)
    assert_that(response.status_code, equal_to(HTTPStatus.CREATED))

    expected_headers = {
        'ETag': instance_of(str),
        'Location': f'http://localhost/api/books/{book_id}'
    }
    assert_that(response.headers, has_entries(expected_headers))

    expected_json = {
        'id': book_id
    }
    assert_that(response.json, has_entries(expected_json))

    matcher = has_properties(book_to_add)
    book_service.return_value.add_book.assert_called_once_with(
        match_equality(matcher))


def test_get_book_when_book_found():
    book_service = MagicMock()
    book_id = 'some-id'
    expected_book = {
        'title': 'Freakonomics',
        'genre': 'Economics',
        'uid': book_id
    }

    book_service.return_value.get_book.return_value = Book(
        title=expected_book['title'], genre=expected_book['genre'], uid=book_id)

    with patch('app.BookService', book_service):
        test_client = create_test_client()

    response = test_client.get(f'/api/books/{book_id}')
    assert_that(response.status_code, equal_to(HTTPStatus.OK))
    assert_that(response.is_json)
    assert_that(response.get_json(), has_entries(expected_book))
    book_service.return_value.get_book.assert_called_once()


def test_get_book_when_book_not_found():
    book_service = MagicMock()
    book_service.return_value.get_book.return_value = None

    with patch('app.BookService', book_service):
        test_client = create_test_client()

    response = test_client.get('/api/books/some-id')
    assert_that(response.status_code, equal_to(HTTPStatus.NOT_FOUND))
