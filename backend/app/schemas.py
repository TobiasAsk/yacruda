from app.model import Book
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field


class BookSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        load_instance = True

    uid = auto_field(dump_only=True)
    created_at = auto_field(dump_only=True)
    last_modified_at = auto_field(dump_only=True)
