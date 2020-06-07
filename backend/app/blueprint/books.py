from http import HTTPStatus

from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError
from marshmallow import EXCLUDE

from app.model import Book
from app.schemas import BookSchema
from app.service import BookService


class Books(Blueprint):

    def __init__(self):
        super().__init__('book_blueprint', __name__, url_prefix='/api/books')
        self.add_url_rule('', 'books', self.books, methods=['GET', 'POST'])
        self.add_url_rule('/<book_uid>', 'book', self.book,
                          methods=['GET', 'PUT'])
        self.book_service = BookService()
        self.book_schema = BookSchema(exclude=['id'])

    def books(self):
        if request.method == 'GET':
            books = self.book_service.get_books()
            return jsonify(self.book_schema.dump(books, many=True))

        if request.method == 'POST' and request.is_json:
            try:
                book_to_add = self.book_schema.load(
                    request.get_json(), transient=True)
            except ValidationError as validation_error:
                return {
                    'status': 'error',
                    'error': validation_error.messages
                }, HTTPStatus.UNPROCESSABLE_ENTITY

            uid = self.book_service.add_book(book_to_add)

            return {
                'id': uid
            }, HTTPStatus.CREATED, self.created_book_headers(book_to_add)

        return {
            'status': 'error',
            'error': 'Request body type not supported'
        }, HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    def book(self, book_uid: str):
        book = self.book_service.get_book(book_uid)

        if not book:
            return {
                'status': 'error',
                'error': 'Resource not found'
            }, HTTPStatus.NOT_FOUND

        if request.method == 'GET':
            return jsonify(self.book_schema.dump(book))

        if request.method == 'PUT' and request.is_json:
            try:
                self.book_schema.load(request.get_json(),
                                      instance=book, unknown=EXCLUDE)
                self.book_service.commit_changes()
            except ValidationError as validation_error:
                return {
                    'status': 'error',
                    'error': validation_error.messages
                }, HTTPStatus.UNPROCESSABLE_ENTITY

            return {
                'status': 'Book updated'
            }, HTTPStatus.OK, self.created_book_headers(book)

        return {
            'status': 'error',
            'error': 'Request body type not supported'
        }, HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    def created_book_headers(self, book: Book) -> dict:
        return {
            'ETag': str(hash(book)),
            'Location': f'/api/books/{book.uid}'
        }
