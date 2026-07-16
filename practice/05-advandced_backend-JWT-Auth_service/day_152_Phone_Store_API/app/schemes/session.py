from datetime import datetime
from pydantic import BaseModel


class RefreshSessionCreate(BaseModel):
    user_id: int
    refresh_token: str
    expires_at: datetime