from datetime import datetime
import discord

async def send_log(bot, channel_id, message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"

    print(log_message)

    with open("bot_logs.txt", "a", encoding="utf-8") as f:
        f.write(log_message + "\n")

    channel = bot.get_channel(channel_id)
    if channel and isinstance(channel, discord.TextChannel):
        await channel.send(log_message)
