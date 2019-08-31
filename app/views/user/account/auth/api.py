from datetime import timedelta

from flask_jwt_extended import create_access_token
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from app.constants.api.auth import VALID_PROVIDERS
from app.context import context_property
from app.decorators.validation import validate_with_pydantic, PayloadLocation
from app.extensions import write_db
from app.models.user import TblUsers
from app.views.user.account.auth.schema import AuthModel


class Auth(Resource):
    @validate_with_pydantic(PayloadLocation.JSON, AuthModel)
    def post(self, provider):
        if provider not in VALID_PROVIDERS:
            raise BadRequest(f"Provider must be in {VALID_PROVIDERS}")

        session = write_db.session

        payload: AuthModel = context_property.request_payload

        # TODO provider별 oauth validation하는 게 좋음

        user = TblUsers.get_first(
            read_session=session, where_clause=TblUsers.id == payload.id
        )

        if user is None:
            user = TblUsers(
                id=payload.id,
                provider=provider,
                thumbnail_url=payload.thumbnailUrl,
                name=payload.name,
            )

            session.add(user)

            session.commit()

        return (
            {
                "data": {
                    "accessToken": create_access_token(
                        identity=user.id, expires_delta=timedelta(days=3)
                    )
                }
            },
            201,
        )
