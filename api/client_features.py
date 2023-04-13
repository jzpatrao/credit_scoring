from pydantic import BaseModel

class ClientFeatures(BaseModel):
    NAME_INCOME_TYPE: str
    DAYS_CREDIT: float
    DAYS_BIRTH: int
    DAYS_EMPLOYED_PERC: float
    REGION_RATING_CLIENT: int
    EXT_SOURCE_1: float
    EXT_SOURCE_2: float
    EXT_SOURCE_3: float