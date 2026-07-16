from pydantic import BaseModel


class PayCacheRead(BaseModel):
    order_id: int
    code: str