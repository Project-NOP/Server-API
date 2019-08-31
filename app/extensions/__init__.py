from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.models import WriteDB

cors = CORS()
jwt = JWTManager()
write_db = WriteDB()
