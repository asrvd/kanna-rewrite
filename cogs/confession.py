'''Confession Cog
Made and Released only for WeebHub Server.
Not avaialable for people not in WeebHub Server.
'''

import discord
from discord.ext import commands
from discord.ui import View, Button
import pyrebase
import datetime
from decouple import config
from ._config import ec
import json

fr = pyrebase.initialize_app(json.loads(config("FIREBASE_CONFIG")))
db = fr.database()
mod_list = [
    767018851585490994, 
    695110624891371632, 
    503466945950253066,
    690204262201950230,
    452910515954515990,
    784363251940458516,
    499090668023578632
]

## Database Functions
def add_confession(id, message):
    db.child("CONFESSIONS").child(id).set({"MESSAGE": message})

def get_confession(id):
    msg = db.child("CONFESSIONS").child(id).child("MESSAGE").get().val()
    if msg is not None:
        return msg
    elif msg is None:
        return None

def remove_confession(id):
    db.child("CONFESSIONS").child(id).remove()

## Main View
class ConfView(View):
    def __init__(self, cs, cl):
        super().__init__(timeout=None)
        self.cs = cs
        self.cl = cl

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success)
    async def a_callback(self, button, interaction):
        msg = get_confession(interaction.message.id)
        emb = discord.Embed(description=msg, color=ec)
        emb.set_author(
            name="WeebHub Confessions",
            icon_url=interaction.guild.icon
        )
        emb.set_footer(
            text="Send `k.confess your_confession` in my DM to confess.\nMade by Kanna Chan",
            icon_url=self.cl.display_avatar
        )
        emb.timestamp=datetime.datetime.utcnow()
        await self.cs.send(embed=emb)
        for btn in self.children:
            btn.disabled=True
        await interaction.response.edit_message(content=f"`Approved by {interaction.user}.`", view=self)
        remove_confession(interaction.message.id)

    @discord.ui.button(label="Disapprove", style=discord.ButtonStyle.danger)
    async def d_callback(self, button, interaction):
        for btn in self.children:
            btn.disabled=True
        await interaction.response.edit_message(content=f"`Disapproved by {interaction.user}.`", view=self)
        remove_confession(interaction.message.id)

## Commands
class Confess(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def confess(self, ctx, *, content):
        guild = self.client.get_guild(864220272444571658)
        #if guild.get_member(ctx.author.id) != None:
        if ctx.channel.type is discord.ChannelType.private:
            cs = self.client.get_channel(879271125228593152)
            ca = self.client.get_channel(879270880553865246)
            await ctx.reply("Confession Sent. Please wait for Approval.")
            view = ConfView(cs, self.client.user)
            emb = discord.Embed(description=content, color=ec)
            emb.set_author(
                name="New Confession!",
                icon_url=guild.icon
            )
            emb.set_footer(
                text="In case Interaction fails please approve manually using `kana aaprove message_id` command.",
                icon_url=self.client.user.display_avatar
            )
            emb.timestamp = datetime.datetime.utcnow()
            msg = await ca.send(embed=emb, view=view)
            add_confession(msg.id, content)
        else:
            await ctx.reply("This command can only be used in DMs")
        #else:
            #await ctx.reply("This command is not available for all the servers.")

    @commands.command()
    async def approve(self, ctx, id: int=None):
        if id is None:
            await ctx.reply("Please provide the id of message to approve! `kana approve id`")
        else:
            if ctx.author.id in mod_list:   
                msg = get_confession(int(id))
                mg = await ctx.fetch_message(int(id))
                if msg != None:
                    cs = self.client.get_channel(879271125228593152)
                    await cs.send(msg)
                    await ctx.reply("✅ Approved the Confession!")
                    await mg.edit(f"`Approved by {ctx.author}.`", view=None)
                else:
                    await ctx.reply("No confession found with this ID!")
            else:
                await ctx.reply("You are not allowed to use this command.")


def setup(client):
    client.add_cog(Confess(client))
    print(">> Confession Loaded.")

