import re
import os
from os import environ
from Script import script

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot Information
API_ID = int(environ.get("API_ID", ""))
API_HASH = environ.get("API_HASH", "")
BOT_TOKEN = environ.get("BOT_TOKEN", "")

PICS = (environ.get('PICS', 'https://freeimage.host/i/d10VHep')).split() # Bot Start Picture
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '5783103507').split()]
BOT_USERNAME = environ.get("BOT_USERNAME", "mrviral_bot") # without @
PORT = environ.get("PORT", "8080")

# Clone Info :-
CLONE_MODE = bool(environ.get('CLONE_MODE', False)) # Set True or False
# If Clone Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
CLONE_DB_URI = environ.get("CLONE_DB_URI", "mongodb+srv://cinamaj445:UGdvapVczr1kMEkF@cluster0.zik1uzr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
CDB_NAME = environ.get("CDB_NAME", "Cluster0")

# Database Information
DB_URI = environ.get("DB_URI", "mongodb+srv://cinamaj445:UGdvapVczr1kMEkF@cluster0.zik1uzr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = environ.get("DB_NAME", "Cluster0")

# Auto Delete Information
AUTO_DELETE_MODE = bool(environ.get('AUTO_DELETE_MODE', True)) # Set True or False

# If Auto Delete Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
AUTO_DELETE = int(environ.get("AUTO_DELETE", "2")) # Time in Minutes
AUTO_DELETE_TIME = int(environ.get("AUTO_DELETE_TIME", "120")) # Time in Seconds

# dedicated database channel's chat id for storing file data
# Replace with your dedicated database channel's chat id
DB_CHANNEL = int(environ.get("DB_CHANNEL", "-1002818707579"))

# Bot uptime information and stats are shown reply add by tactition
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
AUTH_CHANNEL = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('AUTH_CHANNEL', '-1002685689132').split()]
USER_REPLY_TEXT = "❌Don't send me messages! You Can't Use Me Unless You Have The Special Link To Access My Content."

BOT_ID = int(environ.get("BOT_ID", "7987591680")) # bot id from https://api.telegram.org/bot<YourBotToken>/getMe



# Channel Information
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", "-1002540112625"))

# File Caption Information
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CAPTION}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)

# Enable - True or Disable - False
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "False")), False)

# Verify Info :-
VERIFY_MODE = bool(environ.get('VERIFY_MODE', False)) # Set True or False

# If Verify Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
SHORTLINK_URL = environ.get("SHORTLINK_URL", "yummyurl.com") # shortlink domain without https://
SHORTLINK_API = environ.get("SHORTLINK_API", "f4e1787c1041fd077f95c6a721901f51dfebf0f6") # shortlink api
VERIFY_TUTORIAL = environ.get("VERIFY_TUTORIAL", "https://t.me/bolomotu/1378") # how to open link 

# Website Info:
WEBSITE_URL_MODE = bool(environ.get('WEBSITE_URL_MODE', False)) # Set True or False

# If Website Url Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
WEBSITE_URL = environ.get("WEBSITE_URL", "") # For More Information Check Video On Yt -

# File Stream Config
STREAM_MODE = bool(environ.get('STREAM_MODE', False)) # Set True or False

# If Stream Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
MULTI_CLIENT = True
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '00'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "40")) # in Seconds 
if 'DYNO' in environ:
    ON_HEROKU = True
else:
    ON_HEROKU = False
URL = environ.get("URL", "https://embarrassing-charisse-fsdvzcvzxv-94ddbeac.koyeb.app/")
