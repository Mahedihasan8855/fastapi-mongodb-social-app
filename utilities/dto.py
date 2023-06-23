from pydantic import BaseModel
from typing import List

class UserRegistrationRequest(BaseModel):
    username: str
    email: str
    password: str
    address: str
    birth_date: str
    age: int
    name: str
    profile_picture: str
    bio: str
    social_media_links: dict


class UserProfileResponse(BaseModel):
    username: str
    email: str
    address: str
    birth_date: str
    age: int
    name: str
    profile_picture: str
    bio: str
    social_media_links: dict

class UserProfileUpdateRequest(BaseModel):
    email: str
    address: str
    birth_date: str
    age: int
    name: str


class PostCreateRequest(BaseModel):
    username: str
    details: str
    images: List[str]


class PostResponse(BaseModel):
    id: str
    username: str
    details: str
    images: List[str]
    likes: int
    comments: List[str]
    shares: int
