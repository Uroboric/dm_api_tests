from pydantic import BaseModel, Field, ConfigDict


class LoginCredentials(BaseModel):
    model_config = ConfigDict(extra='forbid')  # required fields to fill in
    login: str = Field(..., description='Login')
    password: str = Field(..., description='Password')
    remember_me: bool = Field(False, description='Remember Me', serialization_alias='rememberMe')
