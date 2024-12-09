from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import (
    List,
    Optional,
    Union,
)

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class ColorSchema(
    str,
    Enum
):
    MODERN = "Modern"
    PALE = "Pale"
    CLASSIC = "Classic"
    CLASSIC_PALE = "ClassicPale"
    NIGHT = "Night"


class UserRole(
    str,
    Enum
):
    GUEST = 'Guest'
    PLAYER = 'Player'
    ADMINISTRATOR = 'Administrator'
    NANNY_MODERATOR = 'NannyModerator'
    REGULAR_MODERATOR = 'RegularModerator'
    SENIOR_MODERATOR = 'SeniorModerator'


class BbParseMode(
    str,
    Enum
):
    COMMON = 'Common'
    INFO = 'Info'
    POST = 'Post'
    CHAT = 'Chat'


class Rating(
    BaseModel
):
    enabled: bool
    quality: int
    quantity: int


class InfoBbText(
    BaseModel
):
    value: str = Field(
        None,
        alias='value'
    )
    parse_mode: BbParseMode = Field(
        None,
        alias='parseMode'
    )


class PagingSettings(
    BaseModel
):
    posts_per_page: int = Field(
        ...,
        alias='postsPerPage'
    )
    comments_per_page: int = Field(
        ...,
        alias='commentsPerPage'
    )
    topics_per_page: int = Field(
        ...,
        alias='topicsPerPage'
    )
    messages_per_page: int = Field(
        ...,
        alias='messagesPerPage'
    )
    entities_per_page: int = Field(
        ...,
        alias='entitiesPerPage'
    )


class UserSettings(
    BaseModel
):
    color_schema: ColorSchema = Field(
        ...,
        alias='colorSchema'
    )
    nanny_greetings_message: str = Field(
        None,
        alias='nannyGreetingsMessage'
    )
    paging: PagingSettings


class UserDetails(
    BaseModel
):
    login: str
    roles: List[UserRole]
    medium_picture_url: str = Field(
        None,
        alias='mediumPictureUrl'
    )
    small_picture_url: str = Field(
        None,
        alias='smallPictureUrl'
    )
    status: str = Field(
        None,
        alias='status'
    )
    rating: Rating
    online: datetime = Field(
        None,
        alias='online'
    )
    name: str = Field(
        None,
        alias='name'
    )
    location: str = Field(
        None,
        alias='location'
    )
    registration: datetime = Field(
        None,
        alias='registration'
    )
    icq: str = Field(
        None,
        alias='icq'
    )
    skype: str = Field(
        None,
        alias='skype'
    )
    original_picture_url: str = Field(
        None,
        alias='originalPictureUrl'
    )
    info: Union[InfoBbText, str] = Field(
        None,
        alias='info'
    )
    settings: UserSettings


class UserDetailsEnvelope(
    BaseModel
):
    model_config = ConfigDict(
        extra='forbid'
    )
    resource: Optional[UserDetails] = None
    metadata: Optional[str] = None
