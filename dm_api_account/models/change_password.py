from pydantic import BaseModel, Field, ConfigDict


class ChangePassword(BaseModel):
    model_config = ConfigDict(extra='forbid')  # required fields to fill in
    login: str = Field(..., description='Login')
    token: str = Field(..., description='Password reset token')
    old_password: str = Field(..., description='Old password', serialization_alias='oldPassword')
    new_password: str = Field(..., description='New password', serialization_alias='newPassword')
