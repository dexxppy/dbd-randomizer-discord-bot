import traceback

try:
    import discord
    import os

    from discord.ext import commands
    from dotenv import load_dotenv

    from utils.error_handler import *
    from utils.commands import (
        register_commands,
        register_help_command,
        register_character_specific_commands,
    )
    from utils.events import register_events

    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True

    bot = commands.Bot(
        command_prefix="!",
        intents=intents,
        help_command=None
    )

    load_dotenv()

    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

    print("TOKEN:", TOKEN is not None)
    print("CHANNEL:", CHANNEL_ID)

    register_help_command(bot)
    register_character_specific_commands(bot)
    register_commands(bot, "killer")
    register_commands(bot, "survivor")
    register_events(bot, CHANNEL_ID)

    print("Starting bot...")


    import asyncio
    asyncio.get_running_loop().set_exception_handler(handle_async_exception)
    
    bot.run(TOKEN)

except Exception:
    traceback.print_exc()
    raise