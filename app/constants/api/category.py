from app.models.category import (
    TblBrandCategories,
    TblProductCategories,
    TblCampaignCategories,
)

CATEGORY_KIND_TO_MODEL = {
    "brand": TblBrandCategories,
    "product": TblProductCategories,
    "campaign": TblCampaignCategories,
}
