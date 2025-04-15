import os
import logging
import json
import time
import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from config import ADMINS

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

POLL_OPTIONS_FILE = "poll_templates.json"
DEFAULT_POLLS = {
    "mood": {
        "question": "How are you feeling today?",
        "options": ["Great", "Good", "Okay", "Not so good", "Terrible"]
    },
    "food": {
        "question": "What's your favorite food type?",
        "options": ["Italian", "Chinese", "Indian", "Mexican", "Fast food"]
    },
    "weather": {
        "question": "What's your favorite weather?",
        "options": ["Sunny", "Rainy", "Snowy", "Cloudy", "Windy"]
    }
}

async def load_poll_templates():
    """Load poll templates from file"""
    try:
        if os.path.exists(POLL_OPTIONS_FILE):
            with open(POLL_OPTIONS_FILE, "r") as f:
                return json.load(f)
        # If file doesn't exist, create it with default polls
        with open(POLL_OPTIONS_FILE, "w") as f:
            json.dump(DEFAULT_POLLS, f, indent=4)
        return DEFAULT_POLLS
    except Exception as e:
        logger.error(f"Error loading poll templates: {e}")
        return DEFAULT_POLLS

async def save_poll_templates(templates):
    """Save poll templates to file"""
    try:
        with open(POLL_OPTIONS_FILE, "w") as f:
            json.dump(templates, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving poll templates: {e}")

@Client.on_message(filters.command('poll'))
async def send_poll_handler(client, message: Message):
    """Send a poll when a user uses the /poll command"""
    try:
        # Extract command arguments
        args = message.text.split(' ', 2)
        poll_templates = await load_poll_templates()
        
        # If no arguments are provided, send the default mood poll
        if len(args) == 1:
            poll_data = poll_templates.get("mood", DEFAULT_POLLS["mood"])
            
            # Using bot.get_me() to check if initialized
            me = await client.get_me()
            logger.info(f"Bot username: {me.username}")
            
            # Try sending with pyrogram's raw API
            await message.reply("Creating mood poll...")
            try:
                return await client._send_custom_request(
                    "sendPoll",
                    {
                        "chat_id": message.chat.id,
                        "question": poll_data["question"],
                        "options": poll_data["options"],  # No need to JSON encode
                        "is_anonymous": False,
                        "allows_multiple_answers": False
                    }
                )
            except AttributeError:
                # If _send_custom_request doesn't exist, try this alternative
                return await client.invoke(
                    raw.functions.messages.SendMedia(
                        peer=await client.resolve_peer(message.chat.id),
                        media=raw.types.InputMediaPoll(
                            poll=raw.types.Poll(
                                id=random.randint(0, 2147483647),
                                question=poll_data["question"],
                                answers=[
                                    raw.types.PollAnswer(text=option, option=bytes([i]))
                                    for i, option in enumerate(poll_data["options"])
                                ],
                                closed=False,
                                public_voters=True,
                                multiple_choice=False,
                                quiz=False
                            )
                        ),
                        random_id=random.randint(0, 2147483647),
                        message=""
                    )
                )
            
        # If a template name is provided
        if len(args) >= 2 and args[1] in poll_templates:
            poll_data = poll_templates[args[1]]
            await message.reply(f"💭 Here's a poll about {args[1]}...")
            
            # Use a simpler approach - creating a poll via Telegram Bot API
            # Most scripts have an HTTP client imported, or we can use the built-in one
            import urllib.request
            import urllib.parse
            
            # Get bot token
            bot_token = os.environ.get("BOT_TOKEN", "")
            if not bot_token:
                # Try to get the token from the client if available
                try:
                    bot_token = client.bot_token
                except:
                    await message.reply("❌ Could not find bot token. Please set BOT_TOKEN in environment variables.")
                    return
            
            # Create API URL
            api_url = f"https://api.telegram.org/bot{bot_token}/sendPoll"
            
            # Prepare data
            data = {
                "chat_id": message.chat.id,
                "question": poll_data["question"],
                "options": json.dumps(poll_data["options"]),
                "is_anonymous": False,
                "allows_multiple_answers": False
            }
            
            # Send request
            data = urllib.parse.urlencode(data).encode()
            req = urllib.request.Request(api_url, data=data)
            try:
                with urllib.request.urlopen(req) as response:
                    response_data = response.read()
                    logger.info(f"Poll response: {response_data}")
                return
            except Exception as e:
                logger.error(f"Error sending poll via HTTP: {e}")
                await message.reply(f"❌ Failed to create poll. Try a different approach.")
                return
            
        # Show usage instructions
        await message.reply(
            "📊 **Poll Command Usage**:\n\n"
            "• `/poll` - Send a mood poll\n"
            "• `/poll food` - Send food preference poll\n"
            "• `/poll weather` - Send weather preference poll\n"
            f"Available templates: {', '.join(poll_templates.keys())}"
        )
        
    except Exception as e:
        logger.exception(f"Poll command error: {e}")
        await message.reply(f"❌ Error creating poll: {str(e)}")

@Client.on_message(filters.command('addpoll') & filters.user(ADMINS))
async def add_poll_template(client, message: Message):
    """Allows admins to add new poll templates"""
    try:
        args = message.text.split(' ', 3)
        if len(args) != 4:
            await message.reply(
                "❌ **Format error!**\n\n"
                "Usage: `/addpoll template_name \"Question\" \"Option1, Option2, ...\"`\n\n"
                "Example: `/addpoll movies \"What's your favorite movie genre?\" \"Action, Comedy, Horror, Sci-Fi, Drama\"`"
            )
            return
            
        template_name = args[1].lower()
        question = args[2].strip('"\'')
        options_text = args[3].strip('"\'')
        options = [opt.strip() for opt in options_text.split(',')]
        
        if len(options) < 2 or len(options) > 10:
            await message.reply("❌ Poll must have between 2 and 10 options!")
            return
            
        poll_templates = await load_poll_templates()
        poll_templates[template_name] = {
            "question": question,
            "options": options
        }
        await save_poll_templates(poll_templates)
        
        await message.reply(f"✅ Poll template `{template_name}` added successfully!")
        
    except Exception as e:
        logger.exception(f"Add poll template error: {e}")
        await message.reply("❌ Error adding poll template.")

@Client.on_message(filters.command('listpolls'))
async def list_poll_templates(client, message: Message):
    """List all available poll templates"""
    try:
        poll_templates = await load_poll_templates()
        if not poll_templates:
            await message.reply("No poll templates available.")
            return
            
        reply_text = "📊 **Available Poll Templates**:\n\n"
        for name, data in poll_templates.items():
            options_text = "`, `".join(data["options"])
            reply_text += f"• **{name}**: \"{data['question']}\"\n  Options: `{options_text}`\n\n"
            
        await message.reply(reply_text)
        
    except Exception as e:
        logger.exception(f"List polls error: {e}")
        await message.reply("❌ Error retrieving poll templates.")

@Client.on_message(filters.command('delpoll') & filters.user(ADMINS))
async def delete_poll_template(client, message: Message):
    """Allows admins to delete poll templates"""
    try:
        args = message.text.split(' ', 1)
        if len(args) != 2:
            await message.reply("❌ Usage: `/delpoll template_name`")
            return
            
        template_name = args[1].lower()
        poll_templates = await load_poll_templates()
        
        if template_name not in poll_templates:
            await message.reply(f"❌ Template `{template_name}` not found!")
            return
            
        del poll_templates[template_name]
        await save_poll_templates(poll_templates)
        
        await message.reply(f"✅ Poll template `{template_name}` deleted successfully!")
        
    except Exception as e:
        logger.exception(f"Delete poll template error: {e}")
        await message.reply("❌ Error deleting poll template.")