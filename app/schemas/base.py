from pydantic import BaseModel, ConfigDict


class RequestBaseModel(BaseModel):
    """
    Base for request DTOs (forbid unknown fields).
    """
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class ResponseBaseModel(BaseModel):
    """
    Base for response DTOs (allow field aliasing and from ORM).
    """
    model_config = ConfigDict(
        populate_by_name=True, from_attributes=True, str_strip_whitespace=True
    )
