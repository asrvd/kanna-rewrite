from datetime import time
import discord
from discord import message
from discord.commands.commands import command
from discord.ext import commands
from discord.guild import MISSING
from discord.ui import View, Button, Select, view
from discord.commands import slash_command
from ._config import ec, gi
from ._helpembed import get_help_embed

options = [
    discord.SelectOption(
        label="Moderation", description="List of Moderation Commands.", emoji=discord.PartialEmoji(name="mod", id=928226643607183421)
    ),
    discord.SelectOption(
        label="Utility", description="List of Utility Commands", emoji=discord.PartialEmoji(name="util", id=928226643250663454)
    ),
    discord.SelectOption(
        label="Games", description="List of Games available.", emoji=discord.PartialEmoji(name="game", id=928226643439419412)
    ),
    discord.SelectOption(
        label="Fun", description="List of Fun Commands.", emoji=discord.PartialEmoji(name="fun", id=928226643363901441)
    ),
    discord.SelectOption(
        label="Memes", description="List of Meme Commands.", emoji=discord.PartialEmoji(name="meme", id=928226643821080576)
    ),
]


class HelpView(View):
    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.ctx=ctx

    @discord.ui.select(
        placeholder="Select any Category",
        min_values=1,
        max_values=1,
        options=options,
    )
    async def callback(self, select, interaction):
        emb = get_help_embed(select.values[0], interaction.user)
        for sel in options:
            if sel.label == select.values[0]:
                sel.default = True
            else:
                sel.default=False
        await interaction.response.edit_message(
            embed=emb, view=self
        )
        #for sel in options:
            #sel.default = False


class Help(commands.Cog):
    def __init__(self, client):
        self.client=client

    @commands.command()
    async def help(self, ctx):
        emb = discord.Embed(
            description=f"**-꒰ Basic Info ꒱-**\n> ❀ ID: `{self.client.user.id}`\n> ❀ Commands: `50+`\n> ❀ Tags: `Fun`, `Games`, `Moderation`, `Utility`, `Memes`\n> ❀ Developer: `asheeshh#7727`\n\n**-꒰ Config ꒱-**\n> ❀ Prefixes: `kana `, `kanna `, `k.`\n\n**-꒰ Command Categories ꒱-**\n> ❀ Moderation: `Moderation related commands.`\n> ❀ Utility  : `Utility related commands.`\n> ❀ Games: `List of Games available.`\n> ❀ Fun: `Fun commands to pass time.`\n> ❀ Memes: `Meme related commands.`", 
            color=ec
        )
        emb.set_author(
            name="⊱┊Help Menu for Kanna",
            icon_url=ctx.author.display_avatar
        )
        emb.set_footer(
            text=f"❀ Requested by {ctx.author.display_name}\n❀ Made by Kanna Chan",
            icon_url=self.client.user.display_avatar
        )
        emb.set_image(url="https://i.imgur.com/HPHuVr2.png")
        view=HelpView(ctx)
        btn1 = Button(label="Contact Developer", style=discord.ButtonStyle.url, url="discord://discordapp.com/users/926870214254153739")
        btn3 = Button(label="Support Server", style=discord.ButtonStyle.url, url="discord://discord.gg/7CYP8pKzDB")
        btn2 = Button(label="Invite", style=discord.ButtonStyle.url, url="discord://discordapp.com/api/oauth2/authorize?client_id=922887317218279444&permissions=8&scope=bot%20applications.commands")
        view.add_item(btn1)
        view.add_item(btn3)
        view.add_item(btn2)
        msg = await ctx.send(embed=emb, view=view)
        async def timeout():
            for dd in view.children:
                if not isinstance(dd, Button):
                    dd.disabled=True
            await msg.edit(view=view)
        view.on_timeout = timeout

def setup(client):
    client.add_cog(Help(client))
    print(">> Help Loaded.")