# pylint: disable=wildcard-import, unused-wildcard-import, redefined-outer-name, missing-function-docstring
from app.service import BookService
from unittest.mock import patch
from app.model import Book
import pytest
from hamcrest import *


@pytest.fixture
def book_service():
    return BookService()


@patch('app.service.book_service.Book')
def test_get_books(mock_book, book_service):
    books = [
        Book(title='The Lord of the Rings', genre='Fantasy novel')
    ]
    mock_book.query.all.return_value = books
    returned_books = book_service.get_books()
    assert_that(returned_books, contains_inanyorder(*books))


@patch('app.service.book_service.db')
def test_add_book_sets_id_inserts_into_db(mock_db, book_service):
    book_to_add = Book(title='The Lord of the Rings', genre='Fantasy novel')
    book_id = book_service.add_book(book_to_add)
    assert_that(book_to_add, has_property('uid', book_id))
    mock_db.session.add.assert_called_once_with(book_to_add)
    mock_db.session.commit.assert_called_once()
 