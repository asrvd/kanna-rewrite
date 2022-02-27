import discord
from discord.ext import commands
import aiohttp
from decouple import config
import json
import pyrebase

firebaseconfig=json.loads(config("FIREBASE_CONFIG"))
bid = str(config("CA_BID"))
key = str(config("CA_KEY"))

firebase = pyrebase.initialize_app(firebaseconfig)
db = firebase.database()

def create(gid, cid):
    db.child("CHATBOT").child(gid).child("SETUP").set({"ID":cid, "set":True})

def check(gid):
    if db.child("CHATBOT").child(gid).child("SETUP").child("set").get().val() == False or db.child("CHATBOT").child(gid).child("SETUP").child("set").get().val() == None:
        return False
    else:
        return True

def return_id(gid):
    return db.child("CHATBOT").child(gid).child("SETUP").child("ID").get().val()

class ChatBot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def chat_setup(self, ctx):
        msg = await ctx.send('Setting up new channel..')
        try:
            ch = await ctx.guild.create_text_channel(name="❤-chat-with-kanna")
            create(ctx.guild.id, ch.id)
            await msg.edit(content=f"Setup Complete, You can chat with kanna now in {ch.mention}.\nPlease make sure kanna has the permission to read messages in this channel.")
        except discord.Forbidden:
            await ctx.send("I don't have permissions to create a channel!")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def chat_disable(self, ctx):
        if check(ctx.guild.id):
            await ctx.send("Disabling chat..")
            db.child("CHATBOT").child(ctx.guild.id).child("SETUP").child("set").set(False)
            await ctx.send("`Chat-With-Kanna` disabled for this guild.\nSend `kana chat_enable` to enable it again.")
        else:
            await ctx.send("`Chat-With-Kanna` is not setup in this guild.")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def chat_enable(self, ctx):
        if check(ctx.guild.id):
            await ctx.send("`Chat-With-Kanna` is already setup in this guild.")
        else:
            await ctx.send("Enabling chat..")
            db.child("CHATBOT").child(ctx.guild.id).child("SETUP").child("set").set(True)
            await ctx.send("`Chat-With-Kanna` is now enabled for this guild.")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not check(message.guild.id):
            return
        chid = int(return_id(message.guild.id))
        if message.author.bot or message.channel.id != chid:
            return
        async with message.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://api.brainshop.ai/get?bid={bid}&key={key}&uid={message.author.id}&msg={message.content}") as resp:
                    if resp.status == 200:
                        cont = await resp.json()
                        await message.channel.send(cont["cnt"])

    @chat_setup.error
    async def chat_setup_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permission to do that. Required Perm: `Manage Server`")
        elif isinstance(error, discord.Forbidden):
            await ctx.send("Kanna doesn't have perms to do that. Please make sure kanna has the permission to manage channels.")
    
    @chat_disable.error
    async def chat_disable_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permission to do that. Required Perm: `Manage Server`")

    @chat_enable.error
    async def chat_enable_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permission to do that. Required Perm: `Manage Server`")

def setup(client):
    client.add_cog(ChatBot(client))
