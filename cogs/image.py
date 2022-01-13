import discord
from discord.commands import slash_command
from discord.commands.commands import command
from discord.ui import View, Button
import requests
import json
from discord.ext import commands
from ._config import gi

class ImageView(View):
    def __init__(self, ctx, arg):
        super().__init__(timeout=10)
        self.ctx = ctx
        self.arg = arg
    @discord.ui.button(label="Next", style=1)
    async def n_callback(self, button, interaction):
        res = requests.get("https://api.thecatapi.com/v1/images/search") if self.arg == "c" else requests.get("https://api.thedogapi.com/v1/images/search")
        await interaction.response.edit_message(content=json.loads(res.content)[0]['url'])
    @discord.ui.button(label="Exit", style=2)
    async def e_callback(self, button, interaction):
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This message is not for you!", ephemeral=True)
            return False
        else:
            return True
    async def on_timeout(self):
        for button in self.children:
            button.disabled = True
        await self.ctx.edit(view=self)


class Image(commands.Cog):
    def __init__(self, client):
        self.client=client

    @slash_command(
        name="meow", 
        description="Get random catto image nya~", 
        guild_ids=gi
    )
    async def meow(self, ctx):
        res = requests.get("https://api.thecatapi.com/v1/images/search")
        view=ImageView(ctx, "c")
        await ctx.respond(json.loads(res.content)[0]['url'], view=view)

    @slash_command(
        name="woof",
        description="Get random doggo image nya~", 
        guild_ids=gi
    )
    async def woof(self, ctx):
        res = requests.get("https://api.thedogapi.com/v1/images/search")
        view=ImageView(ctx, "d")
        await ctx.respond(json.loads(res.content)[0]['url'], view=view)

class NImage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def meow(self, ctx):
        res = requests.get("https://api.thecatapi.com/v1/images/search")
        view=ImageView(ctx, "c")
        msg = await ctx.send(json.loads(res.content)[0]['url'], view=view)
        async def timeout():
            for btn in view.children:
                btn.disabled=True
            await msg.edit(view=view)
        view.on_timeout = timeout

    @commands.command()
    async def woof(self, ctx):
        res = requests.get("https://api.thedogapi.com/v1/images/search")
        view=ImageView(ctx, "d")
        msg = await ctx.send(json.loads(res.content)[0]['url'], view=view)
        async def timeout():
            for btn in view.children:
                btn.disabled=True
            await msg.edit(view=view)
        view.on_timeout = timeout

def setup(client):
    client.add_cog(Image(client))
    client.add_cog(NImage(client))
    print(">> Image Loaded.")