import os
import traceback

import discord
from utils.logger import send_log

def register_events(bot, channel_id):
    @bot.event
    async def on_command_error(ctx, error):
        from discord.ext import commands

        if isinstance(error, commands.CommandNotFound):
            return

        msg = f"[ERROR] "
        tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))

        try:
            guild_name = ctx.guild.name if ctx.guild else "DM"
            user = f"{ctx.author} (ID: {ctx.author.id})"

            msg = f"[ERROR] Command {ctx.command} called by {user} on server {guild_name} encountered an error: {error}"
        except Exception as e:
            msg += f"{e} "
        finally:
            msg = msg + tb

            with open("last_error.txt", "w", encoding="utf-8") as f:
                f.write(msg)

            await send_log(bot, channel_id, msg)

    @bot.event
    async def on_error(event, *args, **kwargs):
        error_msg = traceback.format_exc()
        with open("last_error.txt", "w", encoding="utf-8") as f:
            f.write(error_msg)

        msg = f"[ERROR] Event {event} encountered an error: {error_msg}"

        await send_log(bot, channel_id, msg)

    @bot.event
    async def on_guild_join(guild):
        try:
            owner = guild.get_member(guild.owner_id) or await guild.fetch_member(guild.owner_id)
            msg = f"[INVITE] Bot invited to {guild.name} (ID: {guild.id}, Members: {guild.member_count}) by {owner}"
        except Exception as e:
            msg = f"[ERROR] Could not fetch guild owner: {e}"
        await send_log(bot, channel_id, msg)

    @bot.event
    async def on_guild_remove(guild):
        await send_log(bot, channel_id, f"[KICK] Bot removed from {guild.name} (ID: {guild.id})")

    @bot.listen("on_command")
    async def log_command(ctx):
        await send_log(bot, channel_id, f"[COMMAND] {ctx.author} called '{ctx.command}' on {ctx.guild.name if ctx.guild else 'DM'}")

    @bot.event
    async def on_ready():
        print(f"Logged as {bot.user}")

        if os.path.exists("last_error.txt"):
            with open("last_error.txt", "r", encoding="utf-8") as f:
                last_error = f.read()

            if last_error.strip():
                await send_log(bot, channel_id, f"[ERROR] Last logged error before restarting:\n```\n{last_error}\n```")

            open("last_error.txt", "w", encoding="utf-8").close()
