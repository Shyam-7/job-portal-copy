from pydantic import BaseModel
from app.db.schemas.common.base_schema import BaseSchema

class MessageBase(BaseModel):
    application_id: str
    recipient_id: str
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase, BaseSchema):
    class Config:
        from_attributes = True
