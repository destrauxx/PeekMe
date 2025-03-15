import os

from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = str(os.getenv("TG_TOKEN"))
YA_GPT_API = str(os.getenv("YA_GPT_API"))
YA_FOLDER_ID = str(os.getenv("YA_FOLDER_ID"))

BACKEND_API = str(os.getenv("BACKEND_API"))
