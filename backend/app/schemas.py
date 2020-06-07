from app.model import Book
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(SQLAlchemyAutoSchema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


class BookSchema(CamelCaseSchema):
    class Meta:
        model = Book
        load_instance = True

    uid = auto_field(dump_only=True)
    created_at = auto_field(dump_only=True)
    last_modified_at = auto_field(dump_only=True)
