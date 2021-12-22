import discord
from discord.commands import slash_command
from discord.ui import Button, View
from discord.ext import commands
from ._embed import get_embed

gi=[843823778755641344]


class MarryView(View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
    @discord.ui.button(label="Yes", style=3, emoji="✅")
    async def yes_callback(self, button, interaction):
        for button in self.children:
            button.disabled = True
        emb = get_embed("a", self.ctx)
        await interaction.response.edit_message(embed=emb, view=self)
    @discord.ui.button(label="No", style=4, emoji="❎")
    async def no_callback(self, button, interaction):
        for button in self.children:
            button.disabled = True
        emb = get_embed("d", self.ctx)
        await interaction.response.edit_message(embed=emb, view=self)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user == self.ctx.author:
            #await interaction.response.send_message("NO", ephemeral=True)
            return True
        else:
            return True
    
class Button(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mr(self, ctx, u:discord.User=None):
        if u is None:
            u = ctx.author
        view = MarryView(ctx)
        await ctx.send("Marriage Proposal", view=view)

    @slash_command(name="marry", description="Virtually marry a person uwu", guild_ids=gi)
    async def s(self, ctx, u:discord.User):
        #if u == ctx.author:
            #await ctx.respond("You `can't` marry yourself. I `won't` allow it.")
        #elif u.bot:
            #await ctx.respond("You `can't` marry a BOT please..")
        #else:
            e = get_embed("m", ctx, u)
            view = MarryView(ctx)
            await ctx.respond(u.mention, embed=e, view=view)


def setup(client):
    client.add_cog(Button(client))
    print(">> Button Loaded.")

        