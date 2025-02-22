import logging  

from pyrogram import Client 

from telegram.ext import Application
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger("pyrate_limiter").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

OWNER_ID = 5932230962
sudo_users = ["5932230962", "6691393517"]
GROUP_ID = -1001875834087
TOKEN = "6730555552:AAFgW2O0ULSC6cH-6wl7KgJdaM297w59bqM"
mongo_url = "mongodb+srv://vikas:vikas@vikas.yfezexk.mongodb.net/?retryWrites=true&w=majority"
PHOTO_URL = ["https://telegra.ph/file/72ea883532b722f405059.jpg", "https://telegra.ph/file/72ea883532b722f405059.jpg"]
SUPPORT_CHAT = "HEROKUFREECC"
UPDATE_CHAT = "HEROKUFREECC"
BOT_USERNAME = "AnzooBot"
CHARA_CHANNEL_ID = -1001875834087
api_id = 6435225
api_hash = "4e984ea35f854762dcde906dce426c2d"


application = Application.builder().token(TOKEN).build()
Grabberu = Client("Grabber", api_id, api_hash, bot_token=TOKEN)
client = AsyncIOMotorClient(mongo_url)
db = client['Character_catcher']
collection = db['anime_characters']
user_totals_collection = db['user_totals']
user_collection = db["user_collection"]
group_user_totals_collection = db['group_user_total']
top_global_groups_collection = db['top_global_groups']



