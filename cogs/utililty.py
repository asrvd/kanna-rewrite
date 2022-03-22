import discord
from discord import Spotify
from discord.embeds import Embed
from discord.enums import ButtonStyle
from discord.ext import commands
from discord.ui import Button, View
from discord.commands import slash_command
import aiohttp
import json
from discord.ui.button import button
from weeby import Weeby
from ._config import gi, ec
from ._anime import get_anime_info
import asyncio
import pyrebase
from decouple import config
import json

w = Weeby(str(config("WTOKEN")))
firebaseconfig=json.loads(config("FIREBASE_CONFIG"))
R_KEY = config("RKEY")

firebase = pyrebase.initialize_app(firebaseconfig)
db = firebase.database()

def create(guild, channel):    #stores guild ID and channel ID
    db.child("WELCOME").child(guild).set({"CHANNEL": channel})
    
def remove(guild):
    db.child("WELCOME").child(guild).remove()

def return_channel(guild):     #returns channel ID
    channel = db.child("WELCOME").child(guild).child("CHANNEL").get().val()
    if channel == None:
        return None
    else:
        return channel

def afcreate(id, guild,  message):
    db.child("AFKUTIL").child(id).child(guild).set({"AFK": True, "MESSAGE": message})

def checkafk(id, guild):
    check = db.child("AFKUTIL").child(id).child(guild).child("AFK").get().val()
    if check == None or check == False:
        return False
    elif check == True:
        return True

def get_afk_message(id, guild):
    message = db.child("AFKUTIL").child(id).child(guild).child("MESSAGE").get().val()
    return message

def remove_afk(id, guild):
    db.child("AFKUTIL").child(id).child(guild).remove()

class Util(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(
        name="define",
        description="Define any word using Urban Dictionary."
    )
    async def define(self, ctx, *query: str):
        if query == None:
            await ctx.respond("You need to provide a Query to get the defintion!", ephemeral=True)
        else:
            async with aiohttp.ClientSession() as cs:
                url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
                querystring = {"term":f"{query}"}
                headers = {
                    'x-rapidapi-key': "6d59309ca9msh8800e69e9f7434ep19edb6jsn6986daa39884",
                    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
                }
                async with cs.get(url, params=querystring, headers=headers) as r:
                    res = await r.json()
                    list = res["list"]
                    #print(res)
                    if list == []:
                        await ctx.respond("No results available for this query ;-;", ephemeral=True)
                    else:
                        jtext = res["list"][0]["definition"]
                        example = res["list"][0]["example"]
                        emb = discord.Embed(description=f"{jtext}\n\n*`{example}`*\n", color=0x2e69f2)
                        emb.set_author(name=f"Definition Of {query.capitalize()}", icon_url=ctx.author.display_avatar)
                        view = View()
                        btn = Button(label="More Results", url=f"http://{query.lower().replace(" ", "%20")}.urbanup.com")
                        view.add_item(btn)
                        emb.set_footer(text="Kanna Chan")
                        await ctx.respond(embed=emb, view=view)
    
    @slash_command(
        name="lyrics",
        description="Get the lyrics of any Song!"
    )
    async def lyrics(self, ctx, song:str):
        await ctx.defer()
        ly = w.get_json_response().lyrics(track=song)
        #print(ly)
        view = View()
        button=Button(label="Play on Spotify", style=ButtonStyle.url, url=ly['track']['media'][0]['url'], emoji=discord.PartialEmoji(name="spotify", id=923937275522473984))
        view.add_item(button)
        embed = discord.Embed(description=ly['lyrics'])
        embed.set_author(
            name=f"{ly['track']['name']} ~ {ly['artist']['name']}",
            icon_url=ctx.author.display_avatar
        )
        embed.set_thumbnail(url=ly['track']['thumbnail'])

        await ctx.respond(embed=embed, view=view)

    @slash_command(
        name="anime",
        description="Get info about any anime."
    )
    async def anime(self, ctx, *, name:str):
        emb = await get_anime_info(arg=name, user=ctx.author)
        if isinstance(emb, discord.Embed):
            emb.set_footer(
                text=f"❀ Requested by {ctx.author.display_name}\n❀ Made by Kanna Chan",
                icon_url=self.client.user.display_avatar
            )
            await ctx.respond(embed=emb)
        else:
            await ctx.respond("No anime with this name found!")


class NUtility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['df', 'def'])
    async def define(self, ctx, *, query: str):
        if query == None:
            await ctx.reply("You need to provide a Query to get the defintion!")
        else:
            async with aiohttp.ClientSession() as cs:
                url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
                querystring = {"term":f"{query}"}
                headers = {
                    'x-rapidapi-key': f"{str(R_KEY)}",
                    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
                }
                async with cs.get(url, params=querystring, headers=headers) as r:
                    res = await r.json()
                    list = res["list"]
                    #print(res)
                    if list == []:
                        await ctx.reply("No results available for this query ;-;")
                    else:
                        jtext = res["list"][0]["definition"]
                        example = res["list"][0]["example"]
                        emb = discord.Embed(description=f"{jtext}\n\n*`{example}`*\n", color=ec)
                        emb.set_author(name=f"Definition Of {query.capitalize()}", icon_url=ctx.author.display_avatar)
                        view = View()
                        btn = Button(label="More Results", url=f"http://{query.lower()}.urbanup.com")
                        view.add_item(btn)
                        emb.set_footer(
                            text=f"❀ Requested by {ctx.author.display_name}\n❀ Made by Kanna Chan",
                            icon_url=self.client.user.display_avatar
                        )
                        await ctx.send(embed=emb, view=view)

    @commands.command()
    async def anime(self, ctx, *, name:str):
        emb = await get_anime_info(arg=name, user=ctx.author)
        if isinstance(emb, discord.Embed):
            emb.set_footer(
                text=f"❀ Requested by {ctx.author.display_name}\n❀ Made by Kanna Chan",
                icon_url=self.client.user.display_avatar
            )
            await ctx.reply(embed=emb)
        else:
            await ctx.reply("No anime with this name found!")

    @commands.command()
    async def lyrics(self, ctx, *, song:str):
        try:
            ly = w.get_json_response().lyrics(track=song)
            #print(ly)
            view = View()
            button=Button(label="Play on Spotify", style=ButtonStyle.url, url=ly['track']['media'][0]['url'], emoji=discord.PartialEmoji(name="spotify", id=923937275522473984))
            view.add_item(button)
            embed = discord.Embed(description=ly['lyrics'], color=ec)
            embed.set_author(
                name=f"{ly['track']['name']} ~ {ly['artist']['name']}",
                icon_url=ctx.author.display_avatar
            )
            embed.set_thumbnail(url=ly['track']['thumbnail'])

            await ctx.send(embed=embed, view=view)
        except KeyError:
            await ctx.send("No lyrics found for this Song!")

    @commands.command()
    async def spotify(self, ctx, user:discord.User=None):
        await ctx.reply("This command isn't available for now.")
        #user = ctx.author if user is None else user
        #if user.activities:
            #for activity in user.activities:
                #if isinstance(activity, Spotify):
                    #embed = discord.Embed(color = activity.color)
                    #embed.set_thumbnail(url=activity.album_cover_url)
                    #desc = ""
                    #for i in range(0, len(activity.artists)):
                        #if i == 0:
                            #desc = activity.artists[i]
                        #else:
                            #desc = desc + ", " + activity.artists[i]
                    #embed.add_field(name="Track", value=f"*{activity.title}*")
                    #embed.add_field(name="Artists", value=f"*{desc}*", inline=False)
                    #embed.add_field(name="Album", value=f"*{activity.album}*")
                    #embed.add_field(name="Duration", value=f"**{activity.duration.seconds//60}:{activity.duration.seconds%60}**")
                    #embed.set_author(
                        #name=f"{user.name.capitalize()}'s Spotify Activity",
                        #icon_url=user.display_avatar
                    #)
                    #view = View()
                    #button = Button(label="Listen on Spotify", style=ButtonStyle.url, url=activity.track_url, emoji=discord.PartialEmoji(name="spotify", id=923937275522473984))
                    #view.add_item(button)
                    #await ctx.send(embed=embed, view=view)
                #else:
                    #await ctx.reply("No Spotify activity found!")

    @commands.command()
    async def afk(self, ctx, *, message:str=None):
        if message == None:
            message = "AFK"
        nick = ctx.author.display_name
        new_nick = "[AFK] " + nick
        try:
            await ctx.author.edit(nick = new_nick)
            afcreate(ctx.author.id, ctx.guild.id, message)
            await ctx.reply(f"`{ctx.author.name}` your AFK has been set: {message}")
        except Exception:
            afcreate(ctx.author.id, ctx.guild.id, message)
            await ctx.reply(f"`{ctx.author.name}` your AFK has been set: {message}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if checkafk(message.author.id, message.guild.id):
            remove_afk(message.author.id, message.guild.id)
            await message.reply(f"Welcome back! your AFK has been removed", delete_after=10)
            new_nick = message.author.display_name.strip("[AFK]")
            await message.author.edit(nick=new_nick)
        for mention in message.mentions:
            if checkafk(mention.id, message.guild.id):
                if message.author.bot:
                    return
                else:
                    note = get_afk_message(mention.id, message.guild.id)
                    await message.reply(
                    f"`{mention}` is AFK: `{note}`", delete_after=10)


def setup(client):
    client.add_cog(Util(client))
    client.add_cog(NUtility(client))
    print(">> Utility Loaded.")
