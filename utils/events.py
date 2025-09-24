import discord
from utils.logger import send_log

def register_events(bot, channel_id):
    @bot.event
    async def on_command_error(ctx, error):
        from discord.ext import commands
        import traceback

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
            await send_log(bot, channel_id, msg)

    @bot.event
    async def on_error(event, *args, **kwargs):
        import traceback
        tb = "".join(traceback.format_exc())
        msg = f"[ERROR] Event {event} encountered an error" + tb

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
