from discord import Spotify, emoji
from discord.commands import slash_command
from discord.enums import ButtonStyle
from discord.ui import Button, View
from discord.ext import commands
import discord
from ._config import gi


class UserSpotify(commands.Cog):
    def __init__(self, client):
        self.client = client
    @slash_command(
        name="spotify",
        description="get a user's Spotify Playing Info",
        guild_ids=gi
    )
    async def spotify(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    embed = discord.Embed(color = activity.color)
                    embed.set_thumbnail(url=activity.album_cover_url)
                    desc = ""
                    for i in range(0, len(activity.artists)):
                        if i == 0:
                            desc = activity.artists[i]
                        else:
                            desc = desc + ", " + activity.artists[i]
                    embed.add_field(name="Track", value=f"*{activity.title}*")
                    embed.add_field(name="Artists", value=f"*{desc}*", inline=False)
                    embed.add_field(name="Album", value=f"*{activity.album}*")
                    embed.add_field(name="Duration", value=f"**{activity.duration.seconds//60}:{activity.duration.seconds%60}**")
                    embed.set_author(
                        name=f"{user.name.capitalize()}'s Spotify Activity",
                        icon_url=user.display_avatar
                    )
                    view = View()
                    button = Button(label="Listen on Spotify", style=ButtonStyle.url, url=activity.track_url, emoji=discord.PartialEmoji(name="spotify", id=923937275522473984))
                    view.add_item(button)
                    await ctx.respond(embed=embed, view=view)

def setup(client):
    client.add_cog(UserSpotify(client))
    print(">> Spotify loaded.")
