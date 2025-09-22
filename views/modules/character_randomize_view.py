import discord
from core.randomize_funcs import get_random_character
from views.modules.perks_randomize_view import PerksRandomizeView
from views.randomize_view import BaseRandomizeView


class CharacterRandomizeView(BaseRandomizeView):

    def __init__(self, ctx, data_loader, state, character_type, next_step: bool = True):

        followup = {
            "killer": {"view": PerksRandomizeView, "next_drawn": "perks"},
            "survivor": {"view": PerksRandomizeView, "next_drawn": "perks"}
        }

        super().__init__(
            ctx, data_loader, state, character_type, next_step, followup_view=followup
        )

        self.characters_list = data_loader.characters_list
        self.random_character = None
        self.exclude_ids = []

        self.randomize()

        self.get_replace_button("Character")
        self.get_accept_button()
    
    def get_message(self):
        msg = f'**{self.ctx.author.mention}**, your character:'

        embeds = []

        character_name = self.random_character[f"{self.character_type}_name"]
        character_desc = self.random_character[f"{self.character_type}_description"]
        character_icon = self.random_character[f"{self.character_type}_icon"]

        embed = discord.Embed(
            title=character_name,
            description=f'*{character_desc}*',
            color=discord.Color.dark_blue()
        )
        embed.set_thumbnail(url=character_icon)
        embeds.append(embed)

        if not self.next_step:
            embeds[-1].set_footer(text=f'Check out !{self.character_type}_setup too!')

        return {'content': msg, 'embeds': embeds}

    def randomize(self):
        randomize_result = get_random_character(
            self.characters_list,
            self.character_type,
            self.exclude_ids,
        )
        
        self.exclude_ids = randomize_result["exclude_ids"]
        self.random_character = randomize_result[f"random_{self.character_type}"]

    async def accept(self, interaction: discord.Interaction):
        self.state.character = self.random_character
        next_view = self.followup_view["view"](ctx=self.ctx, 
                                               data_loader=self.data_loader, 
                                               state=self.state, 
                                               character_type=self.character_type, 
                                               next_step=True)
        msg = next_view.get_message()
        content = msg['content']
        embeds = msg['embeds']

        await interaction.response.edit_message(
            content=content,
            embeds=embeds,
            view=next_view
        )


