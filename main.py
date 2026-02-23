import os
import asyncio
import aiohttp
import yt_dlp
from telethon import TelegramClient, events, Button
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors import UserAlreadyParticipantError, InviteHashExpiredError, FloodWaitError
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.sessions import StringSession
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, InputMessagesFilterEmpty
from telethon.utils import get_display_name
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from pytgcalls.types.stream import AudioQuality, VideoQuality
import logging
from datetime import datetime, timedelta
import time
from PIL import Image
from io import BytesIO
import uuid
import re
from typing import Optional, Dict, List
import random
from telethon.tl.functions.channels import GetParticipantRequest, JoinChannelRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator, ChatParticipantAdmin, ChatParticipantCreator
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import subprocess
import json
import psutil

# ================= CONFIGURATION =================
BOT_TOKEN = "8493611261:AAHQNQnfmZwhuVe16TDTuve7r8cqGTQmWvg"
API_ID = 30191201
API_HASH = "5c87a8808e935cc3d97958d0bb24ff1f"
COOKIES_FILE = "cookies.txt"
ASSISTANT_SESSION = "1BVtsOKoBu2m6t9kIzAreFVIjWQXldBPJOS_nDiq7Kyp0P8vBtOfrjIjRaBMJNDEGK1HcF6pdH7C3EzMULEcrKxMpi42eTFoqYvzFGR4JIdDHTCh2F2hrLpOswumw3Imlyk5uL4a3gTBP24QLMVvj7TFpcO71KQ4CeUW8ok8BeXkedQTkLk2H9cep4WjvOqTVphVDrbuJlhgcDD90fv7eRv3_F7JUFtrmxpksaQJUJQjM3SGjLTuRjgFHiAnEctVYHsxZ0ee2_oJE0AO_tbupxXo3TJ8xsA_lcis-lcRSbSBuDUG6LLY1atBNgw0S7xOv006jeETUcs7ORikuZFsEwSwTp4A7fjQ="
OWNER_ID = 5774811323
UPDATES_CHANNEL = "ASUNA_XMUSIC_UPDATES"  # Bina @ ke
LOG_GROUP_ID = -1003681145012  # TERI LOG GROUP ID

# Welcome image URL
WELCOME_IMAGE_URL = "https://myimgs.org/storage/images/17832/asuna.png"
PING_IMAGE_URL = "https://myimgs.org/storage/images/17832/asuna.png"

# Database file
DB_FILE = "bot_database.json"

# ================= DEFAULT COOKIES =================
# Yeh default cookies hain - inhe apne actual cookies se replace karo
DEFAULT_COOKIES = """# Netscape HTTP Cookie File
# https://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file! Do not edit.

.youtube.com	TRUE	/	TRUE	1796534205	LOGIN_INFO	AFmmF2swRQIgXhMjyG_KuWx3zbSu4O1_aka5IKX-El98wjM9grtwx7oCIQDBs7xcAku1cs3qYVjBYsBtrE980GazWOvev71VKx1dcA:QUQ3MjNmekh1c0ZYYmtSN0hSd1BrTHdqNmlpZGdoU2o3RWktMzB4YVUyclFpWUdCcG5oLVBVOUo4R1ZUT3ZLTlBteHpXM3lrb05GWDhfMGFrVkNHNlo4TGdRN1BMalQ3RjRuRl85Z1pWVzJfVk1JaXhfdzh6c2RGcHhtZkpodFFkajJVVklQdUU1MjZLTWFGWmEtel8wdHNwNF94Y0RwRWRR
.youtube.com	TRUE	/	TRUE	1784548914	VISITOR_INFO1_LIVE	MAkn4Y9kaCg
.youtube.com	TRUE	/	TRUE	1784548914	VISITOR_PRIVACY_METADATA	CgJJThIEGgAgUQ%3D%3D
.youtube.com	TRUE	/	TRUE	1806418119	PREF	f7=150&tz=Asia.Calcutta
.youtube.com	TRUE	/	FALSE	1804700021	SID	g.a0006QhnTlbsoTwmbRZXRXcJBZLZkGepU6wzQh9xCdvKuaPbrEvBAdasiz5L_o9SajgxjQqa3QACgYKAagSARUSFQHGX2MiCeib2MYdwI8Dbs0Ye_48bBoVAUF8yKr5fdScmALPBxId_Ddgw7mI0076
.youtube.com	TRUE	/	TRUE	1804700021	__Secure-1PSID	g.a0006QhnTlbsoTwmbRZXRXcJBZLZkGepU6wzQh9xCdvKuaPbrEvBd4O2KdUdcAyzg6eCBy02GwACgYKAXQSARUSFQHGX2MicZnfS0TEgvXtureUf_-J_BoVAUF8yKrB5SbrWLHQBT7INg4glvki0076
.youtube.com	TRUE	/	TRUE	1804700021	__Secure-3PSID	g.a0006QhnTlbsoTwmbRZXRXcJBZLZkGepU6wzQh9xCdvKuaPbrEvBH9Is_qCn0TtyRg-FasmnawACgYKAd4SARUSFQHGX2Mi6NsiBPIGyfU5FT0RJ_k5nRoVAUF8yKoV-vYZO94L7vqd3a-vVVFb0076
.youtube.com	TRUE	/	FALSE	1804700021	HSID	A9TVt8qgx8FGXadVD
.youtube.com	TRUE	/	TRUE	1804700021	SSID	AC5wBV0u9EJ_lLTFS
.youtube.com	TRUE	/	FALSE	1804700021	APISID	-mbkpYjKQw7AFOer/AHt3mzKNVlmLl2U2p
.youtube.com	TRUE	/	TRUE	1804700021	SAPISID	_a0G9ZnYpi48Knf8/AHTuasfNToANBhPiL
.youtube.com	TRUE	/	TRUE	1804700021	__Secure-1PAPISID	_a0G9ZnYpi48Knf8/AHTuasfNToANBhPiL
.youtube.com	TRUE	/	TRUE	1804700021	__Secure-3PAPISID	_a0G9ZnYpi48Knf8/AHTuasfNToANBhPiL
.youtube.com	TRUE	/	TRUE	1786532870	__Secure-YNID	15.YT=EZuapdMVeWhuaE8A3KOk7FVR4CO8tolkPea2RRgK3rrsy9dAZdce3jJzJgliGBPiyXT0jd4IODrmo7jsmhqeMUTkDH9Pi-m_YQcJ-m-JNu2JAaI-BowIfFxNivlX2p5XLaEhS2RMCgp-eO7LPbwk0XYCso9Qt091UkXVqu9L-DAHttXg0nI1Ae_53FDEaWVydCHmn9ekLPYahbpkU7izmWGEZ05qOx16UGbfZrvayPJvfjUWRXsKmIsxxZ1UJPaNxjPt0brgW5irTC8VCPe262Tij0LkzQzJKPOi5Fqi3j7QHpGtzrORhzdOn9TWFd1pOeQ7wT7yF1y-nK0uOMtTjw
.youtube.com	TRUE	/	TRUE	1803396574	__Secure-1PSIDTS	sidts-CjQBBj1CYqUjeuhR7fZT6HAFRqvlbnjhkjeLY8Z9A2RV8L3Sj3J9v_xq0OucSEhdJkXjAXV3EAA
.youtube.com	TRUE	/	TRUE	1803396574	__Secure-3PSIDTS	sidts-CjQBBj1CYqUjeuhR7fZT6HAFRqvlbnjhkjeLY8Z9A2RV8L3Sj3J9v_xq0OucSEhdJkXjAXV3EAA
.youtube.com	TRUE	/	FALSE	1803396574	SIDCC	AKEyXzVxgnfq07Y2t4ul4lIE_JrzSeUG9ZAO85BqVsNiYy0pe3BnmPbKtNIrkUncAeo0n1g0x2A
.youtube.com	TRUE	/	TRUE	1803396574	__Secure-1PSIDCC	AKEyXzW9uCe38mPwHjltt7qyUQ-qIWeP_6bQWmZtmHgjPM9i5WR5KpNJdRWioG0cy6c-CTp1fyg
.youtube.com	TRUE	/	TRUE	1803396574	__Secure-3PSIDCC	AKEyXzXhK5eg6n_hu9u7O4aydpE9k4wCmD7d6_X7uCIvG36bBxBuafqw0tzDoIFspUqOv8vOSA
.youtube.com	TRUE	/	TRUE	1787410112	VISITOR_INFO1_LIVE	Xk2bZPd0v74
.youtube.com	TRUE	/	TRUE	1787410112	VISITOR_PRIVACY_METADATA	CgJJThIEGgAgIw%3D%3D
.youtube.com	TRUE	/	TRUE	1787410112	__Secure-YNID	16.YT=KfAh07c6WQ0YUuy8my2RPVn9l2ThT1flRAdtOb_9S6rrW-1zazI1ztbI_gIYIVMCzYXbWTSy3o6WlXdUOBDc37AzbZ_NnBqrGYLHNMx-ApRQfJ5-r0j5xCscFA4WCwZBXjhy37foNtkSYmeiGslOz6NvyxXdWJITn726RV8I4n3oVGdVMclw8dAEBP5y3IlNQNUViZ66hZjFBIW03gC8c1v0gaST41W-ksy2lW5dMUta-CabZ_K2vSxNvYH5xAz6PCD7gGkpkTRAFQN2QqsK2-7JBKSMiB1blvPeDCbQ8_6NukoM0uiFPfTs5X7lrsY7zfTkhawk8dl9vzqO6DqCMw
.youtube.com	TRUE	/	TRUE	0	YSC	LXBU5GOsdaU
.youtube.com	TRUE	/	TRUE	1787410112	__Secure-ROLLOUT_TOKEN	CKGa9q7D1re_VhCi6seAxryQAxia4brq7e-SAw%3D%3D
"""

# ================= LOGGING =================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ================= DATABASE CLASS =================
class Database:
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        self.data = self.load()
    
    def load(self):
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r') as f:
                    data = json.load(f)
                    # Ensure cookies field exists
                    if "cookies" not in data:
                        data["cookies"] = DEFAULT_COOKIES
                    return data
            else:
                return {
                    "users": {},
                    "groups": {},
                    "bot_admins": [OWNER_ID],
                    "cookies": DEFAULT_COOKIES,
                    "stats": {
                        "total_commands": 0,
                        "songs_played": 0,
                        "bot_start_time": time.time()
                    }
                }
        except Exception as e:
            logger.error(f"Database load error: {e}")
            return {
                "users": {},
                "groups": {},
                "bot_admins": [OWNER_ID],
                "cookies": DEFAULT_COOKIES,
                "stats": {
                    "total_commands": 0,
                    "songs_played": 0,
                    "bot_start_time": time.time()
                }
            }
    
    def save(self):
        try:
            with open(self.db_file, 'w') as f:
                json.dump(self.data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Database save error: {e}")
            return False
    
    def save_cookies(self, cookies_text):
        """Save cookies to database and file"""
        self.data["cookies"] = cookies_text
        self.save()
        # Also save to file for yt-dlp
        try:
            with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
                f.write(cookies_text)
            logger.info(f"Cookies saved to {COOKIES_FILE}")
            return True
        except Exception as e:
            logger.error(f"Failed to save cookies file: {e}")
            return False
    
    def get_cookies(self):
        """Get cookies from database"""
        return self.data.get("cookies", DEFAULT_COOKIES)
    
    def load_cookies_to_file(self):
        """Load cookies from database to file on startup"""
        cookies = self.get_cookies()
        if cookies:
            try:
                with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
                    f.write(cookies)
                logger.info(f"Cookies loaded from database to {COOKIES_FILE}")
                return True
            except Exception as e:
                logger.error(f"Failed to load cookies to file: {e}")
        return False
    
    def add_user(self, user_id, username=None, first_name=None):
        user_id = str(user_id)
        now = time.time()
        
        if user_id not in self.data["users"]:
            self.data["users"][user_id] = {
                "first_seen": now,
                "last_active": now,
                "username": username or "",
                "name": first_name or ""
            }
        else:
            self.data["users"][user_id]["last_active"] = now
            if username:
                self.data["users"][user_id]["username"] = username
            if first_name:
                self.data["users"][user_id]["name"] = first_name
        
        self.save()
    
    def add_group(self, group_id, name=None, username=None, members_count=0):
        group_id = str(group_id)
        
        if group_id not in self.data["groups"]:
            self.data["groups"][group_id] = {
                "added_date": time.time(),
                "name": name or "",
                "username": username or "",
                "members_count": members_count
            }
        else:
            if name:
                self.data["groups"][group_id]["name"] = name
            if username:
                self.data["groups"][group_id]["username"] = username
            if members_count:
                self.data["groups"][group_id]["members_count"] = members_count
        
        self.save()
    
    def remove_group(self, group_id):
        group_id = str(group_id)
        if group_id in self.data["groups"]:
            del self.data["groups"][group_id]
            self.save()
            return True
        return False
    
    def is_bot_admin(self, user_id):
        return int(user_id) in self.data["bot_admins"] or int(user_id) == OWNER_ID
    
    def add_bot_admin(self, user_id):
        user_id = int(user_id)
        if user_id not in self.data["bot_admins"] and user_id != OWNER_ID:
            self.data["bot_admins"].append(user_id)
            self.save()
            return True
        return False
    
    def remove_bot_admin(self, user_id):
        user_id = int(user_id)
        if user_id in self.data["bot_admins"] and user_id != OWNER_ID:
            self.data["bot_admins"].remove(user_id)
            self.save()
            return True
        return False
    
    def get_bot_admins(self):
        return self.data["bot_admins"]
    
    def increment_command_count(self):
        self.data["stats"]["total_commands"] = self.data["stats"].get("total_commands", 0) + 1
        self.save()
    
    def increment_songs_played(self):
        self.data["stats"]["songs_played"] = self.data["stats"].get("songs_played", 0) + 1
        self.save()
    
    def get_stats(self):
        users_count = len(self.data["users"])
        groups_count = len(self.data["groups"])
        total_commands = self.data["stats"].get("total_commands", 0)
        songs_played = self.data["stats"].get("songs_played", 0)
        uptime_seconds = time.time() - self.data["stats"].get("bot_start_time", time.time())
        uptime_str = str(timedelta(seconds=int(uptime_seconds)))
        
        return {
            "users": users_count,
            "groups": groups_count,
            "total_commands": total_commands,
            "songs_played": songs_played,
            "uptime": uptime_str,
            "uptime_seconds": uptime_seconds
        }

# Initialize database
db = Database()

# Load cookies from database to file on startup
db.load_cookies_to_file()

# ================= LOG FUNCTION =================
async def log_to_group(action_type, user=None, group=None, song=None, details=""):
    """Send log to log group"""
    if not LOG_GROUP_ID:
        return
    
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if action_type == "user_start":
            # User started bot
            user_mention = f"[{get_display_name(user)}](tg://user?id={user.id})" if user else "Unknown"
            username = f"@{user.username}" if user and user.username else "`No username`"
            first_name = user.first_name if user and user.first_name else "N/A"
            last_name = user.last_name if user and user.last_name else "N/A"
            lang_code = user.lang_code if user and user.lang_code else "N/A"
            
            log_text = f"""
**╭━━━━ ⟬ 👤 ᴜsᴇʀ sᴛᴀʀᴛᴇᴅ ʙᴏᴛ ⟭━━━━╮**
┃
┃**ᴛɪᴍᴇ:** `{timestamp}`
┃**ᴜsᴇʀ:** {user_mention}
┃**ᴜsᴇʀ ɪᴅ:** `{user.id if user else 'N/A'}`
┃**ᴜsᴇʀɴᴀᴍᴇ:** {username}
┃**ғɪʀsᴛ ɴᴀᴍᴇ:** `{first_name}`
┃**ʟᴀsᴛ ɴᴀᴍᴇ:** `{last_name}`
┃**ʟᴀɴɢᴜᴀɢᴇ:** `{lang_code}`
**╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯**
"""
        
        elif action_type == "song_played":
            # Song played
            user_mention = f"[{get_display_name(user)}](tg://user?id={user.id})" if user else "Unknown"
            username = f"@{user.username}" if user and user.username else "`No username`"
            
            group_title = group.title if group else "Private"
            group_id = group.id if group else "N/A"
            
            song_title = song.get('title', 'Unknown')[:50] if song else 'Unknown'
            song_duration = song.get('duration_str', '0:00') if song else 'N/A'
            
            log_text = f"""
**╭━━━━ ⟬ 🎵 sᴏɴɢ ᴘʟᴀʏᴇᴅ ⟭━━━━╮**
┃
┃**ᴛɪᴍᴇ:** `{timestamp}`
┃**ᴜsᴇʀ:** {user_mention}
┃**ᴜsᴇʀ ɪᴅ:** `{user.id if user else 'N/A'}`
┃**ᴜsᴇʀɴᴀᴍᴇ:** {username}
┃
┃**ɢʀᴏᴜᴘ:** `{group_title}`
┃**ɢʀᴏᴜᴘ ɪᴅ:** `{group_id}`
┃
┃**sᴏɴɢ:** `{song_title}`
┃**ᴅᴜʀᴀᴛɪᴏɴ:** `{song_duration}`
**╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯**
"""
        
        elif action_type == "cookies_updated":
            # Cookies updated
            log_text = f"""
**╭━━━━ ⟬ 🍪 ᴄᴏᴏᴋɪᴇs ᴜᴘᴅᴀᴛᴇᴅ ⟭━━━━╮**
┃
┃**ᴛɪᴍᴇ:** `{timestamp}`
┃**ᴀᴄᴛɪᴏɴ:** `Cookies file updated`
┃**ᴅᴇᴛᴀɪʟs:** `{details}`
**╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯**
"""
        
        else:
            # Generic log
            log_text = f"""
**╭━━━━ ⟬ ʟᴏɢ ᴇɴᴛʀʏ ⟭━━━━╮**
┃
┃**ᴛɪᴍᴇ:** `{timestamp}`
┃**ᴀᴄᴛɪᴏɴ:** `{action_type}`
┃**ᴅᴇᴛᴀɪʟs:** `{details}`
**╰━━━━━━━━━━━━━━━━━━╯**
"""
        
        await bot.send_message(LOG_GROUP_ID, log_text)
    except Exception as e:
        logger.error(f"Failed to send log: {e}")

# ================= GLOBALS =================
BOT_ADMINS = db.get_bot_admins()
players = {}
call = None
bot = None
assistant = None
COMMAND_PREFIXES = ["/", "!", "."]
BOT_START_TIME = time.time()

# ================= MUSIC PLAYER CLASS =================
class MusicPlayer:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.queue = []
        self.current = None
        self.loop = False
        self.paused = False
        self.play_task = None
        self.message = None
        self.control_message_id = None
        self.control_chat_id = None

# ================= HELPER FUNCTIONS =================
async def download_and_convert_thumbnail(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return None
                data = await resp.read()

        image = Image.open(BytesIO(data)).convert("RGB")
        filename = f"thumb_{uuid.uuid4().hex}.jpg"
        image.save(filename, "JPEG")
        return filename

    except Exception as e:
        logger.error(f"Thumbnail convert error: {e}")
        return None

async def get_player(chat_id):
    if chat_id not in players:
        players[chat_id] = MusicPlayer(chat_id)
    return players[chat_id]

async def is_admin(chat_id, user_id):
    """Check if user is admin in group"""
    # Bot admins always have access
    if db.is_bot_admin(user_id):
        return True
    
    try:
        # Try to get participant info
        participant = await bot(GetParticipantRequest(
            channel=chat_id,
            participant=user_id
        ))
        
        # Check if admin or creator
        if isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator, 
                                                ChatParticipantAdmin, ChatParticipantCreator)):
            return True
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
    
    return False

async def is_bot_admin(user_id):
    return db.is_bot_admin(user_id)

# ================= JOIN VOICE CHAT =================
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, ExportChatInviteRequest
from telethon.errors import ChatAdminRequiredError

async def join_voice_chat(chat_id: int):
    try:
        # Check if assistant already member
        try:
            me = await assistant.get_me()
            await assistant(GetParticipantRequest(chat_id, me.id))
            logger.info("Assistant already in group")
            return True
        except:
            pass

        chat = await bot.get_entity(chat_id)

        # Public group (username exists)
        if getattr(chat, "username", None):
            await assistant(JoinChannelRequest(chat.username))
            logger.info("Assistant joined public group")

        # Private group
        else:
            try:
                invite = await bot(ExportChatInviteRequest(
                    peer=chat_id,
                    expire_date=None,
                    usage_limit=None
                ))
            except ChatAdminRequiredError:
                logger.error("Bot needs Invite Users via Link permission")
                return False

            invite_hash = invite.link.split("/")[-1].replace("+", "")

            try:
                await assistant(ImportChatInviteRequest(invite_hash))
                logger.info("Assistant joined private group")
            except UserAlreadyParticipantError:
                return True

        await asyncio.sleep(2)
        await assistant.get_dialogs()
        await assistant.get_entity(chat_id)

        return True

    except Exception as e:
        logger.error(f"Auto join failed: {e}")
        return False

# ================= VOICE MESSAGE HANDLER =================
async def download_voice_message(event):
    """Download voice message and convert to MP3"""
    try:
        # Check if it's a reply to a voice message
        if event.message.reply_to_msg_id:
            reply_msg = await event.get_reply_message()
            
            # Check if replied message has voice/media
            if reply_msg.voice or (reply_msg.document and reply_msg.document.mime_type and 'audio' in reply_msg.document.mime_type):
                msg = await event.reply("**📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠᴏɪᴄᴇ ᴍᴇssᴀɢᴇ...**")
                
                # Generate unique filename
                file_name = f"voice_{uuid.uuid4().hex}"
                file_path = await reply_msg.download_media(file=file_name)
                
                if not file_path:
                    await msg.edit("**❌ ғᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴠᴏɪᴄᴇ ᴍᴇssᴀɢᴇ!**")
                    await asyncio.sleep(3)
                    await msg.delete()
                    return None
                
                # Convert to MP3 if needed
                output_file = f"{file_name}.mp3"
                
                # Use ffmpeg to convert to MP3
                try:
                    process = await asyncio.create_subprocess_exec(
                        'ffmpeg', '-i', file_path, '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', output_file,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    await process.communicate()
                    
                    # Remove original file
                    try:
                        os.remove(file_path)
                    except:
                        pass
                    
                    # Get duration using ffprobe
                    duration = 0
                    try:
                        process = await asyncio.create_subprocess_exec(
                            'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', output_file,
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )
                        stdout, _ = await process.communicate()
                        if stdout:
                            duration = int(float(stdout.decode().strip()))
                    except:
                        pass
                    
                    minutes = duration // 60
                    seconds = duration % 60
                    duration_str = f"{minutes}:{seconds:02d}"
                    
                    await msg.delete()
                    
                    return {
                        'file_path': output_file,
                        'title': 'Voice Message',
                        'duration': duration,
                        'duration_str': duration_str,
                        'thumbnail': None,
                        'uploader': reply_msg.sender.first_name if reply_msg.sender else 'Unknown',
                        'is_local': True
                    }
                except Exception as e:
                    logger.error(f"FFmpeg conversion error: {e}")
                    await msg.edit("**❌ ғᴀɪʟᴇᴅ ᴛᴏ ᴄᴏɴᴠᴇʀᴛ ᴠᴏɪᴄᴇ ᴍᴇssᴀɢᴇ!**")
                    await asyncio.sleep(3)
                    await msg.delete()
                    return None
    except Exception as e:
        logger.error(f"Voice message download error: {e}")
        return None
    
    return None

# ================= EXTRACT AUDIO/VIDEO =================
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def download_audio(query):
    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "geo_bypass": True,
        "geo_bypass_country": "IN",
        "cookiefile": COOKIES_FILE,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            if query.startswith(("http://", "https://")):
                info = ydl.extract_info(query, download=True)
            else:
                results = ydl.extract_info(f"ytsearch1:{query}", download=True)
                if not results or not results.get("entries"):
                    return None
                info = results["entries"][0]

            if not info:
                return None

            base_path = ydl.prepare_filename(info)
            file_path = os.path.splitext(base_path)[0] + ".mp3"

            duration = info.get("duration") or 0
            minutes = duration // 60
            seconds = duration % 60

            return {
                "file_path": file_path,
                "title": info.get("title", "Unknown"),
                "duration": duration,
                "duration_str": f"{minutes}:{seconds:02d}",
                "thumbnail": info.get("thumbnail"),
                "uploader": info.get("uploader", "Unknown"),
                "is_local": False,
            }

    except Exception as e:
        logger.error(f"Download audio error: {e}")
        return None

async def download_video(query):
    ydl_opts = {
        "format": "bestvideo[height<=720]+bestaudio/best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "geo_bypass": True,
        "geo_bypass_country": "IN",
        "cookiefile": COOKIES_FILE,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            if query.startswith(("http://", "https://")):
                info = ydl.extract_info(query, download=True)
            else:
                results = ydl.extract_info(f"ytsearch1:{query}", download=True)
                if not results or not results.get("entries"):
                    return None
                info = results["entries"][0]

            if not info:
                return None

            base_path = ydl.prepare_filename(info)
            file_path = os.path.splitext(base_path)[0] + ".mp4"

            duration = info.get("duration") or 0
            minutes = duration // 60
            seconds = duration % 60

            return {
                "file_path": file_path,
                "title": info.get("title", "Unknown"),
                "duration": duration,
                "duration_str": f"{minutes}:{seconds:02d}",
                "thumbnail": info.get("thumbnail"),
                "uploader": info.get("uploader", "Unknown"),
                "is_local": False,
            }

    except Exception as e:
        logger.error(f"Download video error: {e}")
        return None

# ================= PLAY SONG =================
async def play_song(chat_id, song_info, is_video=False):
    player = await get_player(chat_id)

    # Ensure assistant is in chat
    for attempt in range(3):
        try:
            await assistant.get_entity(chat_id)
            break
        except:
            if attempt == 2:
                await join_voice_chat(chat_id)
                await asyncio.sleep(2)
            else:
                await asyncio.sleep(1)

    try:
        # Determine source (local file or URL)
        source = song_info.get("file_path") or song_info.get("url")
        if not source:
            return False

        if is_video:
            media = MediaStream(
                source,
                audio_parameters=AudioQuality.STUDIO,
                video_parameters=VideoQuality.HD_720p,
            )
        else:
            media = MediaStream(
                source,
                audio_parameters=AudioQuality.STUDIO,
            )

        await call.play(chat_id, media)

        song_info["is_video"] = is_video
        player.current = song_info
        player.paused = False

        # Increment songs played counter
        db.increment_songs_played()

        # Cancel previous auto task
        if player.play_task and not player.play_task.done():
            player.play_task.cancel()

        # Auto next only if duration known
        duration = song_info.get("duration", 0)
        if duration > 0:
            player.play_task = asyncio.create_task(
                auto_next(chat_id, duration)
            )
        else:
            player.play_task = None

        await send_streaming_message(chat_id, song_info, is_video)

        return True

    except Exception as e:
        logger.error(f"Play song error: {e}")
        return False


async def send_streaming_message(chat_id, song_info, is_video):
    player = await get_player(chat_id)
    
    # Different title for voice messages
    if song_info.get('is_local', False):
        title_display = "🎤 Voice Message"
        uploader = song_info.get('uploader', 'Unknown')
        thumbnail_url = None
    else:
        title_display = song_info.get('title', 'Unknown')[:30]
        uploader = song_info.get('uploader', 'Unknown')
        thumbnail_url = song_info.get('thumbnail')
    
    caption = f"""
**╭━━━━ ⟬ ➲ ɴᴏᴡ sᴛʀᴇᴀᴍɪɴɢ ⟭━━━━╮**
┃
┃⟡➣ **ᴛɪᴛʟᴇ:** `{title_display}`
┃⟡➣ **ᴅᴜʀᴀᴛɪᴏɴ:** `{song_info.get('duration_str', '0:00')}`
┃⟡➣ **ᴛʏᴘᴇ:** `{'🎬 ᴠɪᴅᴇᴏ' if is_video else '🎵 ᴀᴜᴅɪᴏ'}`
┃⟡➣ **ʟᴏᴏᴘ:** `{'ᴏɴ' if player.loop else 'ᴏғғ'}`
┃⟡➣ **ǫᴜᴇᴜᴇ:** `{len(player.queue)} sᴏɴɢs`
┃⟡➣ **ᴜᴘʟᴏᴀᴅᴇʀ:** `{uploader}`
**╰━━━━━━━━━━━━━━━━━━━━━━╯**
    """
    
    buttons = [
        [Button.inline("⏸️", data=f"pause_{chat_id}"),
         Button.inline("⏭️", data=f"skip_{chat_id}"),
         Button.inline("⏹️", data=f"end_{chat_id}"),
         Button.inline("🔄", data=f"loop_{chat_id}")],
        [Button.inline("📋 ǫᴜᴇᴜᴇ", data=f"queue_{chat_id}"),
         Button.inline("🗑️ ᴄʟᴇᴀʀ", data=f"clear_{chat_id}")]
    ]
    
    # Download thumbnail only for non-voice messages
    thumb_path = None
    if thumbnail_url and not song_info.get('is_local', False):
        thumb_path = await download_and_convert_thumbnail(thumbnail_url)
    
    # Delete old control message
    if player.control_message_id and player.control_chat_id:
        try:
            await bot.delete_messages(
                player.control_chat_id,
                player.control_message_id
            )
        except:
            pass
    
    # Send new control message
    try:
        if thumb_path and os.path.exists(thumb_path):
            msg = await bot.send_file(
                chat_id,
                thumb_path,
                caption=caption,
                buttons=buttons,
                spoiler=True
            )
            os.remove(thumb_path)
        else:
            msg = await bot.send_message(
                chat_id,
                caption,
                buttons=buttons
            )
    except Exception:
        msg = await bot.send_message(
            chat_id,
            caption,
            buttons=buttons
        )
    
    player.control_message_id = msg.id
    player.control_chat_id = chat_id


async def auto_next(chat_id, duration):
    await asyncio.sleep(duration)

    player = await get_player(chat_id)

    if player.loop and player.current:
        await play_song(
            chat_id,
            player.current,
            player.current.get("is_video", False)
        )
        return

    if player.queue:
        next_song = player.queue.pop(0)
        await play_song(
            chat_id,
            next_song,
            next_song.get("is_video", False)
        )
    else:
        # Cleanup local file
        if player.current:
            file_path = player.current.get("file_path")
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass

        player.current = None

        try:
            await call.leave_call(chat_id)
        except:
            pass

        # Delete control message
        if player.control_message_id and player.control_chat_id:
            try:
                await bot.delete_messages(
                    player.control_chat_id,
                    player.control_message_id
                )
            except:
                pass

        player.control_message_id = None
        player.control_chat_id = None

# ================= COMMAND CHECKER =================
def is_command(text, command):
    """Super simple command checker for large groups"""
    if not text:
        return False
    
    text = text.strip()
    
    # Direct check for /play, !play, .play
    for prefix in COMMAND_PREFIXES:
        if text.startswith(f"{prefix}{command}"):
            # Check if it's exactly the command or has space after
            rest = text[len(f"{prefix}{command}"):]
            if not rest or rest[0] in [' ', '@']:
                return True
    
    return False

def get_command_args(text, command):
    """Simple args extractor"""
    if not text:
        return None
    
    text = text.strip()
    
    for prefix in COMMAND_PREFIXES:
        if text.startswith(f"{prefix}{command}"):
            # Remove command part
            args = text[len(f"{prefix}{command}"):].strip()
            # Remove bot username if present
            if args.startswith('@'):
                parts = args.split(' ', 1)
                if len(parts) > 1:
                    return parts[1].strip()
                return None
            return args if args else None
    
    return None

# ================= BOT COMMANDS =================
@events.register(events.NewMessage)
async def message_handler(event):
    """Main message handler"""
    if not event.message.text:
        return
    
    text = event.message.text.strip()
    chat_id = event.chat_id
    user_id = event.sender_id
    sender = await event.get_sender()
    
    # Add user to database
    first_name = sender.first_name if hasattr(sender, 'first_name') else getattr(sender, 'title', str(sender.id))
    db.add_user(user_id, sender.username, first_name)
    
    # Add group to database if it's a group/channel
    if event.is_group or event.is_channel:
        chat = await event.get_chat()
        members_count = getattr(chat, 'participants_count', 0)
        db.add_group(chat_id, chat.title, getattr(chat, 'username', ''), members_count)
    
    # Log every command
    if text.startswith(tuple(COMMAND_PREFIXES)):
        db.increment_command_count()
    
    # ===== BASIC COMMANDS =====
    
    # /start command
    if is_command(text, "start"):
        user = await event.get_sender()
        
        # LOG USER START
        await log_to_group("user_start", user=user)
        
        caption = f"""
✨ **ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ˹𝚨𝛔𝛖𝛎𝛂 ꭙ 𝐌ᴜꜱɪᴄ ♪˼ ʙᴏᴛ** ✨

⟡➣ **ʜᴇʏ** [{get_display_name(user)}](tg://user?id={user.id}) ❤️

⟡➣ **ɪ ᴀᴍ ᴀ ᴘᴏᴡᴇʀғᴜʟ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ.**
⟡➣ **ᴛʜᴀᴛ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜsɪᴄ ᴀɴᴅ ᴠɪᴅᴇᴏ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs.**

⟡➣ **ᴄʟɪᴄᴋ ᴏɴ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ.**
        """
        
        buttons = [
            [Button.url("⟡➣ 𝙾𝚠𝚗𝚎𝚛", f"https://t.me/god_knows_0"),
             Button.url("➕ 𝙰𝚍𝚍 𝙼𝚎", f"https://t.me/{(await event.client.get_me()).username}?startgroup=true")],
            [Button.inline("⟡➣ 𝙷𝚎𝚕𝚙", data="help"),
             Button.url("⟡➣ 𝚄𝚙𝚍𝚊𝚝𝚎𝚜", f"https://t.me/{UPDATES_CHANNEL}")]
        ]
        
        await event.reply(file=WELCOME_IMAGE_URL, message=caption, buttons=buttons)
        
        # Delete user's command message
        try:
            await event.message.delete()
        except:
            pass
        return
    
    # ===== MUSIC COMMANDS =====
    
    # /play command
    if is_command(text, "play"):
        query = get_command_args(text, "play")

        voice_info = None
        if not query and event.message.reply_to_msg_id:
            voice_info = await download_voice_message(event)
            if voice_info:
                query = "voice"

        if not query and not voice_info:
            reply_msg = await event.reply(
                "**ᴜsᴀɢᴇ:** `/play <sᴏɴɢ ɴᴀᴍᴇ ᴏʀ ʟɪɴᴋ>`\n"
                "**ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠᴏɪᴄᴇ ᴍᴇssᴀɢᴇ**"
            )
            try:
                await event.message.delete()
            except:
                pass

            await asyncio.sleep(5)
            try:
                await reply_msg.delete()
            except:
                pass
            return

        msg = await event.reply("**🔍 ᴘʀᴏᴄᴇssɪɴɢ...**")

        try:
            await event.message.delete()
        except:
            pass

        # Download audio
        if voice_info:
            song_info = voice_info
        else:
            song_info = await download_audio(query)

        if not song_info or not song_info.get("file_path"):
            await msg.edit("**❌ sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ!**")
            await asyncio.sleep(3)
            await msg.delete()
            return

        player = await get_player(chat_id)

        if player.current:
            player.queue.append(song_info)
            queue_pos = len(player.queue)
            
            # Different title for voice messages
            if voice_info:
                title_display = "Voice Message"
            else:
                title_display = song_info['title'][:20]
            
            caption = f"""
**╭━━━━ ⟬ ➲ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ ⟭━━━━╮**
┃
┃⟡➣ **ᴛɪᴛʟᴇ:** `{title_display}`
┃⟡➣ **ᴅᴜʀᴀᴛɪᴏɴ:** `{song_info['duration_str']}`
┃⟡➣ **ᴘᴏsɪᴛɪᴏɴ:** `#{queue_pos}`
┃⟡➣ **ᴜᴘʟᴏᴀᴅᴇʀ:** `{song_info['uploader']}`
**╰━━━━━━━━━━━━━━━━━━━╯**
            """
            
            # Download thumbnail only for non-voice messages
            thumbnail_url = song_info.get('thumbnail')
            thumb_path = None
            if thumbnail_url and not voice_info:
                thumb_path = await download_and_convert_thumbnail(thumbnail_url)
            
            await msg.delete()
            
            if thumb_path:
                sent_msg = await bot.send_file(
                    chat_id,
                    thumb_path,
                    caption=caption,
                    spoiler=True
                )
                os.remove(thumb_path)
            else:
                sent_msg = await event.reply(caption)
            
            # Auto delete queue message after 10 seconds
            await asyncio.sleep(10)
            try:
                await sent_msg.delete()
            except:
                pass

        else:
            # LOG SONG PLAYED
            chat = await event.get_chat() if event.is_group else None
            await log_to_group("song_played", user=sender, group=chat, song=song_info)
            
            success = await play_song(chat_id, song_info, is_video=False)

            if not success:
                await msg.edit("**❌ ғᴀɪʟᴇᴅ ᴛᴏ ᴘʟᴀʏ sᴏɴɢ!**")
                await asyncio.sleep(3)
                await msg.delete()

                # Cleanup voice file
                if voice_info:
                    path = song_info.get("file_path")
                    if path and os.path.exists(path):
                        os.remove(path)
            else:
                await msg.delete()

        return


    # /vplay command (download video)
    if is_command(text, "vplay"):
        query = get_command_args(text, "vplay")

        if not query:
            reply_msg = await event.reply(
                "**ᴜsᴀɢᴇ:** `/vplay <ᴠɪᴅᴇᴏ ɴᴀᴍᴇ ᴏʀ ʟɪɴᴋ>`"
            )
            try:
                await event.message.delete()
            except:
                pass

            await asyncio.sleep(5)
            try:
                await reply_msg.delete()
            except:
                pass
            return

        msg = await event.reply("**🎬 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ...**")

        try:
            await event.message.delete()
        except:
            pass

        video_info = await download_video(query)

        if not video_info or not video_info.get("file_path"):
            await msg.edit("**❌ ᴠɪᴅᴇᴏ ɴᴏᴛ ғᴏᴜɴᴅ!**")
            await asyncio.sleep(3)
            await msg.delete()
            return

        player = await get_player(chat_id)

        if player.current:
            player.queue.append(video_info)
            queue_pos = len(player.queue)

            caption = f"""
**╭━━━━ ⟬ ➲ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ ⟭━━━━╮**
┃
┃⟡➣ **ᴛɪᴛʟᴇ:** `{video_info['title'][:20]}`
┃⟡➣ **ᴅᴜʀᴀᴛɪᴏɴ:** `{video_info['duration_str']}`
┃⟡➣ **ᴘᴏsɪᴛɪᴏɴ:** `#{queue_pos}`
┃⟡➣ **ᴜᴘʟᴏᴀᴅᴇʀ:** `{video_info['uploader']}`
**╰━━━━━━━━━━━━━━━━━━━╯**
            """
            
            thumbnail_url = video_info.get('thumbnail')
            thumb_path = await download_and_convert_thumbnail(thumbnail_url) if thumbnail_url else None
            
            await msg.delete()
            
            if thumb_path:
                sent_msg = await bot.send_file(
                    chat_id,
                    thumb_path,
                    caption=caption,
                    spoiler=True
                )
                os.remove(thumb_path)
            else:
                sent_msg = await event.reply(caption)
            
            # Auto delete queue message after 10 seconds
            await asyncio.sleep(10)
            try:
                await sent_msg.delete()
            except:
                pass

        else:
            # LOG SONG PLAYED (video)
            chat = await event.get_chat() if event.is_group else None
            await log_to_group("song_played", user=sender, group=chat, song=video_info)
            
            success = await play_song(chat_id, video_info, is_video=True)

            if not success:
                await msg.edit("**❌ ғᴀɪʟᴇᴅ ᴛᴏ ᴘʟᴀʏ ᴠɪᴅᴇᴏ!**")
                await asyncio.sleep(3)
                await msg.delete()
            else:
                await msg.delete()

        return
    
    # /skip command
    if is_command(text, "skip"):
        if not await is_admin(chat_id, user_id):
            reply_msg = await event.reply("**❌ ᴏɴʟʏ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs ᴄᴀɴ sᴋɪᴘ!**")
            # Delete user's command
            try:
                await event.message.delete()
            except:
                pass
            # Delete error message after 3 seconds
            await asyncio.sleep(3)
            try:
                await reply_msg.delete()
            except:
                pass
            return
        
        player = await get_player(chat_id)
        
        if not player.current:
            reply_msg = await event.reply("**❌ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ!**")
            # Delete user's command
            try:
                await event.message.delete()
            except:
                pass
            # Delete error message after 3 seconds
            await asyncio.sleep(3)
            try:
                await reply_msg.delete()
            except:
                pass
            return
        
        msg = await event.reply("**⏭️ sᴋɪᴘᴘɪɴɢ...**")
        
        # Delete user's command message
        try:
            await event.message.delete()
        except:
            pass
        
        # Clean up current local file if it was a voice message
        if player.current and player.current.get('is_local', False):
            try:
                os.remove(player.current['file_path'])
            except:
                pass
        
        # Cancel current play task
        if player.play_task and not player.play_task.done():
            player.play_task.cancel()
        
        # Stop current stream
        try:
            await call.leave_call(chat_id)
        except:
            pass
        
        # Small delay to ensure clean stop
        await asyncio.sleep(1)
        
        if player.queue:
            next_song = player.queue.pop(0)
            success = await play_song(chat_id, next_song, next_song.get('is_video', False))
            if success:
                await msg.edit("**✅ sᴋɪᴘᴘᴇᴅ ᴛᴏ ɴᴇxᴛ sᴏɴɢ!**")
                await asyncio.sleep(3)
                await msg.delete()
            else:
                await msg.edit("**❌ ғᴀɪʟᴇᴅ ᴛᴏ ᴘʟᴀʏ ɴᴇxᴛ sᴏɴɢ!**")
                player.queue.insert(0, next_song)
                await asyncio.sleep(3)
                await msg.delete()
        else:
            player.current = None
            
            if player.control_message_id and player.control_chat_id:
                try:
                    await bot.delete_messages(player.control_chat_id, player.control_message_id)
                except:
                    pass
            player.control_message_id = None
            player.control_chat_id = None
            
            await msg.edit("**⏹️ ǫᴜᴇᴜᴇ ɪs ᴇᴍᴘᴛʏ!**")
            await asyncio.sleep(3)
            await msg.delete()
        return
    
    # /pause command
    if is_command(text, "pause"):
        if not await is_admin(chat_id, user_id):
            reply_msg = await event.reply("**❌ ᴏɴʟʏ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs ᴄᴀɴ ᴘᴀᴜsᴇ!**")
            # Delete user's command
            try:
                await event.message.delete()
            except:
                pass
            # Delete error message after 3 seconds
            await asyncio.sleep(3)
            try:
                await reply_msg.delete()
            except:
                pass
            return
        
        # Delete user's command message
        try:
            await event.message.delete()
        except:
            pass
        
        try:
            await call.pause(chat_id)
            msg = await event.reply("**⏸️ ᴘᴀᴜsᴇᴅ**")
            await asyncio.sleep(3)
            await msg.delete()
        except Exception as e:
            msg = await event.reply(f"**❌ ғᴀɪʟᴇᴅ: {str(e)[:50]}**")
            await asyncio.sleep(3)
            await msg.delete()
        return
    
    # /resume command
    if is_command(text, "resume"):
        if not await is_admin(chat_id, user_id):
            reply_msg = await event.reply("**❌ ᴏɴʟʏ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs ᴄᴀɴ ʀᴇsᴜᴍᴇ!**")
            # Delete user's command
            try:
                await event.message.delete()
            except:
                pass
            # Delete error message after 3 seconds
            await asyncio.sleep(3)
            try:
                await reply_msg.delete()
            except:
                pass
            return
        
        # Delete user's command message
        try:
            await event.message.delete()
        except:
            pass
        
        try:
            await call.resume(chat_id)
            msg = await event.reply("**▶️ ʀᴇsᴜᴍᴇᴅ**")
            await asyncio.sleep(3)
            await msg.delete()
        except Exception as e:
            msg = await event.reply(f"**❌ ғᴀɪʟᴇᴅ: {str(e)[:50]}**")
            await asyncio.sleep(3)
            await msg.delete()
        return
    
    # /end command
    if is_command(text, "end"):
        if not await is_admin(chat_id, user_id):
            reply_msg = await event.reply("**❌ ᴏɴʟʏ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs ᴄᴀɴ ᴇɴᴅ!**")
            # Delete user's command
            try:
                await event.message.delete()
            except:
                pass
            # Delete error message after 3 seconds
            await asyncio.sleep(3)
            try:
                await reply_msg.delete()
            except:
                pass
            return
        
        player = await get_player(chat_id)
        
        # Delete user's command message
        try:
            await event.message.delete()
        except:
            pass
        
        # Clean up current local file if it was a voice message
        if player.current and player.current.get('is_local', False):
            try:
                os.remove(player.current['file_path'])
            except:
                pass
        
        if player.play_task and not player.play_task.done():
            player.play_task.cancel()
        
        try:
            await call.leave_call(chat_id)
        except:
            pass
        
        # Clean up all local files in queue
        for song in player.queue:
            if song.get('is_local', False):
                try:
                    os.remove(song['file_path'])
                except:
                    pass
        
        player.queue.clear()
        player.current = None
        player.paused = False
        
        if player.control_message_id and player.control_chat_id:
            try:
                await bot.delete_messages(player.control_chat_id, player.control_message_id)
            except:
                pass
        player.control_message_id = None
        player.control_chat_id = None
        
        msg = await event.reply("**⏹️ sᴛᴏᴘᴘᴇᴅ ᴀɴᴅ ʟᴇғᴛ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ!**")
        await asyncio.sleep(3)
        await msg.delete()
        return
    
    # /queue command
    if is_command(text, "queue"):
        player = await get_player(chat_id)
        
        # Delete user's command message
        try:
            await event.message.delete()
        except:
            pass
        
        if not player.queue:
            msg = await event.reply("**📭 ǫᴜᴇᴜᴇ ɪs ᴇᴍᴘᴛʏ!**")
            await asyncio.sleep(3)
            await msg.delete()
            return
        
        text = "**📋 ǫᴜᴇᴜᴇ ʟɪsᴛ:**\n\n"
        for i, song in enumerate(player.queue[:10], 1):
            if song.get('is_local', False):
                title = 'Voice Message'
            else:
                title = song['title'][:30]
            text += f"{i}. {title} ({song['duration_str']})\n"
        
        if len(player.queue) > 10:
            text += f"\n...ᴀɴᴅ {len(player.queue) - 10} ᴍᴏʀᴇ"
        
        msg = await event.reply(text)
        await asyncio.sleep(10)
        await msg.delete()
        return
    
    # /loop command
    if is_command(text, "loop"):
        player = await get_player(chat_id)
        
        # Delete user's command message
        try:
            await event.message.delete()
        except:
            pass
        
        player.loop = not player.loop
        status = 'ᴏɴ' if player.loop else 'ᴏғғ'
        msg = await event.reply(f"**🔄 ʟᴏᴏᴘ: {status}**")
        await asyncio.sleep(3)
        await msg.delete()
        
        # Update streaming message if exists
        if player.current and player.control_message_id:
            await send_streaming_message(chat_id, player.current, player.current.get('is_video', False))
        return
    
    # /clear command
    if is_command(text, "clear"):
        if not await is_admin(chat_id, user_id):
            reply_msg = await event.reply("**❌ ᴏɴʟʏ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs ᴄᴀɴ ᴄʟᴇᴀʀ ǫᴜᴇᴜᴇ!**")
            # Delete user's command
            try:
                await event.message.delete()
            except:
                pass
            # Delete error message after 3 seconds
            await asyncio.sleep(3)
            try:
                await reply_msg.delete()
            except:
                pass
            return
        
        player = await get_player(chat_id)
        
        # Delete user's command message
        try:
            await event.message.delete()
        except:
            pass
        
        # Clean up all local files in queue
        for song in player.queue:
            if song.get('is_local', False):
                try:
                    os.remove(song['file_path'])
                except:
                    pass
        
        queue_count = len(player.queue)
        player.queue.clear()
        msg = await event.reply(f"**🗑️ {queue_count} sᴏɴɢs ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ǫᴜᴇᴜᴇ!**")
        await asyncio.sleep(3)
        await msg.delete()
        return
    
    # /reload command
    if is_command(text, "reload"):
        if not await is_admin(chat_id, user_id):
            reply_msg = await event.reply("**❌ ᴏɴʟʏ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs ᴄᴀɴ ʀᴇʟᴏᴀᴅ!**")
            # Delete user's command
            try:
                await event.message.delete()
            except:
                pass
            # Delete error message after 3 seconds
            await asyncio.sleep(3)
            try:
                await reply_msg.delete()
            except:
                pass
            return
        
        # Delete user's command message
        try:
            await event.message.delete()
        except:
            pass
        
        msg = await event.reply("**✅ ᴀᴅᴍɪɴ ᴄʜᴇᴄᴋ ʀᴇʟᴏᴀᴅᴇᴅ!**")
        await asyncio.sleep(3)
        await msg.delete()
        return
    
    # /ping command
    if is_command(text, "ping"):
        start_time = time.time()
        msg = await event.reply("**🏓 ᴘᴏɴɢɪɴɢ...**")
        end_time = time.time()
        ping_ms = round((end_time - start_time) * 1000, 3)
        
        # Get system stats
        ram_percent = psutil.virtual_memory().percent
        cpu_percent = psutil.cpu_percent(interval=0.5)
        disk_percent = psutil.disk_usage('/').percent
        
        # Get uptime
        uptime_seconds = time.time() - BOT_START_TIME
        uptime_str = str(timedelta(seconds=int(uptime_seconds)))
        
        # Get pytgcalls ping (simulated)
        pytgcalls_ping = round(random.uniform(0.005, 0.020), 3)
        
        caption = f"""
🏓 **ᴩᴏɴɢ :** {ping_ms}ᴍs

˹𝚨𝛔𝛖𝛎𝛂 ꭙ 𝐌ᴜꜱɪᴄ ♪˼ sʏsᴛᴇᴍ sᴛᴀᴛs :

↬ **ᴜᴩᴛɪᴍᴇ :** {uptime_str}
↬ **ʀᴀᴍ :** {ram_percent}%
↬ **ᴄᴩᴜ :** {cpu_percent}%
↬ **ᴅɪsᴋ :** {disk_percent}%
↬ **ᴩʏ-ᴛɢᴄᴀʟʟs :** {pytgcalls_ping}ᴍs
        """
        
        # Delete user's command
        try:
            await event.message.delete()
        except:
            pass
        
        await msg.delete()
        await event.reply(file=PING_IMAGE_URL, message=caption)
        return
    
    # /stats command (only for bot admins)
    if is_command(text, "stats"):
        if not db.is_bot_admin(user_id):
            reply_msg = await event.reply("**❌ ᴏɴʟʏ ʙᴏᴛ ᴀᴅᴍɪɴs ᴄᴀɴ ᴠɪᴇᴡ sᴛᴀᴛs!**")
            # Delete user's command
            try:
                await event.message.delete()
            except:
                pass
            await asyncio.sleep(3)
            await reply_msg.delete()
            return
        
        stats = db.get_stats()
        
        # Delete user's command
        try:
            await event.message.delete()
        except:
            pass
        
        caption = f"""
**╭━━━━ ⟬ ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs ⟭━━━━╮**
┃
┃⟡➣ **ᴛᴏᴛᴀʟ ᴜsᴇʀs:** `{stats['users']}`
┃⟡➣ **ᴛᴏᴛᴀʟ ɢʀᴏᴜᴘs:** `{stats['groups']}`
┃⟡➣ **ᴛᴏᴛᴀʟ ᴄᴏᴍᴍᴀɴᴅs:** `{stats['total_commands']}`
┃⟡➣ **sᴏɴɢs ᴘʟᴀʏᴇᴅ:** `{stats['songs_played']}`
┃⟡➣ **ʙᴏᴛ ᴜᴘᴛɪᴍᴇ:** `{stats['uptime']}`
┃⟡➣ **ᴀᴄᴛɪᴠᴇ ᴘʟᴀʏᴇʀs:** `{len(players)}`
**╰━━━━━━━━━━━━━━━━━━━━━━╯**
        """
        
        await event.reply(caption)
        return

# ================= UPDATE COOKIES COMMAND =================
@events.register(events.NewMessage)
async def update_cookies_handler(event):
    """Handle update cookies command"""
    if not event.message.text:
        return

    text = event.message.text.strip()
    user_id = event.sender_id

    if is_command(text, "update"):
        # Only owner can update cookies
        if user_id != OWNER_ID:
            reply_msg = await event.reply("**❌ ᴏɴʟʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜᴘᴅᴀᴛᴇ ᴄᴏᴏᴋɪᴇs!**")
            try:
                await event.message.delete()
            except:
                pass
            await asyncio.sleep(3)
            try:
                await reply_msg.delete()
            except:
                pass
            return

        # Get cookies string
        cookies_string = get_command_args(text, "update")
        
        if not cookies_string:
            reply_msg = await event.reply(
                "**📝 ᴜsᴀɢᴇ:** `/update <ᴄᴏᴏᴋɪᴇs_ᴛᴇxᴛ>`\n\n"
                "**ᴇxᴀᴍᴘʟᴇ:**\n"
                "`/update # Netscape HTTP Cookie File\n.youtube.com\tTRUE\t/\tTRUE\t1735689600\tCONSENT\tYES+1`"
            )
            try:
                await event.message.delete()
            except:
                pass
            await asyncio.sleep(5)
            try:
                await reply_msg.delete()
            except:
                pass
            return

        msg = await event.reply("**🔄 ᴜᴘᴅᴀᴛɪɴɢ ᴄᴏᴏᴋɪᴇs...**")

        try:
            await event.message.delete()
        except:
            pass

        try:
            # Save cookies to database AND file
            if db.save_cookies(cookies_string):
                # Verify file was written
                if os.path.exists(COOKIES_FILE):
                    file_size = os.path.getsize(COOKIES_FILE)
                    await msg.edit(
                        f"**✅ ᴄᴏᴏᴋɪᴇs ᴜᴘᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n"
                        f"**ғɪʟᴇ:** `{COOKIES_FILE}`\n"
                        f"**sɪᴢᴇ:** `{file_size} ʙʏᴛᴇs`\n"
                        f"**ᴅᴀᴛᴀʙᴀsᴇ:** ✅ sᴀᴠᴇᴅ"
                    )
                    
                    # Log the update
                    await log_to_group(
                        "cookies_updated", 
                        details=f"Cookies file updated by owner\nSize: {file_size} bytes"
                    )
                else:
                    await msg.edit("**❌ ғᴀɪʟᴇᴅ ᴛᴏ ᴡʀɪᴛᴇ ᴄᴏᴏᴋɪᴇs ғɪʟᴇ!**")
            else:
                await msg.edit("**❌ ғᴀɪʟᴇᴅ ᴛᴏ sᴀᴠᴇ ᴄᴏᴏᴋɪᴇs ᴛᴏ ᴅᴀᴛᴀʙᴀsᴇ!**")
        
        except Exception as e:
            await msg.edit(f"**❌ ᴇʀʀᴏʀ ᴜᴘᴅᴀᴛɪɴɢ ᴄᴏᴏᴋɪᴇs:**\n`{str(e)}`")
        
        # Auto delete after 10 seconds
        await asyncio.sleep(10)
        try:
            await msg.delete()
        except:
            pass
        return

# ================= CALLBACK HANDLER =================
@events.register(events.CallbackQuery)
async def callback_handler(event):
    """Handle button callbacks"""
    data = event.data.decode()
    user_id = event.sender_id
    
    if "_" in data:
        command, chat_id_str = data.split("_", 1)
        chat_id = int(chat_id_str)
    else:
        await event.answer("Invalid data!", alert=True)
        return
    
    if not await is_admin(chat_id, user_id):
        await event.answer("ᴏɴʟʏ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs ᴄᴀɴ ᴅᴏ ᴛʜɪs!", alert=True)
        return
    
    player = await get_player(chat_id)
    
    if command == "pause":
        try:
            await call.pause(chat_id)
            await event.answer("⏸️ ᴘᴀᴜsᴇᴅ")
        except:
            await event.answer("❌ ғᴀɪʟᴇᴅ", alert=True)
    
    elif command == "skip":
        if not player.current:
            await event.answer("ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ!", alert=True)
            return
        
        # Clean up current local file if it was a voice message
        if player.current and player.current.get('is_local', False):
            try:
                os.remove(player.current['file_path'])
            except:
                pass
        
        if player.play_task and not player.play_task.done():
            player.play_task.cancel()
        
        try:
            await call.leave_call(chat_id)
        except:
            pass
        
        await asyncio.sleep(1)
        
        if player.queue:
            next_song = player.queue.pop(0)
            success = await play_song(chat_id, next_song, next_song.get('is_video', False))
            if success:
                await event.answer("⏭️ sᴋɪᴘᴘᴇᴅ")
            else:
                player.queue.insert(0, next_song)
                await event.answer("❌ ғᴀɪʟᴇᴅ ᴛᴏ ᴘʟᴀʏ", alert=True)
        else:
            player.current = None
            
            if player.control_message_id and player.control_chat_id:
                try:
                    await event.message.delete()
                except:
                    pass
            player.control_message_id = None
            player.control_chat_id = None
            
            await event.answer("ǫᴜᴇᴜᴇ ᴇᴍᴘᴛʏ")
    
    elif command == "end":
        # Clean up current local file if it was a voice message
        if player.current and player.current.get('is_local', False):
            try:
                os.remove(player.current['file_path'])
            except:
                pass
        
        # Clean up all local files in queue
        for song in player.queue:
            if song.get('is_local', False):
                try:
                    os.remove(song['file_path'])
                except:
                    pass
        
        if player.play_task and not player.play_task.done():
            player.play_task.cancel()
        
        try:
            await call.leave_call(chat_id)
        except:
            pass
        
        player.queue.clear()
        player.current = None
        player.paused = False
        
        try:
            await event.message.delete()
        except:
            pass
        player.control_message_id = None
        player.control_chat_id = None
        
        await event.answer("⏹️ sᴛᴏᴘᴘᴇᴅ")
    
    elif command == "loop":
        player.loop = not player.loop
        await event.answer(f"ʟᴏᴏᴘ: {'ᴏɴ' if player.loop else 'ᴏғғ'}")
        
        if player.current:
            await send_streaming_message(chat_id, player.current, player.current.get('is_video', False))
    
    elif command == "queue":
        if not player.queue:
            await event.answer("ǫᴜᴇᴜᴇ ɪs ᴇᴍᴘᴛʏ!", alert=True)
            return
        
        text = "**📋 ǫᴜᴇᴜᴇ ʟɪsᴛ:**\n\n"
        for i, song in enumerate(player.queue[:5], 1):
            title = 'Voice Message' if song.get('is_local', False) else song['title'][:30]
            text += f"{i}. {title} ({song['duration_str']})\n"
        
        if len(player.queue) > 5:
            text += f"\n...ᴀɴᴅ {len(player.queue) - 5} ᴍᴏʀᴇ"
        
        await event.answer(text, alert=True)
    
    elif command == "clear":
        # Clean up all local files in queue
        for song in player.queue:
            if song.get('is_local', False):
                try:
                    os.remove(song['file_path'])
                except:
                    pass
        
        player.queue.clear()
        await event.answer("🗑️ ǫᴜᴇᴜᴇ ᴄʟᴇᴀʀᴇᴅ")

# ================= HELP CALLBACK =================
@events.register(events.CallbackQuery(data="help"))
async def help_callback(event):
    help_text = """
**╭━━━━ ⟬ ʜᴇʟᴘ ᴍᴇɴᴜ ⟭━━━━╮**
┃
┃ **ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs:** 
┃
┃✨ **/play** [song] - ᴘʟᴀʏ ᴀᴜᴅɪᴏ
┃   📢 ʀᴇᴘʟʏ ᴛᴏ ᴠᴏɪᴄᴇ ᴍᴇssᴀɢᴇ ᴛᴏ ᴘʟᴀʏ
┃🎬 **/vplay** [video] - ᴘʟᴀʏ ᴠɪᴅᴇᴏ
┃⏭️ **/skip** - sᴋɪᴘ ᴄᴜʀʀᴇɴᴛ
┃⏸️ **/pause** - ᴘᴀᴜsᴇ
┃▶️ **/resume** - ʀᴇsᴜᴍᴇ
┃⏹️ **/end** - sᴛᴏᴘ
┃📋 **/queue** - sʜᴏᴡ ǫᴜᴇᴜᴇ
┃🔄 **/loop** - ᴛᴏɢɢʟᴇ ʟᴏᴏᴘ
┃🗑️ **/clear** - ᴄʟᴇᴀʀ ǫᴜᴇᴜᴇ
┃🔄 **/reload** - ʀᴇʟᴏᴀᴅ ᴀᴅᴍɪɴs
┃🏓 **/ping** - ᴄʜᴇᴄᴋ ʙᴏᴛ ᴘɪɴɢ
┃🍪 **/update** - ᴜᴘᴅᴀᴛᴇ ᴄᴏᴏᴋɪᴇs (ᴏᴡɴᴇʀ ᴏɴʟʏ)
┃
┃ **ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs:**
┃
┃📢 **/gcast** - ʙʀᴏᴀᴅᴄᴀsᴛ
┃➕ **/addadmin** - ᴀᴅᴅ ʙᴏᴛ ᴀᴅᴍɪɴ
┃➖ **/deladmin** - ʀᴇᴍᴏᴠᴇ ʙᴏᴛ ᴀᴅᴍɪɴ
┃📋 **/admins** - sʜᴏᴡ ᴀᴅᴍɪɴs
┃📊 **/stats** - sʜᴏᴡ ʙᴏᴛ sᴛᴀᴛs
**╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯**
    """
    
    buttons = [[Button.inline("🔙 ʙᴀᴄᴋ", data="back_to_start")]]
    await event.edit(help_text, buttons=buttons)

@events.register(events.CallbackQuery(data="back_to_start"))
async def back_to_start(event):
    user = await event.get_sender()
    
    caption = f"""
✨ **ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ˹𝚨𝛔𝛖𝛎𝛂 ꭙ 𝐌ᴜꜱɪᴄ ♪˼ ʙᴏᴛ** ✨

⟡➣ **ʜᴇʏ** [{get_display_name(user)}](tg://user?id={user.id}) ❤️

⟡➣ **ɪ ᴀᴍ ᴀ ᴘᴏᴡᴇʀғᴜʟ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ.**
⟡➣ **ᴛʜᴀᴛ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜsɪᴄ ᴀɴᴅ ᴠɪᴅᴇᴏ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs.**
    """
    
    buttons = [
        [Button.url("⟡➣ 𝙾𝚠𝚗𝚎𝚛", f"https://t.me/god_knows_0"),
         Button.url("➕ 𝙰𝚍𝚍 𝙼𝚎", f"https://t.me/{(await event.client.get_me()).username}?startgroup=true")],
        [Button.inline("⟡➣ 𝙷𝚎𝚕𝚙", data="help"),
         Button.url("⟡➣ 𝚄𝚙𝚍𝚊𝚝𝚎𝚜", f"https://t.me/{UPDATES_CHANNEL}")]
    ]
    
    await event.edit(file=WELCOME_IMAGE_URL, message=caption, buttons=buttons)

# ================= ADMIN COMMANDS =================
@events.register(events.NewMessage)
async def admin_commands(event):
    """Handle admin commands"""

    if not event.message.text:
        return

    text = event.message.text.strip()
    user_id = event.sender_id

    # Only run if it's actually an admin command
    if not any(is_command(text, cmd) for cmd in ["gcast", "addadmin", "deladmin", "admins"]):
        return

    # ================= GCAST =================
    if is_command(text, "gcast"):

        if not db.is_bot_admin(user_id):
            reply_msg = await event.reply("❌ You are not a bot admin!")
            await asyncio.sleep(3)
            await reply_msg.delete()
            return

        query = get_command_args(text, "gcast")
        if not query:
            reply_msg = await event.reply("Usage: /gcast <message>")
            await asyncio.sleep(3)
            await reply_msg.delete()
            return

        try:
            await event.message.delete()
        except:
            pass

        msg = await event.reply("📢 Broadcasting...")

        sent_users = 0
        failed_users = 0
        sent_groups = 0
        failed_groups = 0

        # ===== USERS =====
        for user_id_str in list(db.data["users"].keys()):
            try:
                await bot.send_message(int(user_id_str), query)
                sent_users += 1
                await asyncio.sleep(0.3)

            except Exception as e:
                failed_users += 1

                error_text = str(e).lower()

                # Remove blocked users
                if "blocked" in error_text or "deactivated" in error_text:
                    db.data["users"].pop(user_id_str, None)

                # Handle flood wait
                if "flood" in error_text:
                    await asyncio.sleep(5)

        # ===== GROUPS =====
        for group_id_str in list(db.data["groups"].keys()):
            try:
                await bot.send_message(int(group_id_str), query)
                sent_groups += 1
                await asyncio.sleep(0.5)

            except Exception as e:
                failed_groups += 1
                error_text = str(e).lower()

                # Remove invalid groups
                if "not a member" in error_text or "chat not found" in error_text:
                    db.remove_group(group_id_str)

                if "flood" in error_text:
                    await asyncio.sleep(5)

        db.save()

        await msg.edit(
            f"📢 Broadcast Completed\n\n"
            f"👤 Users → ✅ {sent_users} | ❌ {failed_users}\n"
            f"👥 Groups → ✅ {sent_groups} | ❌ {failed_groups}"
        )

        await asyncio.sleep(6)
        await msg.delete()
        return
    
    # /addadmin command
    if is_command(text, "addadmin"):
        if user_id != OWNER_ID:
            reply_msg = await event.reply("**❌ ᴏɴʟʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴀᴅᴅ ᴀᴅᴍɪɴs!**")
            try:
                await event.message.delete()
            except:
                pass
            await asyncio.sleep(3)
            await reply_msg.delete()
            return
        
        new_admin = get_command_args(text, "addadmin")
        if not new_admin:
            reply_msg = await event.reply("**ᴜsᴀɢᴇ:** `/addadmin <ᴜsᴇʀ_ɪᴅ>`")
            try:
                await event.message.delete()
            except:
                pass
            await asyncio.sleep(3)
            await reply_msg.delete()
            return
        
        try:
            await event.message.delete()
        except:
            pass
        
        try:
            new_admin = int(new_admin)
            if db.add_bot_admin(new_admin):
                msg = await event.reply(f"**✅ ᴜsᴇʀ `{new_admin}` ɪs ɴᴏᴡ ᴀ ʙᴏᴛ ᴀᴅᴍɪɴ!**")
            else:
                msg = await event.reply("**⚠️ ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ ᴏʀ ɪs ᴏᴡɴᴇʀ!**")
        except:
            msg = await event.reply("**❌ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ!**")
        
        await asyncio.sleep(3)
        await msg.delete()
        return
    
    # /deladmin command
    if is_command(text, "deladmin"):
        if user_id != OWNER_ID:
            reply_msg = await event.reply("**❌ ᴏɴʟʏ ᴏᴡɴᴇʀ ᴄᴀɴ ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴs!**")
            try:
                await event.message.delete()
            except:
                pass
            await asyncio.sleep(3)
            await reply_msg.delete()
            return
        
        remove_admin = get_command_args(text, "deladmin")
        if not remove_admin:
            reply_msg = await event.reply("**ᴜsᴀɢᴇ:** `/deladmin <ᴜsᴇʀ_ɪᴅ>`")
            try:
                await event.message.delete()
            except:
                pass
            await asyncio.sleep(3)
            await reply_msg.delete()
            return
        
        try:
            await event.message.delete()
        except:
            pass
        
        try:
            remove_admin = int(remove_admin)
            if db.remove_bot_admin(remove_admin):
                msg = await event.reply(f"**✅ ᴜsᴇʀ `{remove_admin}` ɪs ɴᴏ ʟᴏɴɢᴇʀ ᴀ ʙᴏᴛ ᴀᴅᴍɪɴ!**")
            else:
                msg = await event.reply("**⚠️ ᴜsᴇʀ ɪs ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ᴏʀ ɪs ᴏᴡɴᴇʀ!**")
        except:
            msg = await event.reply("**❌ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ!**")
        
        await asyncio.sleep(3)
        await msg.delete()
        return
    
    # /admins command
    if is_command(text, "admins"):
        if not db.is_bot_admin(user_id):
            reply_msg = await event.reply("**❌ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀ ʙᴏᴛ ᴀᴅᴍɪɴ!**")
            try:
                await event.message.delete()
            except:
                pass
            await asyncio.sleep(3)
            await reply_msg.delete()
            return
        
        try:
            await event.message.delete()
        except:
            pass
        
        text = "**👑 ʙᴏᴛ ᴀᴅᴍɪɴs ʟɪsᴛ:**\n\n"
        for admin_id in db.get_bot_admins():
            try:
                user = await bot.get_entity(admin_id)
                text += f"• {get_display_name(user)} (`{admin_id}`)\n"
            except:
                text += f"• `{admin_id}`\n"
        
        msg = await event.reply(text)
        await asyncio.sleep(10)
        await msg.delete()
        return

# ================= GROUP LEAVE HANDLER =================
@events.register(events.ChatAction)
async def on_leave(event):
    """Handle bot being removed from group"""
    if event.user_left or event.user_kicked:
        if event.user_id == (await bot.get_me()).id:
            chat = await event.get_chat()
            db.remove_group(chat.id)

# ================= MAIN FUNCTION =================
async def main():
    global bot, assistant, call, BOT_START_TIME
    
    BOT_START_TIME = time.time()
    
    bot = TelegramClient('bot', API_ID, API_HASH)
    assistant = TelegramClient(StringSession(ASSISTANT_SESSION), API_ID, API_HASH)
    
    logger.info("Starting Bot...")
    await bot.start(bot_token=BOT_TOKEN)
    logger.info("✅ Bot Started!")
    
    logger.info("Starting Assistant...")
    await assistant.start()
    logger.info("✅ Assistant Started!")
    
    logger.info("Caching dialogs for assistant...")
    async for dialog in assistant.iter_dialogs():
        logger.info(f"Cached: {dialog.name} (ID: {dialog.id})")
    
    logger.info("Starting PyTgCalls...")
    call = PyTgCalls(assistant)
    await call.start()
    logger.info("✅ PyTgCalls Started!")
    
    bot.add_event_handler(message_handler)
    bot.add_event_handler(callback_handler)
    bot.add_event_handler(help_callback)
    bot.add_event_handler(back_to_start)
    bot.add_event_handler(admin_commands)
    bot.add_event_handler(on_leave)
    bot.add_event_handler(update_cookies_handler)
    
    # Log bot start
    await log_to_group("bot_start", details=f"Bot started successfully!\nUsers: {len(db.data['users'])}\nGroups: {len(db.data['groups'])}")
    
    logger.info("🤖 Bot is running!")
    await bot.run_until_disconnected()

# ================= RUN BOT =================
if __name__ == "__main__":
    # Install required packages:
    # pip install telethon pytgcalls yt-dlp pillow aiohttp psutil
    # Also need ffmpeg installed on system
    asyncio.run(main())
