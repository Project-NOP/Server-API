from dataclasses import dataclass


@dataclass
class AuthModel:
    id: str
    thumbnailUrl: str
    name: str
