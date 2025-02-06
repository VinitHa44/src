from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from app.config.settings import settings

class Database:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        self.client = AsyncIOMotorClient(settings.DATABASE_URL)
        self.db = self.client[settings.DATABASE_NAME]
        print("\ndatbase connected")

    async def disconnect(self):
        self.client.close()

db = Database()

@asynccontextmanager
async def lifespan(app):
    await db.connect()
    yield
    await db.disconnect()
