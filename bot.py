import discord
import os

from discord.ext import commands
from dotenv import load_dotenv
from utils.commands import register_commands, register_help_command, register_character_specific_commands
from utils.events import register_events

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID'))

register_help_command(bot)
register_character_specific_commands(bot)
register_commands(bot, "killer")
register_commands(bot, "survivor")
register_events(bot, CHANNEL_ID)

bot.run(TOKEN)

