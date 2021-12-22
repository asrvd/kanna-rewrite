import discord
from discord.commands import slash_command
import requests
import json
from discord.ext import commands

gi=[843823778755641344]

class Image(commands.Cog):
    def __init__(self, client):
        self.client=client

    @slash_command(name="meow", description="Get random catto image nya~", guild_ids=gi)
    async def meow(self, ctx):
        res = requests.get("https://api.thecatapi.com/v1/images/search")
        await ctx.respond(json.loads(res.content)[0]['url'])

    @slash_command(name="woof", description="Get random doggo image nya~", guild_ids=gi)
    async def woof(self, ctx):
        res = requests.get("https://api.thedogapi.com/v1/images/search")
        await ctx.respond(json.loads(res.content)[0]['url'])

def setup(client):
    client.add_cog(Image(client))
    print(">> Image Loaded.")