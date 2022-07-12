import discord
from discord.ext import commands
from discord.ui import View, Button
from ._config import ec
import datetime, calendar
import io
import aiohttp

cont = "<:reply:928274405358993418>"
cont2 = "<:reply_cont:928276632232398869>"


def get_unix(date: datetime.datetime):
    u = calendar.timegm(date.utctimetuple())
    return f"<t:{u}:R>"


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def prefix(self, ctx):
        await ctx.reply("My prefixes are `kana`, `kanna` and `k.`.")

    @commands.command()
    async def invite(self, ctx):
        view = View()
        btn = Button(
            label="Invite Me",
            style=discord.ButtonStyle.url,
            url="https://discord.com/api/oauth2/authorize?client_id=857835279259664403&permissions=1538369383927&scope=bot%20applications.commands",
        )
        view.add_item(btn)
        await ctx.reply("Here is my Invite Link (╯▽╰ )", view=view)

    @commands.command()
    async def support(self, ctx):
        view = View()
        btn = Button(
            label="Invite Me",
            style=discord.ButtonStyle.url,
            url="https://discord.gg/7CYP8pKzDB",
        )
        view.add_item(btn)
        await ctx.reply("Join this server for support (╯▽╰ )", view=view)

    @commands.command()
    async def about(self, ctx):
        view = View()
        btn1 = Button(
            label="Invite Me",
            style=discord.ButtonStyle.url,
            url="https://discord.com/api/oauth2/authorize?client_id=857835279259664403&permissions=1538369383927&scope=bot%20applications.commands",
        )
        btn2 = Button(
            label="Invite Me",
            style=discord.ButtonStyle.url,
            url="https://discord.gg/7CYP8pKzDB",
        )
        view.add_item(btn1)
        view.add_item(btn2)
        ch = 0
        for guild in self.client.guilds:
            for channel in guild.channels:
                ch += 1
        desc = f"**-꒰ About Kanna ꒱-**\n> ❀ Version: `2.0.0a`\n> ❀ ID: `{self.client.user.id}`\n> ❀ Commands: `100+`\n> ❀ Tags: `Fun`, `Games`, `Moderation`, `Utility`, `Memes`\n> ❀ Developer: `asheeshh#7727`\n> ❀ Server Count: `{len(self.client.guilds)}`\n> ❀ User Count: `{len(self.client.users)}`\n> ❀ Channel Count: `{ch}`\n> ❀ Library: `Pycord`"
        emb = discord.Embed(description=desc, color=ec)
        emb.set_author(name="About Me OwO", icon_url=self.client.user.display_avatar)
        emb.set_thumbnail(url=self.client.user.display_avatar)
        emb.set_footer(
            text=f"❀ Requested by {ctx.author.display_name}\n❀ Made by Kanna Chan",
            icon_url=ctx.author.display_avatar,
        )
        await ctx.send(embed=emb)

    @commands.command(aliases=["userinfo", "whois"])
    async def ui(self, ctx, user: discord.Member = None):
        user = ctx.author if user is None else user
        if user.guild_avatar is None:
            print("trueee")
        desc = f"**-꒰ Member Info ꒱-**\n{cont2} ❀ Username: `{user}`\n{cont2} ❀ Nickname: `{user.display_name}`\n{cont2} ❀ ID: `{user.id}`\n{cont2} ❀ Joined Discord: {get_unix(user.created_at)}\n{cont2} ❀ Joined Server: {get_unix(user.joined_at)}\n{cont2} ❀ Is Bot: `{'Yes' if user.bot else 'No'}`\n{cont2} ❀ Top Role: {user.top_role.mention}\n{cont} ❀ Guild Avatar: {f'[`Click Here`]({user.guild_avatar.url})' if user.guild_avatar is not None else '`None`'}"
        emb = discord.Embed(description=desc, color=ec)
        emb.set_author(
            name=f"Showing Info for {user}", icon_url=ctx.author.display_avatar
        )
        try:
            us = await self.client.fetch_user(user.id)
            emb.set_image(url=us.banner)
        except Exception:
            pass
        emb.set_thumbnail(url=user.display_avatar)
        emb.set_footer(
            text=f"❀ Requested by {ctx.author.display_name}\n❀ Made by Kanna Chan",
            icon_url=ctx.author.display_avatar,
        )
        await ctx.send(embed=emb)

    @commands.command(aliases=["rg"])
    async def rgay(self, ctx):
        msg_id = ctx.message.reference.message_id
        msg = self.client.get_message(int(msg_id))
        await msg.add_reaction("🇬")
        await msg.add_reaction("🇦")
        await msg.add_reaction("🇾")

    @commands.command(aliases=["aq"])
    async def aquote(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://animechan.vercel.app/api/random") as r:
                data = await r.json()
                await ctx.send(
                    f"*“{data['quote']}„*\n-- {data['character']} | {data['anime']}"
                )


def setup(client):
    client.add_cog(Misc(client))
    print(">> Misc Loaded")
