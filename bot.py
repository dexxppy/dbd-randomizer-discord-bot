from datetime import datetime

import discord
import os

from discord.ext import commands
from dotenv import load_dotenv
from commands import register_commands, register_help_command, register_character_specific_commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID'))

@bot.event
async def on_guild_join(guild):
    log_message = ""
    try:
        owner = guild.get_member(guild.owner_id)
        if owner is None:
            owner = await guild.fetch_member(guild.owner_id)

        log_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INVITE] Bot invited to {guild.name} (ID: {guild.id}, Members: {guild.member_count}) by {owner}"
    except Exception as e:
        log_message = f"Error inviting to new server: {e}"
    finally:
        print(log_message)

        with open("bot_logs.txt", "a", encoding="utf-8") as f:
            f.write(log_message + "\n")

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(log_message)

@bot.event
async def on_guild_remove(guild):
    log_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [KICK] Bot removed from {guild.name} (ID: {guild.id})"
    print(log_message)

    with open("bot_logs.txt", "a", encoding="utf-8") as f:
        f.write(log_message + "\n")

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(log_message)

@bot.listen("on_command")
async def log_command(ctx):
    log_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [COMMAND] {ctx.author} called: '{ctx.command}' on server: {ctx.guild.name if ctx.guild else 'DM'}"
    print(log_message)

    with open("bot_logs.txt", "a", encoding="utf-8") as f:
        f.write(log_message + "\n")

register_help_command(bot)
register_character_specific_commands(bot)
register_commands(bot, "killer")
register_commands(bot, "survivor")

bot.run(TOKEN)

