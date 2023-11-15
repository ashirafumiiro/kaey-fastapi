import motor.motor_asyncio
from dotenv import load_dotenv

import os

load_dotenv()
# db: motor.motor_asyncio.AsyncIOMotorDatabase = None
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client["kaey_site"]