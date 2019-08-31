from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.constants.schema import IMAGE_URL_MAX_LENGTH
from app.models import Base
from app.models.category import TblProductCategories


class TblProducts(Base):
    __tablename__ = "tbl_products"

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False, unique=True)
    image_url = Column(String(IMAGE_URL_MAX_LENGTH), nullable=False)
    brand_id = Column(Integer, ForeignKey("tbl_brands.id"), nullable=False)
    category_id = Column(
        Integer, ForeignKey("tbl_product_categories.id"), nullable=False
    )

    category = relationship(TblProductCategories)
