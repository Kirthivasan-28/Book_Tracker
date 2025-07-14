from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os 

load_dotenv()

mongo_url = os.getenv("MONGO_URI")
db_name = os.getenv("DATABASE_NAME")

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

try:
    client.server_info()
    print("Book Tracker DB Connected Successfully!!")
except Exception as e:
    print(f"MongoDB Connection Error:{e}")
