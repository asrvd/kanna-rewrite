import discord
from discord.ext import commands
from discord.ui import View, Button
import random
import aiohttp
import weeby
from petpetgif import petpet
from io import BytesIO
from ._config import ec
from decouple import config

w = weeby.Weeby(str(config("WTOKEN")))
ml=["memes", "meme", "MemeEconomy", "dankmemes"]

class MemeView(View):
    def __init__(self, ctx):
        super().__init__(timeout=10)
        self.ctx = ctx
    @discord.ui.button(label="Next", style=1)
    async def n_callback(self, button, interaction):
        embed=discord.Embed(title="Meme", color=ec)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://www.reddit.com/r/{random.choice(ml)}/new.json?sort=hot') as r:
                res = await r.json()
                print(res['data'])
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await interaction.response.edit_message(embed=embed)
    @discord.ui.button(label="Exit", style=2)
    async def e_callback(self, button, interaction):
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)
    async def interaction_check(self, interaction) -> bool:
        if interaction.user == self.ctx.author:
            return True
        await interaction.response.send_message("This message is not for you!", ephemeral=True)
        return False

class Memey(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kawaiirate(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        rate = random.randint(0, 101)
        embed = discord.Embed(description=f"> Kanna Chan used her legendary powers to calculate **{user.display_name}'s** KawaiiRate and found out that they are ||**{rate}%**|| kawaii uwu.", color=ec)
        embed.set_author(
            name=f"{ctx.author.display_name}'s KawaiiRate!",
            icon_url=ctx.author.display_avatar
        )
        embed.set_footer(
            text=f"● Requested by {ctx.author.display_name}\n● Made by Kanna Chan",
            icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def simprate(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        rate = random.randint(0, 101)
        embed = discord.Embed(description=f"> Kanna Chan used her legendary powers to calculate **{user.display_name}'s** SimpRate and found out that they are ||**{rate}%**|| simp.", color=ec)
        embed.set_author(
            name=f"{ctx.author.display_name}'s SimpRate!",
            icon_url=ctx.author.display_avatar
        )
        embed.set_footer(
            text=f"● Requested by {ctx.author.display_name}\n● Made by Kanna Chan",
            icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def gayrate(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        rate = random.randint(0, 101)
        embed = discord.Embed(description=f"> Kanna Chan used her legendary powers to calculate **{user.display_name}'s** GayRate and found out that they are ||**{rate}%**|| gay.", color=ec)
        embed.set_author(
            name=f"{ctx.author.display_name}'s GayRate!",
            icon_url=ctx.author.display_avatar
        )
        embed.set_footer(
            text=f"● Requested by {ctx.author.display_name}\n● Made by Kanna Chan",
            icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def tis(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        im = w.generate().spotify(url=user.display_avatar.url, hex=str(user.color).strip("#"), text=user.display_name)
        #print(user.color)
        dest = BytesIO(im)
        dest.seek(0)
        file = discord.File(dest, filename="tis.png")
        await ctx.send(file=file)

    @commands.command()
    async def tweet(self, ctx, text:str, *,user:discord.User=None):
        user = ctx.author if user is None else user
        im = w.generate().tweet(url=user.display_avatar.url, name=user.display_name, text=text)
        dest = BytesIO(im)
        dest.seek(0)
        file = discord.File(dest, filename="tweet.png")
        await ctx.send(file=file)

    @commands.command()
    async def spiderman(self, ctx, text1:str, text2:str):
        im = w.generate().two_text(type="spiderman", text1=text1, text2=text2)
        dest = BytesIO(im)
        dest.seek(0)
        file = discord.File(dest, filename="spidey.png")
        await ctx.send(file=file)

    @commands.command()
    async def buttons(self, ctx, text1:str, text2:str):
        im = w.generate().two_text(type="twobuttons", text1=text1, text2=text2)
        dest = BytesIO(im)
        dest.seek(0)
        file = discord.File(dest, filename="buttons.png")
        await ctx.send(file=file)

    @commands.command()
    async def bedcuddle(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        im = w.generate().two_image(type="cuddle", url1=ctx.author.display_avatar.url, url2=user.display_avatar.url)
        dest = BytesIO(im)
        dest.seek(0)
        file = discord.File(dest, filename="cuddle.png")
        await ctx.send(file=file)

    @commands.command()
    async def nani(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        im = w.generate().two_image(type="nani", url1=ctx.author.display_avatar.url, url2=user.display_avatar.url)
        dest = BytesIO(im)
        dest.seek(0)
        file = discord.File(dest, filename="nani.png")
        await ctx.send(file=file)

    @commands.command()
    async def batslap(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        im = w.generate().two_image(type="batslap", url1=ctx.author.display_avatar.url, url2=user.display_avatar.url)
        dest = BytesIO(im)
        dest.seek(0)
        file = discord.File(dest, filename="batslap.png")
        await ctx.send(file=file)

    @commands.command()
    async def bed(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        im = w.generate().two_image(type="bed", url1=ctx.author.display_avatar.url, url2=user.display_avatar.url)
        dest = BytesIO(im)
        dest.seek(0)
        file = discord.File(dest, filename="bed.png")
        await ctx.send(file=file)

    @commands.command()
    async def memehug(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        im = w.generate().two_image(type="hug", url1=ctx.author.display_avatar.url, url2=user.display_avatar.url)
        dest = BytesIO(im)
        dest.seek(0)
        file = discord.File(dest, filename="hug.png")
        await ctx.send(file=file)

    @commands.command()
    async def rip(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        asset = w.generate().rip(url=user.display_avatar.url, name=user.display_name, message="R.I.P")
        dest = BytesIO(asset)
        dest.seek(0)
        file = discord.File(dest, filename="rip.png")
        await ctx.send(file=file)

    @commands.command()
    async def eject(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        sussy = random.choice(["imposter", "notimposter", "ejected"])
        asset = w.generate().eject(url=user.display_avatar.url, text=user.display_name, outcome=sussy)
        dest = BytesIO(asset)
        dest.seek(0)
        file = discord.File(dest, filename="eject.gif")
        await ctx.send(file=file)

    @commands.command()
    async def gay(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        asset = w.set_overlay().overlay(type="rainbow", image_url=ctx.author.display_avatar.url)
        dest = BytesIO(asset)
        dest.seek(0)
        file = discord.File(dest, filename="gay.png")
        await ctx.send(file=file)

    @commands.command()
    async def triggered(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        asset = w.generate().triggered(url=user.display_avatar.url, tint=True)
        dest = BytesIO(asset)
        dest.seek(0)
        file = discord.File(dest, filename="triggered.gif")
        await ctx.send(file=file)

    @commands.command()
    async def meme(self, ctx):
        embed=discord.Embed(title="Meme", color=ec)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://www.reddit.com/r/{random.choice(ml)}/new.json?sort=hot') as r:
                res = await r.json()
                print(res['data']['children'][random.randint(0, 25)]['data'])
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                view=MemeView(ctx)
                msg = await ctx.send(embed=embed, view=view)
                async def timeout():
                    for btn in view.children:
                        btn.disabled=True
                    await msg.edit(view=view)
                view.on_timeout=timeout

    @commands.command()
    async def headpat(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        asset = user.display_avatar
        await asset.save('av.png')
        dest = BytesIO()
        petpet.make('av.png', dest)
        dest.seek(0)
        file = discord.File(dest, filename="pat.gif")
        await ctx.send(file=file)

def setup(client):
    client.add_cog(Memey(client))
    print(">> Normal Meme Loaded.")