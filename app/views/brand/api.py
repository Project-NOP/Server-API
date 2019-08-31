from operator import and_

from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Conflict, BadRequest, NotFound

from app.context import context_property
from app.decorators.validation import validate_with_pydantic, PayloadLocation
from app.extensions import write_db
from app.models.brand import TblBrands
from app.models.product import TblProducts
from app.views.brand.schema import BrandCreationModel


class Brands(Resource):
    @validate_with_pydantic(PayloadLocation.JSON, BrandCreationModel)
    def post(self):
        session = write_db.session

        payload: BrandCreationModel = context_property.request_payload

        if TblBrands.get_by_name(read_session=session, name=payload.name):
            raise Conflict()

        brand = TblBrands(
            name=payload.name, logo_url=payload.logoUrl, category_id=payload.categoryId
        )

        try:
            session.add(brand)
            session.commit()
        except IntegrityError:
            raise BadRequest({"invalid": ["categoryId"]})

        return {}, 201, {"Location": f"/brands/{brand.id}"}

    def get(self):
        session = write_db.session

        brand: TblBrands
        return (
            {
                "data": [
                    {
                        "id": brand.id,
                        "name": brand.name,
                        "logoUrl": brand.logo_url,
                        "category": {
                            "id": brand.category.id,
                            "name": brand.category.name,
                        },
                    }
                    for brand in TblBrands.get_all(read_session=session)
                ]
            },
            200,
        )


class Brand(Resource):
    def get(self, id):
        session = write_db.session

        brand = TblBrands.get_by_id(read_session=session, id=id)

        if brand is None:
            raise NotFound()

        alternative_brands = session.query(
            TblBrands
        ).filter(
            and_(
                TblBrands.category_id == brand.category_id,
                TblBrands.id != brand.id
            )
        )

        product: TblProducts
        return (
            {
                "data": {
                    'products': [
                        {
                            "id": product.id,
                            "name": product.name,
                            "imageUrl": product.image_url,
                            "category": {
                                "id": product.category.id,
                                "name": product.category.name,
                            },
                        }
                        for product in brand.products
                    ],
                    'alternatives': [
                        {
                            "id": brand.id,
                            "name": brand.name,
                            "logoUrl": brand.logo_url,
                            "category": {
                                "id": brand.category.id,
                                "name": brand.category.name,
                            },
                        }
                        for brand in alternative_brands
                    ]
                }
            },
            200,
        )


class BrandAlternatives(Resource):
    def get(self, id):
        session = write_db.session

        brand = TblBrands.get_by_id(read_session=session, id=id)

        if brand is None:
            raise NotFound()

        alternative_brands = session.query(
            TblBrands
        ).filter(
            and_(
                TblBrands.category_id == brand.category_id,
                TblBrands.id != brand.id
            )
        )

        brand: TblBrands
        return (
            {
                "data": [
                    {
                        "id": brand.id,
                        "name": brand.name,
                        "logoUrl": brand.logo_url,
                        "category": {
                            "id": brand.category.id,
                            "name": brand.category.name,
                        },
                    }
                    for brand in alternative_brands
                ]
            },
            200,
        )
