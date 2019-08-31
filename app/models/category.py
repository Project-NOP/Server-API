from sqlalchemy import Column, String, Integer

from app.models import Base


class CategoryBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)


class TblBrandCategories(CategoryBase):
    __tablename__ = "tbl_brand_categories"


class TblProductCategories(CategoryBase):
    __tablename__ = "tbl_product_categories"


class TblCampaignCategories(CategoryBase):
    __tablename__ = "tbl_campaign_categories"
