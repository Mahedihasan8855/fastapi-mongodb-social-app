from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utilities.connection import create_mongo_connection
from utilities.dto import (
    UserRegistrationRequest,
    UserProfileUpdateRequest,
    UserProfileResponse,
    PostCreateRequest,
    PostResponse,
)
from utilities.service import (
    process_register_user,
    process_update_user_profile,
    process_user_login,
    retrieve_user_profile,
    process_create_post,
    process_like_post,
    process_comment_on_post,
    process_share_post,
    search_posts_by_keyword,
    process_add_connection,
    process_remove_connection,
    retrieve_connections,
    delete_post,
    get_user_posts,

)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
def register_user(user_data: UserRegistrationRequest):
    return process_register_user(user_data)


@app.post("/login")
def login_user(email: str, password: str):
    return process_user_login(email, password)


@app.put("/profile")
def update_profile(profile_data: UserProfileUpdateRequest):
    return process_update_user_profile(profile_data)


@app.get("/profile/{user_name}", response_model=UserProfileResponse)
def get_user_profile(user_name: str):
    return retrieve_user_profile(user_name)


@app.post("/posts")
def create_post(post_data: PostCreateRequest):
    return process_create_post(post_data)


@app.post("/posts/{post_id}/like")
def like_post(post_id: str):    
    return process_like_post(post_id)


@app.post("/posts/{post_id}/comment")
def comment_on_post(post_id: str, comment: str):
    return process_comment_on_post(post_id, comment)


@app.post("/posts/{post_id}/share")
def share_post(post_id: str):
    return process_share_post(post_id)


@app.get("/posts/{keyword}/search")
def search_posts(keyword: str):
    res = search_posts_by_keyword(keyword)
    return res

@app.delete("/posts/{post_id}")
def remove_post(post_id: str):
    return delete_post(post_id)

@app.get("/posts/user/{username}")
def retrieve_user_posts(username: str):
    return get_user_posts(username)


@app.post("/connections/{user_email}")
def add_connection(user_email: str, connection_email: str):
    return process_add_connection(user_email, connection_email)


@app.get("/connections/{user_email}")
def get_connections(user_email: str):
    return retrieve_connections(user_email)


@app.delete("/connections/{user_email}/{connection_email}")
def remove_connection(user_email: str, connection_email: str):
    return process_remove_connection(user_email, connection_email)

