import discord
from utils.views_utils import get_options_for_select
from core.randomize_funcs import get_random_perks
from views.modules.item_randomize_view import ItemRandomizeView
from views.modules.killer_addons_randomize_view import KillerAddonsRandomizeView
from core.data_loader import DataLoader
from core.state import SetupState
from views.randomize_view import BaseRandomizeView


class PerksRandomizeView(BaseRandomizeView):

    def __init__(self, ctx, data_loader: DataLoader, state: SetupState, character_type, next_step: bool = False):

        followup = {
            "killer": {"view": KillerAddonsRandomizeView, "next_drawn": "addons"},
            "survivor": {"view": ItemRandomizeView, "next_drawn": "item"}
        }

        super().__init__(
            ctx, data_loader, state, character_type, next_step, followup_view=followup
        )
        
        self.perks_list = data_loader.perks_list

        self.random_perks = []
        self.exclude_ids = []
        self.randomize()

        self.get_select(self.random_perks, "perk", 1, 4)
        self.get_replace_button("Selected Perks")
        self.get_accept_button()

    def get_message(self):
        msg = f'**{self.ctx.author.mention}**, these are your perks:'

        embeds = []
        for perk in self.random_perks:
            perk_name = perk["perk_data"][f"{self.character_type}_perk_name"]
            perk_owner = perk["perk_data"][f"{self.character_type}_owner_name"]
            perk_icon = perk["perk_data"][f"{self.character_type}_perk_icon"]

            embed = discord.Embed(
                title=perk_name,
                description=f"from *{perk_owner}*",
                color=discord.Color.dark_green()
            )
            embed.set_thumbnail(url=perk_icon)
            embeds.append(embed)

        if not self.next_step:
            embeds[-1].set_footer(text=f'Check out !{self.character_type}_setup too!')

        return {"content": msg, "embeds": embeds}
            
    def randomize(self):
        randomize_result = get_random_perks(
            self.perks_list, 
            self.random_perks, 
            self.character_type,
            self.exclude_ids
        )

        self.exclude_ids = randomize_result["exclude_ids"]
        self.random_perks = randomize_result["random_perks"]
    
    async def replace(self, interaction: discord.Interaction):
        for item in self.random_perks:
            item["replace"] = item["perk_data"][f"{self.character_type}_perk_id"] in self.selected_ids

        self.randomize()
        self.select.options = get_options_for_select(self.random_perks, "perk", self.character_type)

        msg = self.get_message()
        content = msg['content']
        embeds = msg['embeds']

        await interaction.response.edit_message(
            content=content,
            embeds=embeds,
            view=self
        )

    async def accept(self, interaction: discord.Interaction):
        self.state.perks = self.random_perks
        next_view = self.followup_view["view"](ctx=self.ctx,
                                               data_loader=self.data_loader,
                                               state=self.state,
                                               next_step=True)

        msg = next_view.get_message()
        content = msg['content']
        embeds = msg['embeds']

        await interaction.response.edit_message(
            content=content,
            embeds=embeds,
            view=next_view
        )

