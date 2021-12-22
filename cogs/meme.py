import discord
from discord.ext import commands
from discord.commands import slash_command
from petpetgif import petpet
from io import BytesIO
import os
import aiohttp
import random

gi=[843823778755641344]
ml=["memes", "meme", "MemeEconomy", "dankmemes"]

class Meme(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @slash_command(
        name = "headpat",
        description = "Generates a HeadPat GIF using avatar",
        guild_ids=gi,
    )
    async def headpat(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        asset = user.display_avatar
        await asset.save('av.png')
        dest = BytesIO()
        petpet.make('av.png', dest)
        dest.seek(0)
        file = discord.File(dest, filename="pat.gif")
        await ctx.respond(file=file)
        #os.remove(dest)

    @slash_command(
        name="meme",
        description="Get a random meme.",
        guild_ids=gi
    )
    async def meme(self, ctx):
        embed=discord.Embed(title="Meme")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://www.reddit.com/r/{random.choice(ml)}/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.respond(embed=embed)

        
def setup(client):
    client.add_cog(Meme(client))
    print("Meme Loaded.")