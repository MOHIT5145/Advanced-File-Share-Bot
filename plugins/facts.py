import os
import logging
import random
import asyncio
import re
import json
import html
import base64
import time
import socket
import ssl
import urllib.parse
import html  # Python standard library
import requests
from datetime import date, datetime, timedelta
from pytz import timezone
from pyrogram import Client, filters, enums
from pyrogram.types import *
from config import *
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# =============================
# DAILY FACTS FUNCTIONALITY
# =============================
def fetch_daily_facts() -> str:
    """
    Fetches 3 random facts (fixed list conversion)
    """
    try:
        facts = set()
        
        for _ in range(3):
            response = requests.get(
                "https://uselessfacts.jsph.pl/api/v2/facts/random",
                headers={'Accept': 'application/json'},
                timeout=10
            )
            response.raise_for_status()
            fact_data = response.json()
            facts.add(fact_data['text'].strip())

        # Explicitly use built-in list() function
        formatted_facts = [f"✦ {fact}" for fact in __builtins__.list(facts)[:3]]
            
        return (
            "🧠 **Daily Knowledge Boost**\n\n"
            "\n\n".join(formatted_facts) +
            "\n\n━━━━━━━━━━━━━━━━━━━\n"
            "Stay Curious! @Excellerators"
        )
        
    except Exception as e:
        logger.error(f"Fact API error: {str(e)}", exc_info=True)
        return (
            "💡 **Did You Know?**\n\n"
            "✦ Honey never spoils\n"
            "✦ Octopuses have three hearts\n"
            "✦ The Eiffel Tower grows in summer\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "Learn more @Excellerators"
        )
    
    
async def send_scheduled_facts(bot: Client):
    """
    Sends facts daily at 8 AM, 1 PM, and 8 PM IST
    """
    tz = timezone('Asia/Kolkata')
    
    while True:
        now = datetime.now(tz)
        target_times = [
            now.replace(hour=8, minute=0, second=0, microsecond=0),
            now.replace(hour=13, minute=0, second=0, microsecond=0),
            now.replace(hour=20, minute=0, second=0, microsecond=0)
        ]
        
        valid_times = [t for t in target_times if t > now]
        if not valid_times:
            next_time = target_times[0] + timedelta(days=1)
        else:
            next_time = min(valid_times)
        
        sleep_seconds = (next_time - now).total_seconds()
        logger.info(f"Next facts at {next_time.strftime('%d %b %Y %H:%M IST')}")
        
        await asyncio.sleep(sleep_seconds)
        
        try:
            fact_message = fetch_daily_facts()
            await bot.send_message(
                chat_id=FACTS_CHANNEL,
                text=fact_message,
                disable_web_page_preview=True
            )
            await bot.send_message(
                chat_id=LOG_CHANNEL,
                text=f"📚 Facts sent at {datetime.now(tz).strftime('%H:%M IST')}"
            )
            
        except Exception as e:
            logger.exception("Fact broadcast failed:")
            await bot.send_message(
                chat_id=LOG_CHANNEL,
                text=f"❌ Fact error: {str(e)[:500]}"
            )

@Client.on_message(filters.command('facts') & filters.user(ADMINS))
async def instant_facts_handler(client, message: Message):
    try:
        processing_msg = await message.reply("⏳ Fetching facts...")
        fact_message = fetch_daily_facts()
        
        await client.send_message(
            chat_id=FACTS_CHANNEL,
            text=fact_message,
            disable_web_page_preview=True
        )
        
        await processing_msg.edit("✅ Facts published!")
        await client.send_message(
            chat_id=LOG_CHANNEL,
            text=f"📚 Manual facts by {message.from_user.mention}"
        )
        
    except Exception as e:
        await processing_msg.edit(f"❌ Error: {str(e)[:200]}")
        await client.send_message(
            chat_id=LOG_CHANNEL,
            text=f"⚠️ Facts failed by {message.from_user.mention}"
        )

def schedule_facts(client: Client):
    """Starts the facts scheduler"""
    asyncio.create_task(send_scheduled_facts(client))