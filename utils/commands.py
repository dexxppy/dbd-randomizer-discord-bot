import discord

from views.modules.character_randomize_view import CharacterRandomizeView
from core.data_loader import DataLoader
from views.modules.offering_randomize_view import OfferingRandomizeView
from views.modules.item_randomize_view import ItemRandomizeView
from views.modules.killer_addons_randomize_view import KillerAddonsRandomizeView
from views.modules.perks_randomize_view import PerksRandomizeView
from views.start_setup_view import StartSetupView

async def base(ctx, view):
    msg = view.get_message()
    content = msg['content']
    embeds = msg['embeds']

    await ctx.send(
        content=content,
        embeds=embeds,
        view=view
    )


async def setup(ctx, character_type: str):
    view = StartSetupView(ctx=ctx, character_type=character_type)
    await base(ctx, view)


async def perks(ctx, character_type: str):
    view = PerksRandomizeView(ctx=ctx,
                              data_loader=DataLoader(character_type),
                              state=None,
                              character_type=character_type,
                              next_step=False)

    await base(ctx, view)


async def character(ctx, character_type: str):
    view = CharacterRandomizeView(ctx=ctx,
                                  data_loader=DataLoader(character_type),
                                  state=None,
                                  character_type=character_type,
                                  next_step=False)
    await base(ctx, view)


async def killer_addons(ctx):
    view = KillerAddonsRandomizeView(
        ctx=ctx,
        data_loader=DataLoader("killer"),
        state=None,
        next_step=False
    )
    await base(ctx, view)


async def item(ctx):
    view = ItemRandomizeView(
        ctx=ctx,
        data_loader=DataLoader("survivor"),
        state=None,
        next_step=False
    )
    await base(ctx, view)


async def offering(ctx, character_type: str):
    view = OfferingRandomizeView(ctx=ctx,
                                 data_loader=DataLoader(character_type),
                                 state=None,
                                 character_type=character_type,
                                 next_step=False)
    await base(ctx, view)

def register_help_command(bot):
    @bot.command(name="help")
    async def custom_help(ctx):
        embed = discord.Embed(
            title="🎲 Dead By Daylight Randomizer",
            description="Available commands",
            color=discord.Color.dark_red()
        )
        embed.add_field(
            name="🎭 Characters",
            value="`!killer` - Randomize killer character\n"
                  "`!survivor` - Randomize survivor character\n",
            inline=False
        )
        embed.add_field(
            name="🎁 Offerings",
            value="`!killer_offering` - Randomize offering for killer\n"
                  "`!survivor_offering` - Randomize offering for survivor\n",
            inline=False
        )
        embed.add_field(
            name="🔧 Item",
            value="`!item` - Randomize item for survivor\n",
            inline=False
        )
        embed.add_field(
            name="🃏 Perks",
            value="`!killer_perks` - Randomize perks for killer\n"
                  "`!survivor_perks` - Randomize perks for survivor\n",
            inline=False
        )
        embed.add_field(
            name="⚙️ Setup",
            value="`!killer_setup` - Randomize whole setup for killer\n"
                  "`!survivor_setup` - Randomize whole setup for survivor\n",
            inline=False
        )

        embed.set_author(name="With ♥ by dexxppy", )
        await ctx.send(embed=embed)

def register_character_specific_commands(bot):
    @bot.command(name=f"item")
    async def _item(ctx):
        await item(ctx)


def register_commands(bot, character_type: str):

    @bot.command(name=f"{character_type}")
    async def _character(ctx):
        await character(ctx, character_type)

    @bot.command(name=f"{character_type}_offering")
    async def _offering(ctx):
        await offering(ctx, character_type)

    @bot.command(name=f"{character_type}_perks")
    async def _perks(ctx):
        await perks(ctx, character_type)

    @bot.command(name=f"{character_type}_setup")
    async def _setup(ctx):
        await setup(ctx, character_type)
