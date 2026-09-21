import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Prefer an env var in real deployments; falls back to local Mongo for dev.
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
student_collection = db["Students"]
