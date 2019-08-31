from typing import Type

from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from app.constants.api.category import CATEGORY_KIND_TO_MODEL
from app.extensions import write_db
from app.models.category import CategoryBase


class Categories(Resource):
    def get(self, kind):
        session = write_db.session

        try:
            model: Type[CategoryBase] = CATEGORY_KIND_TO_MODEL[kind]
        except KeyError:
            raise BadRequest(f"Category kind must be in {CATEGORY_KIND_TO_MODEL}")

        category: Type[CategoryBase]
        return (
            {
                "data": [
                    {"id": category.id, "name": category.name}
                    for category in model.get_all(read_session=session)
                ]
            },
            200,
        )
