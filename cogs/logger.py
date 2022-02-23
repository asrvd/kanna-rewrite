import discord
from discord.ext import commands
from ._embed import get_logger_embed
import datetime
import calendar
from ._config import ec

def get_unix(date: datetime.datetime):
    u = calendar.timegm(date.utctimetuple())
    return f"<t:{u}:R>"

class Logger(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        emb = discord.Embed(description=f"● Guild Name: {guild.name}\n● Member Count: {len(guild.members)}\n● Owner: {guild.owner.name}\n● Region: {guild.region}\n● Created At: {get_unix(guild.created_at)}", color=ec)
        emb.timestamp = datetime.datetime.utcnow()
        emb.set_thumbnail(url=guild.icon.url if guild.icon else None)
        emb.set_author(
            name=f"Kanna joined a new Guild",
            icon_url=guild.icon_url
        )
        emb.set_footer(
            text=f"Auto Logger | {guild.id}",
            icon_url=self.client.user.display_avatar
        )
        channel = self.client.get_channel(945941318671138866)
        await channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        emb = discord.Embed(description=f"● Guild Name: {guild.name}\n● Member Count: {len(guild.members)}\n● Owner: {guild.owner.name}\n● Region: {guild.region}\n● Created At: {get_unix(guild.created_at)}", color=ec)
        emb.timestamp = datetime.datetime.utcnow()
        emb.set_thumbnail(url=guild.icon.url if guild.icon else None)
        emb.set_author(
            name=f"Kanna was removed from a Guild",
            icon_url=guild.icon.url
        )
        emb.set_footer(
            text=f"Auto Logger | {guild.id}",
            icon_url=self.client.user.display_avatar
        )
        channel = self.client.get_channel(945941318671138866)
        await channel.send(embed=emb)


def setup(client):
    client.add_cog(Logger(client))
    print(">> Logger Loaded.")