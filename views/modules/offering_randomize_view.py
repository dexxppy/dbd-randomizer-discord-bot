import discord
from core.randomize_funcs import get_random_offering
from views.final_setup_view import FinalSetupView
from core.data_loader import DataLoader
from core.state import SetupState
from views.randomize_view import BaseRandomizeView


class OfferingRandomizeView(BaseRandomizeView):

    def __init__(self, ctx, data_loader: DataLoader, state: SetupState, character_type, next_step: bool = True):

        followup = {
            "killer": {"view": FinalSetupView, "next_drawn": "summary"},
            "survivor": {"view": FinalSetupView, "next_drawn": "summary"}
        }

        super().__init__(
            ctx, data_loader, state, character_type, next_step, followup_view=followup
        )
        
        offerings = data_loader.offerings_list
        self.offerings_list = offerings[f"{character_type}_offerings"]
        self.random_offering = None
        self.exclude_ids = []

        self.randomize()
        self.get_replace_button("Offering")
        self.get_accept_button()
    
    def get_message(self):
        msg = f'**{self.ctx.author.mention}**, your offering:'

        embeds = []

        offering_name = self.random_offering[f"offering_name"]
        offering_rarity = self.random_offering[f"offering_rarity"]
        offering_icon = self.random_offering[f"offering_icon"]
        offering_type = self.random_offering[f"offering_type"]

        embed = discord.Embed(
            title=offering_name,
            description=f'{offering_type} \n of *{offering_rarity}* rarity',
            color=discord.Color.dark_purple()
        )
        embed.set_thumbnail(url=offering_icon)
        embeds.append(embed)

        if not self.next_step:
            embeds[-1].set_footer(text=f'Check out !{self.character_type}_setup too!')

        return {'content': msg, 'embeds': embeds}
            
    def randomize(self):
        randomize_result = get_random_offering(
            self.offerings_list,
            self.exclude_ids
        )
        
        self.exclude_ids = randomize_result["exclude_ids"]
        self.random_offering = randomize_result[f"random_offering"]
        
    async def accept(self, interaction: discord.Interaction):
        self.state.offering = self.random_offering
        next_view = self.followup_view["view"](ctx=self.ctx, state=self.state, character_type=self.character_type)

        await interaction.response.edit_message(
            content=None,
            embed=next_view.get_message(),
            view=next_view
        )

