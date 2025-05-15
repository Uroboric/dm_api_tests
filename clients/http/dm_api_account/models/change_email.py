from pydantic import BaseModel, Field, ConfigDict


class ChangeEmail(BaseModel):
    model_config = ConfigDict(extra='forbid')  # required fields to fill in
    login: str = Field(..., description='Login')
    password: str = Field(..., description='Password')
    email: str = Field(..., description='Email')
