from dataclasses import dataclass


@dataclass
class BrandCreationModel:
    name: str
    logoUrl: str
    categoryId: int
