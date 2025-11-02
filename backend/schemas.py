from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class GameBase(BaseModel):
    name: str
    genre: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int
    created_at: datetime
    avg_sentiment: Optional[float] = None
    post_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    game_id: int
    username: str


class Post(PostBase):
    id: int
    user_id: int
    game_id: int
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    confidence: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    username: Optional[str] = None
    game_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    post_id: int
    username: str


class Comment(CommentBase):
    id: int
    post_id: int
    user_id: int
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    created_at: datetime
    username: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class GameAnalytics(BaseModel):
    game_id: int
    game_name: str
    avg_sentiment: float
    post_count: int
    positive_count: int
    negative_count: int
    neutral_count: int

    model_config = ConfigDict(from_attributes=True)
