from typing import Union
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
from ._config import gi

class Card(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @slash_command(
        name="simpcard",
        description="Make a SimpCard (verified) for any person or thing UwU",
        guild_ids=gi
    )
    async def simpcard(self, ctx, user:Option(discord.User, "Choose this for User.", required=False), other:Option(str, "Choose this for any other thing to simp on.", required=False)):
        if user is not None and other is not None:
            await ctx.respond("You need to select any one of `User` or `Other`!", ephemeral=True)
            return
        q = user.name if user is not None and other is None else other
        bg = Image.open("images/assets/simp.png")
        font = ImageFont.truetype("fonts/roboto.ttf", 24)
        auth = ctx.author
        asset = auth.display_avatar.with_size(256)
        data = BytesIO(await asset.read())
        pfp = Image.open(data).convert('RGBA')
        pfp = pfp.resize((185, 214))
        nick = auth.display_name
        bg.paste(pfp, (47, 60))
        draw = ImageDraw.Draw(bg)
        draw.text((395, 172), nick, (0, 0, 0), font=font)
        draw.text((51, 349), q, (0, 0, 0), font=font)
        bg.save(f"images/generated/simp{ctx.author.id}.png")
        file = discord.File(f"images/generated/simp{ctx.author.id}.png")
        embed = discord.Embed(description=f"{ctx.author.mention} Here is your verified Simp Card.", color=0x2e69f2)
        embed.set_image(url=f"attachment://simp{ctx.author.id}.png")
        embed.set_footer(
            text=f"Kanna Chan",
        )
        await ctx.respond(embed=embed, file=file)
        os.system(f"rm -rf images/generated/simp{ctx.author.id}.png")

    @slash_command(
        name="uwucard",
        description="Create an UwUCard to show your love for a person UwU",
        guild_ids=gi
    )
    async def uwucard(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        await ctx.defer()
        bg = Image.open("images/assets/lob.png")
        asset = user.display_avatar.with_size(256)
        data = BytesIO(await asset.read())
        pfp = Image.open(data).convert('RGBA')
        pfp = pfp.resize((181, 201))
        bg.paste(pfp, (35, 121))
        bg.save(f"images/generated/uwu{ctx.author.id}.png")
        file = discord.File(f"images/generated/uwu{ctx.author.id}.png")
        embed = discord.Embed(description=f"{user.mention} you make {ctx.author.mention} happy uwu.", color=0x2e69f2)
        embed.set_image(url=f"attachment://uwu{ctx.author.id}.png")
        embed.set_footer(
            text=f"Kanna Chan"
        )
        await ctx.respond(embed=embed, file=file)
        os.system(f"rm -rf images/generated/uwu{ctx.author.id}.png")

    @slash_command(
        name="gaycard",
        description="Create a Verfied Gay Card for you :flushed:",
        guild_ids=gi
    )
    async def gaycard(self, ctx):
        await ctx.defer()
        bg = Image.open("images/assets/gay.png")
        font = ImageFont.truetype("fonts/roboto.ttf", 32)
        auth = ctx.author
        asset = auth.display_avatar.with_size(256)
        data = BytesIO(await asset.read())
        pfp = Image.open(data).convert('RGBA')
        pfp = pfp.resize((238, 238))
        nick = auth.display_name
        bg.paste(pfp, (76, 165))
        draw = ImageDraw.Draw(bg)
        draw.text((368, 193), nick, (0, 0, 0), font=font)
        bg.save(f"images/generated/gay{auth.id}.png")
        file = discord.File(f"images/generated/gay{auth.id}.png")
        embed = discord.Embed(description=f"{ctx.author.mention} Here is your verified Gay Card.", color=0x2e69f2)
        embed.set_image(url=f"attachment://gay{auth.id}.png")
        embed.set_footer(
            text=f"Kanna Chan",
        )
        await ctx.respond(embed=embed, file=file)
        os.system(f"rm -rf images/generated/gay{auth.id}.png")

class NCards(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def gaycard(self, ctx):
        bg = Image.open("images/assets/gay.png")
        font = ImageFont.truetype("fonts/roboto.ttf", 32)
        auth = ctx.author
        asset = auth.display_avatar.with_size(256)
        data = BytesIO(await asset.read())
        pfp = Image.open(data).convert('RGBA')
        pfp = pfp.resize((238, 238))
        nick = auth.display_name
        bg.paste(pfp, (76, 165))
        draw = ImageDraw.Draw(bg)
        draw.text((368, 193), nick, (0, 0, 0), font=font)
        bg.save(f"images/generated/gay{auth.id}.png")
        file = discord.File(f"images/generated/gay{auth.id}.png")
        embed = discord.Embed(description=f"{ctx.author.mention} Here is your verified Gay Card.", color=0x2e69f2)
        embed.set_image(url=f"attachment://gay{auth.id}.png")
        embed.set_footer(
            text=f"Kanna Chan",
        )
        await ctx.send(embed=embed, file=file)
        os.system(f"rm -rf images/generated/gay{auth.id}.png")

    @commands.command()
    async def uwucard(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        bg = Image.open("images/assets/lob.png")
        asset = user.display_avatar.with_size(256)
        data = BytesIO(await asset.read())
        pfp = Image.open(data).convert('RGBA')
        pfp = pfp.resize((181, 201))
        bg.paste(pfp, (35, 121))
        bg.save(f"images/generated/uwu{ctx.author.id}.png")
        file = discord.File(f"images/generated/uwu{ctx.author.id}.png")
        embed = discord.Embed(description=f"{user.mention} you make {ctx.author.mention} happy uwu.", color=0x2e69f2)
        embed.set_image(url=f"attachment://uwu{ctx.author.id}.png")
        embed.set_footer(
            text=f"Kanna Chan"
        )
        await ctx.send(embed=embed, file=file)
        os.system(f"rm -rf images/generated/uwu{ctx.author.id}.png")

    @commands.command()
    async def simpcard(self, ctx, u: Union[discord.User, str]):
        if u is None:
            await ctx.reply("Please include `What/Who` are you making this simpcard for?\nExample: `kana simpcard asheeshh` or `kana simpcard @SENSEI`.")
        elif isinstance(u, discord.User):
            print("true")
            simp_text = str(u)
        elif isinstance(u, str):
            simp_text = u
        bg = Image.open("images/assets/simp.png")
        font = ImageFont.truetype("fonts/roboto.ttf", 24)
        auth = ctx.author
        asset = auth.display_avatar.with_size(256)
        data = BytesIO(await asset.read())
        pfp = Image.open(data).convert('RGBA')
        pfp = pfp.resize((185, 214))
        bg.paste(pfp, (47, 60))
        draw = ImageDraw.Draw(bg)
        draw.text((395, 172), str(auth), (0, 0, 0), font=font)
        draw.text((51, 349), simp_text, (0, 0, 0), font=font)
        bg.save(f"images/generated/simp{ctx.author.id}.png")
        file = discord.File(f"images/generated/simp{ctx.author.id}.png")
        embed = discord.Embed(description=f"{ctx.author.mention} Here is your verified Simp Card.", color=0x2e69f2)
        embed.set_image(url=f"attachment://simp{ctx.author.id}.png")
        embed.set_footer(
            text=f"Kanna Chan",
        )
        await ctx.send(embed=embed, file=file)
        os.system(f"rm -rf images/generated/simp{ctx.author.id}.png")

def setup(client):
    client.add_cog(Card(client))
    client.add_cog(NCards(client))
    print(">> Cards Loaded.")