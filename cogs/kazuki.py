'''
special and personal cog made for logging in 
kazuki discord server
'''

import discord
from discord.ext import commands
from ._config import ec
import datetime


class Kazuki(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.log_channel = 956421521050583100
        self.kazuki = 785024897863647282

    async def handle_ghost_ping(self, message, channel):
        if len(message.mentions) > 0:
            pinged_users = ""
            mention_str = ""
            for mem in message.mentions:
                if not mem.bot:
                    pinged_users += mem + " "
                    mention_str += mem.mention + " "
            emb = discord.Embed( 
                description=f"",
                color=ec
            )
            emb.add_field(
                name="User",
                value=message.author,
                inline=True
            )
            emb.add_field(
                name="Users Pinged",
                value=pinged_users.strip(),
                inline=True
            )
            emb.add_field(
                name="Message",
                value=message.content,
                inline=False
            )
            emb.set_author(
                name="Ghost Ping Found!!",
                icon_url = self.client.user.display_avatar
            )
            emb.timestamp = datetime.datetime.utcnow()
            await channel.send(mention_str, embed=emb)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild.id == self.kazuki:
            channel = self.client.get_channel(self.log_channel)
            await self.handle_ghost_ping(message, message.channel)
            emb = discord.Embed(description=message.content, color=ec)
            emb.set_author(
                name="Message Deleted!",
                icon_url = self.client.user.display_avatar
            )
            emb.timestamp = datetime.datetime.utcnow()
            await channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.guild.id == self.kazuki:
            channel = self.client.get_channel(self.log_channel)
            emb = discord.Embed(color=ec)
            emb.add_field(
                name="Before",
                value=before.content
            )
            emb.add_field(
                name="After",
                value=after.content
            )
            emb.set_author(
                name="Message Edited!",
                icon_url = self.client.user.display_avatar
            )
            emb.timestamp = datetime.datetime.utcnow()
            await channel.send(embed=emb)

def setup(client):
    client.add_cog(Kazuki(client))
    print(">> Kazuki Loaded.")
