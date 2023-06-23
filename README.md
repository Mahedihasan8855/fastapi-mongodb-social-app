# Create virtual environment
python3 -m venv virtual

# Activate environment
source virtual/bin/activate

# Install required packages
pip install -r requirements.txt


# Commands for Setup Mongo DB

docker pull mongo

docker run -d -p 8002:27017 --name mymongo -v /path/to/data:/data/db -e MONGO_INITDB_ROOT_USERNAME=sa -e MONGO_INITDB_ROOT_PASSWORD=VERY_STRONG_PASSWORD mongo


Find--container ID
82fcd473246be8539c96fe1dcb92d05c39bdcfa935a6ce7d03696f02a8a03c4a

docker run: This command is used to run a Docker container.
-d: It runs the container in the background (detached mode).
-p 8002:27017: It maps port 8002 on the host machine to port 27017 inside the container. This allows you to access MongoDB running inside the 
-e MONGO_INITDB_ROOT_USERNAME=sa -e MONGO_INITDB_ROOT_PASSWORD=VERY_STRONG_PASSWORD: These environment variables are used to set the root username and password for the MongoDB instance inside the container.

docker start <containerID>


# create a .env file and use variables within it

follow .env.example and cretae .env in root directory 
DB_URL="mongodb://sa:VERY_STRONG_PASSWORD@localhost:8002/?authMechanism=DEFAULT"
# Run DB scripts

python3 script.py

# Run API

uvicorn main:app --host 0.0.0.0 --port 8005

# Docker Usage

docker build -t your-image-name .


docker run -d -p 8005:8005 --name your-container-name your-image-name
