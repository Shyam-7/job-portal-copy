from pydantic import BaseModel
from app.db.schemas.common.base_schema import BaseSchema

class SavedJobBase(BaseModel):
    user_id: str
    job_id: str

class SavedJobCreate(SavedJobBase):
    pass

class SavedJob(SavedJobBase, BaseSchema):
    class Config:
        from_attributes = True
