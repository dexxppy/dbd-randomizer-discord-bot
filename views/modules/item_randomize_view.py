import discord
from utils.views_utils import get_options_for_select
from core.randomize_funcs import get_random_item_addons_set, get_random_item_with_addons
from views.modules.offering_randomize_view import OfferingRandomizeView
from core.data_loader import DataLoader
from core.state import SetupState
from views.randomize_view import BaseRandomizeView


class ItemRandomizeView(BaseRandomizeView):
    def __init__(self, ctx, data_loader: DataLoader, state: SetupState, next_step: bool = False):

        character_type = "survivor"

        followup = {
            "survivor": {"view": OfferingRandomizeView, "next_drawn": "offering"}
        }

        super().__init__(
            ctx, data_loader, state, character_type, next_step, followup_view=followup
        )

        items_data = self.data_loader.items_list
        self.items_list = items_data["items"]
        self.addons_list = items_data["addons"]

        self.random_item_set = None
        self.exclude_ids_items = []
        self.exclude_ids_addons = []

        self.randomize()

        self.get_select(self.random_item_set["addons"], "addon", 1, 2)
        self.get_replace_button("Item", self.replace_item)
        self.get_replace_button("Selected Addons", self.replace_addons)
        self.get_accept_button()

    def get_message(self):
        msg = f'**{self.ctx.author.mention}**, your item set: '

        embeds = []

        item = self.random_item_set["item"]
        addons = self.random_item_set["addons"]

        item_name = item["survivor_item_name"]
        item_desc = item["survivor_item_rarity"]
        item_icon = item["survivor_item_icon"]

        item_embed = discord.Embed(
            title=item_name,
            description=f"of *{item_desc}* rarity",
            color=discord.Color.dark_orange()
        )
        item_embed.set_thumbnail(url=item_icon)
        embeds.append(item_embed)

        for addon in addons:
            addon_name = addon["addon_data"]["survivor_addon_name"]
            addon_rarity = addon["addon_data"]["survivor_addon_rarity"]
            addon_icon = addon["addon_data"]["survivor_addon_icon"]

            embed = discord.Embed(
                title=addon_name,
                description=f"of *{addon_rarity}* rarity",
                color=discord.Color.dark_gold()
            )
            embed.set_thumbnail(url=addon_icon)
            embeds.append(embed)

        if not self.next_step:
            embeds[0].set_footer(text=f'Check out !{self.character_type}_setup too!')

        return {"content": msg, "embeds": embeds}

    def randomize(self):
        randomize_result = get_random_item_with_addons(
            all_items_list=self.items_list,
            all_addons_list=self.addons_list,
            exclude_ids_item=self.exclude_ids_items,
            exclude_ids_addons=self.exclude_ids_addons
        )

        self.random_item_set = randomize_result["random_item_set"]
        self.exclude_ids_items = randomize_result["exclude_ids_item"]
        self.exclude_ids_addons = randomize_result["exclude_ids_addons"]
                
    def randomize_items_addons_set(self):
        randomize_result = get_random_item_addons_set(
            all_addons_list=self.addons_list,
            initial_addons_list=self.random_item_set["addons"],
            item_family_name=self.random_item_set["item"]["survivor_item_family"],
            exclude_ids=self.exclude_ids_addons
        )
        
        self.random_item_set["addons"] = randomize_result["random_addons"]
        self.exclude_ids_addons = randomize_result["exclude_ids"]
    
    async def replace_item(self, interaction: discord.Interaction):
        self.exclude_ids_addons = []
        self.randomize()

        self.select.options = get_options_for_select(self.random_item_set["addons"], "addon", self.character_type)

        msg = self.get_message()
        content = msg['content']
        embeds = msg['embeds']

        await interaction.response.edit_message(
            content=content,
            embeds=embeds,
            view=self
        )
        
    async def replace_addons(self, interaction: discord.Interaction):
        for item in self.random_item_set["addons"]:
            item["replace"] = item["addon_data"][f"{self.character_type}_addon_id"] in self.selected_ids
            
        self.randomize_items_addons_set()
        self.select.options = get_options_for_select(self.random_item_set["addons"], "addon", self.character_type)

        msg = self.get_message()
        content = msg['content']
        embeds = msg['embeds']

        await interaction.response.edit_message(
            content=content,
            embeds=embeds,
            view=self
        )

    async def accept(self, interaction: discord.Interaction):
        self.state.item = self.random_item_set
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
        

