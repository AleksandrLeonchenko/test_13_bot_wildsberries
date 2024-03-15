from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_PASS = os.getenv("POSTGRES_PASS")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_NAME = os.getenv("POSTGRES_NAME")

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@postgres/{POSTGRES_NAME}"
# DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@127.0.0.1/{POSTGRES_NAME}"
