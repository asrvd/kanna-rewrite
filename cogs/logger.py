import discord
from discord.ext import commands
from ._embed import get_logger_embed 

class Logger(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        emb = get_logger_embed("j", guild)
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
        emb = get_logger_embed("r", guild)
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