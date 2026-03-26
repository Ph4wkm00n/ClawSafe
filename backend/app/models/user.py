"""User and authentication models."""

from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    role: str = "viewer"


class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    is_active: bool
    created_at: str


class UserList(BaseModel):
    users: list[UserResponse]
    total: int


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
