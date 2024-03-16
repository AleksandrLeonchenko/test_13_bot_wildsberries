from dotenv import load_dotenv
import os

load_dotenv()

# POSTGRES_HOST = os.getenv("POSTGRES_HOST")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT")
# POSTGRES_PASS = os.getenv("POSTGRES_PASS")
# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_NAME = os.getenv("POSTGRES_NAME")
#
# BOT_TOKEN = os.getenv("BOT_TOKEN")
# # DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@postgres/{POSTGRES_NAME}"
# DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@127.0.0.1/{POSTGRES_NAME}"


# POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
# POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
# POSTGRES_PASS = os.environ.get("POSTGRES_PASS")
# POSTGRES_USER = os.environ.get("POSTGRES_USER")
# POSTGRES_NAME = os.environ.get("POSTGRES_NAME")
#
# BOT_TOKEN = os.environ.get("BOT_TOKEN")
# DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@postgres/{POSTGRES_NAME}"
# # DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@127.0.0.1/{POSTGRES_NAME}"



# POSTGRES_HOST = 127.0.0.1
POSTGRES_HOST = 'postgres'
POSTGRES_PORT = 5432
POSTGRES_PASS = '55660078aA'
POSTGRES_USER = 'postgres'
POSTGRES_NAME = 'test_13_wildsberries'

BOT_TOKEN = '6335546830:AAFojQ0Jho4qTKXUnbz2AL57wfiHxPCIoBs'
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@postgres/{POSTGRES_NAME}"
# DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@127.0.0.1/{POSTGRES_NAME}"