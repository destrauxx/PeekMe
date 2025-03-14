import os

from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = str(os.getenv("TG_TOKEN"))
