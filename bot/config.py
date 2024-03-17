from dotenv import load_dotenv
import os

load_dotenv()


POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_PASS = os.environ.get("POSTGRES_PASS")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_NAME = os.environ.get("POSTGRES_NAME")

BOT_TOKEN = os.environ.get("BOT_TOKEN")
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@postgres/{POSTGRES_NAME}"
# DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@127.0.0.1/{POSTGRES_NAME}"
