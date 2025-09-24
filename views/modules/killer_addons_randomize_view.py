import discord
from utils.views_utils import get_options_for_select
from core.randomize_funcs import get_random_killer_addons_set
from views.modules.offering_randomize_view import OfferingRandomizeView
from core.data_loader import DataLoader
from core.state import SetupState
from views.randomize_view import BaseRandomizeView


class KillerAddonsRandomizeView(BaseRandomizeView):
    def __init__(self, ctx, data_loader: DataLoader, state: SetupState, next_step: bool = False):

        character_type = "killer"

        followup = {
            "killer": {"view": OfferingRandomizeView, "next_drawn": "offering"},
        }

        super().__init__(
            ctx, data_loader, state, character_type, next_step, followup_view=followup
        )

        self.addons_list = self.state.character["killer_addons"]

        self.random_addons_set = []
        self.exclude_ids = []
        self.selected_ids = []

        self.randomize()

        self.get_select(self.random_addons_set, "addon", 1, 2)
        self.get_replace_button("Selected Addons", self.replace_addons)
        self.get_accept_button()
            
    def get_message(self):
        msg = f'**{self.ctx.author.mention}**, your killer addon set:'

        embeds = []

        for addon in self.random_addons_set:
            addon_name = addon["addon_data"]["killer_addon_name"]
            addon_rarity = addon["addon_data"]["killer_addon_rarity"]
            addon_icon = addon["addon_data"]["killer_addon_icon"]

            embed = discord.Embed(
                title=addon_name,
                description=f"of *{addon_rarity}* rarity",
                color=discord.Color.dark_gold()
            )
            embed.set_thumbnail(url=addon_icon)
            embeds.append(embed)

        if not self.next_step:
            embeds[-1].set_footer(text=f'Check out !{self.character_type}_setup too!')

        return {"content": msg, "embeds": embeds}
                
    def randomize(self):
        randomize_result = get_random_killer_addons_set(
            all_addons_list=self.addons_list,
            initial_addons_list=self.random_addons_set,
            exclude_ids=self.exclude_ids
        )

        self.random_addons_set = randomize_result["random_addons"]
        self.exclude_ids = randomize_result["exclude_ids"]

    async def replace_addons(self, interaction: discord.Interaction):
        for item in self.random_addons_set:
            item["replace"] = item["addon_data"][f"{self.character_type}_addon_id"] in self.selected_ids

        self.randomize()
        self.select.options = get_options_for_select(self.random_addons_set, "addon", self.character_type)

        msg = self.get_message()
        content = msg['content']
        embeds = msg['embeds']

        await interaction.response.edit_message(
            content=content,
            embeds=embeds,
            view=self
        )

    async def accept(self, interaction: discord.Interaction):
        self.state.killer_addons = self.random_addons_set
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


