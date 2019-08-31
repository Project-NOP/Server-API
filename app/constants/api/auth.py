from dataclasses import dataclass
from typing import Optional, Callable

import boto3

from app.constants.aws.vpc import SSM_VPCE_URL

ssm = boto3.client("ssm", endpoint_url=SSM_VPCE_URL)


@dataclass
class OAuthProvider:
    client_secret: str
    access_token_url: str
    profile_url: str
    id_extractor: Callable
    name_extractor: Callable
    thumbnail_extractor: Callable
    scope: Optional[list] = None


class OAuthProviders:
    GOOGLE = OAuthProvider(
        client_secret=ssm.get_parameter(Name="nop-google-client-secret")["Parameter"][
            "Value"
        ],
        access_token_url="https://www.googleapis.com/oauth2/v4/token",
        profile_url="https://www.googleapis.com/oauth2/v1/userinfo",
        id_extractor=lambda payload: payload["id"],
        name_extractor=lambda payload: payload["picture"],
        thumbnail_extractor=lambda payload: payload["name"],
        scope=["https://www.googleapis.com/auth/userinfo.profile"],
    )

    FACEBOOK = OAuthProvider(
        client_secret=ssm.get_parameter(Name="nop-facebook-client-secret")["Parameter"][
            "Value"
        ],
        access_token_url="https://graph.facebook.com/v3.2/oauth/access_token",
        profile_url="https://graph.facebook.com/me?fields=id,name,picture",
        id_extractor=lambda payload: payload["id"],
        name_extractor=lambda payload: payload["name"],
        thumbnail_extractor=lambda payload: payload["picture"]["data"]["url"],
    )

    # TWITTER = OAuthProvider()


PROVIDER_KEY_TO_PROVIDER_MODEL = {
    "google": OAuthProviders.GOOGLE,
    "facebook": OAuthProviders.FACEBOOK,
}


VALID_PROVIDERS = PROVIDER_KEY_TO_PROVIDER_MODEL.keys()
