from passlib.context import CryptContext
from pymongo.collection import Collection
from fastapi import HTTPException
from utilities.connection import create_mongo_connection
from utilities.dto import UserRegistrationRequest, UserProfileUpdateRequest, PostCreateRequest, PostResponse
from bson import ObjectId

client = create_mongo_connection()

db = client["social_network_db"]

users_collection = db["users"]
posts_collection = db["posts"]
connections_collection = db["connections"]



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def process_register_user(user_data: UserRegistrationRequest):
    existing_user = users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user_data.password)
    user_doc = {
        "username": user_data.username,
        "email": user_data.email,
        "password": hashed_password,
        "address": user_data.address,
        "birth_date": user_data.birth_date,
        "age": user_data.age,
        "name": user_data.name,
        "profile_picture": user_data.profile_picture,
        "bio": user_data.bio,
        "social_media_links": user_data.social_media_links
    }
    users_collection.insert_one(user_doc)
    return {"email": user_data.email}



def delete_post(post_id: str):
    result = posts_collection.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"message": "Post deleted successfully"}

def get_user_posts(username: str):
    user_posts = list(posts_collection.find({"username": username},{"_id": 0}))
    print(user_posts)
    processed_posts = []
    for post in user_posts:
        processed_posts.append(post)
    print(processed_posts)
    return processed_posts

def process_update_user_profile(user_data: UserProfileUpdateRequest):
    existing_user = users_collection.find_one({"email": user_data.email})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user_data = user_data.dict(exclude_unset=True)
    users_collection.update_one({"email": user_data.email}, {"$set": updated_user_data})
    return {"email": user_data.email}


def process_user_login(email: str, password: str):
    user = users_collection.find_one({"email": email})
    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"email": email}


def retrieve_user_profile(user_name: str):
    user_profile = users_collection.find_one({"username": user_name}, {"_id": 0, "password": 0})
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    return user_profile




def process_create_post(post_data: PostCreateRequest):
    post_doc = {
        "username": post_data.username,
        "details": post_data.details,
        "images": post_data.images,
        "likes": 0,
        "comments": [],
        "shares": 0,
    }
    result = posts_collection.insert_one(post_doc)
    post_id = str(result.inserted_id)
    return {"id": post_id}


def process_like_post(post_id: str):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    updated_likes = post["likes"] + 1
    posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": {"likes": updated_likes}})
    return True


def process_comment_on_post(post_id: str, comment: str):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    updated_comments = post["comments"]
    updated_comments.append(comment)
    posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": {"comments": updated_comments}})
    return True


def process_share_post(post_id: str):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    updated_shares = post["shares"] + 1
    posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": {"shares": updated_shares}})
    return True


def search_posts_by_keyword(keyword: str):
    
    posts_collection.create_index([("details", "text")])

    search_results = posts_collection.find({"$text": {"$search": keyword}}, {"_id": 0})
    search_results_list = list(search_results)
    posts=[]
    for post in search_results_list:
        posts.append(post)
    print(posts)
    return posts


def retrieve_connections(username: str):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    connections = connections_collection.find_one({"username": username})
    if not connections:
        return []

    return connections.get("connections", [])

def process_add_connection(username: str, connection_email: str):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    connection = users_collection.find_one({"email": connection_email})
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")

    connections = connections_collection.find_one({"username": username})
    if connections and connection_email in connections.get("connections", []):
        raise HTTPException(status_code=400, detail="Connection already exists")

    connections_collection.update_one(
        {"username": username},
        {"$addToSet": {"connections": connection_email}},
        upsert=True
    )
    return {"message": "Connection added successfully"}


def process_remove_connection(username: str, connection_email: str):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    connection = users_collection.find_one({"email": connection_email})
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")

    connections = connections_collection.find_one({"username": username})
    if not connections or connection_email not in connections.get("connections", []):
        raise HTTPException(status_code=400, detail="Connection does not exist")

    connections_collection.update_one(
        {"username": username},
        {"$pull": {"connections": connection_email}}
    )
    return {"message": "Connection removed successfully"}