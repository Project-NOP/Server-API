from typing import Optional

from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.constants.schema import IMAGE_URL_MAX_LENGTH
from app.models import Base
from app.models.category import TblBrandCategories
from app.models.product import TblProducts


class TblBrands(Base):
    __tablename__ = "tbl_brands"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    logo_url = Column(String(IMAGE_URL_MAX_LENGTH), nullable=False)
    category_id = Column(Integer, ForeignKey("tbl_brand_categories.id"), nullable=False)

    category = relationship(TblBrandCategories)
    products = relationship(TblProducts)

    @classmethod
    def get_by_name(cls, *, read_session, name) -> Optional["TblBrands"]:
        return cls.get_first(read_session=read_session, where_clause=cls.name == name)

    @classmethod
    def get_by_id(cls, *, read_session, id) -> Optional["TblBrands"]:
        return cls.get_first(read_session=read_session, where_clause=cls.id == id)
