import discord
from discord.ext import commands
from discord_slash import SlashCommand, cog_ext
import os
from PIL import Image
from io import BytesIO

from discord_slash.utils.manage_commands import create_option

gi=[843823778755641344]

class Avatar(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @cog_ext.cog_slash(name="hi", description="hi", guild_ids=[843823778755641344])
    async def hi(self, ctx):
        await ctx.send("hi!")

    @cog_ext.cog_slash(
        name="avatar", 
        description="Display a user's avatar.", 
        guild_ids=gi,
        options=[
            create_option(
                name="user1",
                description="user",
                option_type=6,
                required=False
            ),
            create_option(
                name="user2",
                description="user",
                option_type=6,
                required=False
            )
        ]
    )
    async def av(self, ctx, user1:discord.User=None, user2:discord.User=None):
        if user1 is None and user2 is None:
            u = ctx.author
            asset = u.avatar_url_as(size=512)
            await asset.save(f"images/generated/{u.id}.png")
            file = discord.File(f"images/generated/{u.id}.png", filename="pfp.png") 
            await ctx.send(file=file)
            os.remove(f"C:/Users/User/Desktop/kr/images/generated/{u.id}.png")
        elif user1 is not None and user2 is None:
            u = user1
            asset = u.avatar_url_as(size=512)
            await asset.save(f"images/generated/{u.id}.png")
            file = discord.File(f"images/generated/{u.id}.png", filename="pfp.png") 
            await ctx.send(file=file)
            os.remove(f"C:/Users/User/Desktop/kr/images/generated/{u.id}.png")
        elif user1 is None and user2 is not None:
            u = user2
            asset = u.avatar_url_as(size=512)
            await asset.save(f"images/generated/{u.id}.png")
            file = discord.File(f"images/generated/{u.id}.png", filename="pfp.png") 
            await ctx.send(file=file)
            os.remove(f"C:/Users/User/Desktop/kr/images/generated/{u.id}.png")
        elif user1 is not None and user2 is not None:
            bg = Image.new(mode="RGBA", size=(1000, 500))
            a1 = user1.avatar_url_as(size=512)
            a2 = user2.avatar_url_as(size=512)
            pfp1 = Image.open(BytesIO(await a1.read()))
            pfp2 = Image.open(BytesIO(await a2.read()))
            pfp1.resize((500, 500))
            pfp2.resize((500, 500))
            bg.paste(pfp1, (0, 0))
            bg.paste(pfp2, (500, 0))
            bg.save(f"images/generated/shared{user1.id}.png")
            file = discord.File(f"images/generated/shared{user1.id}.png", filename="shared.png")
            await ctx.send(file=file)
            os.remove(f"C:/Users/User/Desktop/kr/images/generated/shared{user1.id}.png")



def setup(client):
    client.add_cog(Avatar(client))
    print("Avatar Loaded.")
    
    