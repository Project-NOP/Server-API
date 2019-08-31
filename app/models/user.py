from sqlalchemy import Column, String

from app.constants.schema import IMAGE_URL_MAX_LENGTH
from app.models import Base


class TblUsers(Base):
    __tablename__ = "tbl_users"

    id = Column(String(256), primary_key=True)
    provider = Column(String(16), nullable=False)
    thumbnail_url = Column(String(IMAGE_URL_MAX_LENGTH), nullable=False)
    name = Column(String(64), nullable=False)
