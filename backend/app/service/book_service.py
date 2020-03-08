from app.model import Book, db
from uuid import uuid4


class BookService:

    def get_books(self):
        return Book.query.all()

    def add_book(self, book: Book):
        uid = str(uuid4())
        book.uid = uid
        db.session.add(book)
        db.session.commit()
        return uid

    def get_book(self, book_uid: str):
        return Book.query.filter_by(uid=book_uid).first()

    def commit_changes(self):
        db.session.commit()
