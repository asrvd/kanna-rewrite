import discord
from discord.ext import commands
from discord.ext.commands.core import check
import weeby
import requests
import json
from ._config import ec
import pyrebase
from decouple import config
import json

gif = weeby.Weeby(str(config("WTOKEN")))
kt = str(config("KTOKEN"))
firebaseconfig = json.loads(config("FIREBASE_CONFIG"))

firebase = pyrebase.initialize_app(firebaseconfig)
db = firebase.database()


def create(user):
    acs = ["SLAP", "KICK", "KISS", "PUNCH", "FLOWER", "BONK", "PAT", "HUG", "CUDDLE"]
    for ac in acs:
        db.child("ACTION").child(user).child(ac).set({"GIVEN": 0, "GOT": 0})


def add_action(user, arg: str, act: str):
    ref = {
        "s": "SLAP",
        "k": "KICK",
        "ki": "KISS",
        "p": "PUNCH",
        "f": "FLOWER",
        "b": "BONK",
        "pa": "PAT",
        "h": "HUG",
        "c": "CUDDLE",
    }
    val = db.child("ACTION").child(user).child(ref[arg]).child(act.upper()).get().val()
    db.child("ACTION").child(user).child(ref[arg]).update({f"{act.upper()}": val + 1})


def check_user(user):
    data = db.child("ACTION").child(user).get().val()
    if data is None:
        create(user)


def return_ac_val(user, arg: str):
    ref = {
        "s": "SLAP",
        "k": "KICK",
        "ki": "KISS",
        "p": "PUNCH",
        "f": "FLOWER",
        "b": "BONK",
        "pa": "PAT",
        "h": "HUG",
        "c": "CUDDLE",
    }
    got = db.child("ACTION").child(user).child(ref[arg]).child("GOT").get().val()
    given = db.child("ACTION").child(user).child(ref[arg]).child("GIVEN").get().val()
    # print(got, given)
    return got, given


def get_gif(type: str):
    url = f"https://kawaii.red/api/gif/{type}/token={kt}/"
    r = requests.get(url)
    return json.loads(r.content)["response"]


class RP(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kill(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} kills {u.display_name} *dies LMAO*",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=get_gif("kill"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def kiss(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        check_user(u.id)
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} kisses {u.display_name} *blush*",
            icon_url=ctx.author.display_avatar,
        )
        got, given = return_ac_val(u.id, "ki")
        emb.set_footer(
            text=f"✿ {u.display_name} kissed others {given} times and got kissed {got} times.\n✿ Made by Kanna Chan",
            icon_url=u.display_avatar,
        )
        emb.set_image(url=get_gif("kiss"))
        await ctx.send(embed=emb)
        add_action(u.id, "ki", "got")
        add_action(ctx.author.id, "ki", "given")

    @commands.command()
    async def wink(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} winks at {u.display_name} （〃｀ 3′〃）",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=gif.get_gif().gif(type="wink"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def lick(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(colr=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} licks {u.display_name} ˋ( ° ▽、° ) ",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=get_gif("lick"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def hug(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        check_user(u.id)
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} hugs {u.display_name} *aww*",
            icon_url=u.display_avatar,
        )
        got, given = return_ac_val(u.id, "h")
        emb.set_footer(
            text=f"✿ {u.display_name} hugged others {given} times and got hugged {got} times.\n✿ Made by Kanna Chan",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=get_gif("hug"))
        await ctx.send(embed=emb)
        add_action(u.id, "h", "got")
        add_action(ctx.author.id, "h", "given")

    @commands.command()
    async def highfive(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} highfives {u.display_name} 〜(￣▽￣〜)",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=gif.get_gif().gif(type="highfive"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def lurk(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} lurks {u.display_name} *who's there!*",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=gif.get_gif().gif(type="lurk"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def love(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} loves {u.display_name} uwu",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=gif.get_gif().gif(type="love"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def feed(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} feeds {u.display_name} *noms*",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=gif.get_gif().gif(type="feed"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def nom(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} noms {u.display_name} *noms*",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=get_gif("nom"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def handhold(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} holds {u.display_name}'s hands uwu",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=gif.get_gif().gif(type="handhold"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def poke(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} pokes {u.display_name} *poke poke*",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=get_gif("poke"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def pout(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} pouts at {u.display_name} ￣へ￣",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=gif.get_gif().gif(type="pout"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def slap(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        check_user(u.id)
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} slaps {u.display_name} *hurts*",
            icon_url=ctx.author.display_avatar,
        )
        got, given = return_ac_val(u.id, "s")
        emb.set_footer(
            text=f"✿ {u.display_name} slapped others {given} times and got slapped {got} times.\n✿ Made by Kanna Chan",
            icon_url=u.display_avatar,
        )
        emb.set_image(url=get_gif("slap"))
        await ctx.send(embed=emb)
        add_action(u.id, "s", "got")
        add_action(ctx.author.id, "s", "given")

    @commands.command()
    async def rawr(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} rawrs at {u.display_name} *rawrrr*",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=gif.get_gif().gif(type="rawr"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def punch(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        check_user(u.id)
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} punches {u.display_name} *hurts*",
            icon_url=ctx.author.display_avatar,
        )
        got, given = return_ac_val(u.id, "p")
        emb.set_footer(
            text=f"✿ {u.display_name} punched others {given} times and got punched {got} times.\n✿ Made by Kanna Chan",
            icon_url=u.display_avatar,
        )
        emb.set_image(url=get_gif("punch"))
        await ctx.send(embed=emb)
        add_action(u.id, "p", "got")
        add_action(ctx.author.id, "p", "given")

    @commands.command()
    async def stare(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} stares at {u.display_name} OwO",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=gif.get_gif().gif(type="stare"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def tease(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} teases {u.display_name} *hehe*",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=gif.get_gif().gif(type="tease"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def throw(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} throws {u.display_name} *yeeeet*",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=gif.get_gif().gif(type="throw"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def tickle(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} tickles {u.display_name} *starts crying..*",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=get_gif("tickle"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def cuddle(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        check_user(u.id)
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} cuddles {u.name} uwu",
            icon_url=ctx.author.display_avatar,
        )
        got, given = return_ac_val(u.id, "c")
        emb.set_footer(
            text=f"✿ {u.display_name} cuddled others {given} times and got cuddled {got} times.\n✿ Made by Kanna Chan",
            icon_url=u.display_avatar,
        )
        emb.set_image(url=get_gif("cuddle"))
        await ctx.send(embed=emb)
        add_action(u.id, "c", "got")
        add_action(ctx.author.id, "c", "given")

    @commands.command()
    async def bonk(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        check_user(u.id)
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} bonks {u.name} ＞︿＜",
            icon_url=ctx.author.display_avatar,
        )
        got, given = return_ac_val(u.id, "b")
        emb.set_footer(
            text=f"✿ {u.display_name} bonked others {given} times and got bonked {got} times.\n✿ Made by Kanna Chan",
            icon_url=u.display_avatar,
        )
        emb.set_image(url=gif.get_gif().gif(type="bonk"))
        await ctx.send(embed=emb)
        add_action(u.id, "b", "got")
        add_action(ctx.author.id, "b", "given")

    @commands.command()
    async def bite(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} bites {u.name} ＼(ﾟｰﾟ＼)",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=gif.get_gif().gif(type="bite"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def boop(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} boops {u.name} *boop boop*",
            icon_url=ctx.author.display_avatar,
        )
        emb.set_image(url=get_gif("boop"))
        await ctx.send(embed=emb)

    @commands.command()
    async def flower(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        check_user(u.id)
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} gives {u.display_name} a flower ✿",
            icon_url=ctx.author.display_avatar,
        )
        got, given = return_ac_val(u.id, "f")
        emb.set_footer(
            text=f"✿ {u.display_name} gave others {given} flowers has {got} flowers.\n✿ Made by Kanna Chan",
            icon_url=u.display_avatar,
        )
        emb.set_image(url=gif.get_gif().gif(type="flower"))
        await ctx.send(embed=emb)
        add_action(u.id, "f", "got")
        add_action(ctx.author.id, "f", "given")

    @commands.command()
    async def pat(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        check_user(u.id)
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{ctx.author.display_name} pats {u.display_name} uwu",
            icon_url=ctx.author.display_avatar,
        )
        got, given = return_ac_val(u.id, "pa")
        emb.set_footer(
            text=f"✿ {u.display_name} patted others {given} times and got pats {got} times.\n✿ Made by Kanna Chan",
            icon_url=u.display_avatar,
        )
        emb.set_image(url=get_gif("pat"))
        await ctx.send(embed=emb)
        add_action(u.id, "pa", "got")
        add_action(ctx.author.id, "pa", "given")

    @commands.command()
    async def baka(self, ctx, u: discord.User = None):
        if u == None:
            u = ctx.author
        emb = discord.Embed(color=ec)
        emb.set_author(
            name=f"{u.display_name} a bakaaaa!", icon_url=ctx.author.display_avatar
        )
        emb.set_image(url=gif.get_gif().gif(type="baka"))
        emb.set_footer(
            text=f"✿ Made by Kanna Chan", icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=emb)


def setup(client):
    client.add_cog(RP(client))
    print(">> Normal RP Loaded.")
