from utilities.connection import create_mongo_connection

client = create_mongo_connection()

db = client["social_network_db"]

users_collection = db["users"]
posts_collection = db["posts"]
connections_collection = db["connections"]

users_collection.create_index("email", unique=True)
posts_collection.create_index("user_id")



sample_users = [
    {
        "username": "user1",
        "email": "user1@example.com",
        "password": "password1",
        "address": "123 Main St, City",
        "birth_date": "1990-01-01",
        "age": 33,
        "name": "John Doe",
        "profile_picture": "profile1.jpg",
        "bio": "I love connecting with new people!",
        "social_media_links": {
            "facebook": "https://www.facebook.com/user1",
            "twitter": "https://www.twitter.com/user1",
        },
    },
    {
        "username": "user2",
        "email": "user2@example.com",
        "password": "password2",
        "address": "456 Elm St, City",
        "birth_date": "1995-05-10",
        "age": 28,
        "name": "Jane Smith",
        "profile_picture": "profile2.jpg",
        "bio": "Travel enthusiast and photography lover",
        "social_media_links": {
            "instagram": "https://www.instagram.com/user2",
            "linkedin": "https://www.linkedin.com/in/user2",
        },
    },
]

sample_posts = [
    {
        "username": "user1",
        "details": "Excited to join this social networking platform!",
        "images": ["post1.jpg"],
        "likes": 1,
        "comments": [],
    },
    {
        "username": "user2",
        "details": "Just returned from an amazing trip. Sharing some photos!",
        "images": ["post2.jpg"],
        "likes": 1,
        "comments": [],
    },
]

sample_connections = [
    {"username": "user1", "connected_users": ["user2"]},
    {"username": "user2", "connected_users": ["user1"]},
]

users_collection.insert_many(sample_users)
posts_collection.insert_many(sample_posts)
connections_collection.insert_many(sample_connections)



keyword = "trip"

posts_collection.create_index([("details", "text")])

search_results = posts_collection.find({"$text": {"$search": keyword}})
search_results_list = list(search_results)
posts=[]
for post in search_results_list:
    posts.append(post)

print(posts)