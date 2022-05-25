from ._bmdb import get_bookmark, check_bookmark, get_bookmarks, set_bookmark, remove_bookmark
from ._config import ec
import discord
from discord.ext import commands
from discord.commands import message_command
import datetime, calendar

def get_unix(date: datetime.datetime):
    u = calendar.timegm(date.utctimetuple())
    return f"<t:{u}:R>"

class BookMark(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name="bookmark", aliases=["bm"], invoke_without_command=True)
    async def bookmark(ctx):
        pass

    @bookmark.command(usage="prefix bm add <message_id> <bookmark_name>", aliases=["a"])
    async def add(ctx, message: discord.Message, *, name: str):
        if message is None or name is None:
            await ctx.reply("Invalid Arguments, Example `kana bm add <message_id> <bookmark_name>`")
        else:
            if not check_bookmark(ctx.author.id, name):
                media = message.attachments
                emb = discord.Embed(color=ec)
                emb.add_field(name="Message", value=message.content, inline=False)
                emb.add_field(name="Author", value=message.author.name+"#"+message.author.discriminator, inline=True)
                emb.add_field(name="Channel", value=message.channel.name, inline=True)
                emb.add_field(name="Server", value=message.guild.name, inline=True)
                emb.add_field(name="Bookmark ID", value=message.id, inline=True)
                emb.add_field(name="Message Created", value=get_unix(message.created_at), inline=True)
                emb.add_field(name="Jump to Message", value=f"[Click Here]({message.jump_url})", inline=True)
                if len(media) > 0:
                    for i in range (0, len(media)):
                        if i == 0:
                            emb.add_field(name="Medias", value=f"[Attachmet {i+1}]({media[i].url})", inline=False)
                        else:
                            emb.set_field_at(index=len(emb.fields)-1, name="Medias", value=emb.fields[-1].value+" | "+f"[Attachmet {i+1}]({media[i].url})", inline=False)
                set_bookmark(ctx.author.id, message.id, name, message.content, message.author.name+"#"+message.author.discriminator, message.channel.name, message.guild.name, get_unix(message.created_at), message.jump_url)
                await ctx.reply(f"Bookmark added with name {name}", embed=emb)
            else:
                await ctx.reply(f"Bookmark with name `{name}` already exists!")
            
    @bookmark.command(aliases=["view"])
    async def show(ctx, *, name: str):
        if check_bookmark(ctx.author.id, name):
            b = dict(get_bookmark(ctx.author.id, name))
            emb = discord.Embed(color=ec)
            emb.add_field(name="Message", value=b["content"], inline=False)
            emb.add_field(name="Author", value=b["author"], inline=True)
            emb.add_field(name="Channel", value=b["channel"], inline=True)
            emb.add_field(name="Server", value=b["server"], inline=True)
            emb.add_field(name="Bookmark ID", value=b["id"], inline=True)
            emb.add_field(name="Message Created", value=b["created"], inline=True)
            emb.add_field(name="Jump to Message", value=f"[Click Here]({b['link']})", inline=True)
            await ctx.reply(embed=emb)
        else:
            await ctx.reply(f"Bookmark with name **{name}** does not exist!")

    @bookmark.command(aliases=["bms"])
    async def all(ctx, *, user: discord.User = None):
        user = ctx.author if user is None else user
        msg = await ctx.send('Getting bookmarks...')
        bms = list(dict(get_bookmarks(user.id)).keys()) if get_bookmarks(user.id) is not None else []
        print(bms)
        if len(bms) > 0:
            desc=f""
            for i in range (0, len(bms)):
                if i == len(bms)-1:
                    desc += f"`{bms[i]}`"
                else:
                    desc += f"`{bms[i]}`, "
            emb = discord.Embed(description=desc, color=ec)
            emb.set_author(
                name=f"{user.name}#{user.discriminator}'s Bookmarks",
                icon_url=user.default_avatar
            )
            await ctx.reply(embed=emb)
            await msg.delete()
        else:
            await ctx.reply(f"`{user.name}#{user.discriminator}` has no bookmarks.")
            await msg.delete()

    @bookmark.command(aliases=["rm", "del"])
    async def remove(ctx, *, name):
        if check_bookmark(ctx.author.id, name):
            remove_bookmark(ctx.author.id, name)
            await ctx.reply(f"Bookmark **{name}** deleted!")
        else:
            await ctx.reply(f"Bookmark **{name}** does not exist!")

class BookMarkApp(commands.Cog):
    def __init__(self, client):
        self.client = client

    @message_command(name="Bookmark Message")
    async def bookmark_message(ctx, message: discord.Message):
        if not check_bookmark(ctx.author.id, msg.content):
            media = message.attachments
            emb = discord.Embed(color=ec)
            emb.add_field(name="Message", value=message.content, inline=False)
            emb.add_field(name="Author", value=message.author.name+"#"+message.author.discriminator, inline=True)
            emb.add_field(name="Channel", value=message.channel.name, inline=True)
            emb.add_field(name="Server", value=message.guild.name, inline=True)
            emb.add_field(name="Bookmark ID", value=message.id, inline=True)
            emb.add_field(name="Message Created", value=get_unix(message.created_at), inline=True)
            emb.add_field(name="Jump to Message", value=f"[Click Here]({message.jump_url})", inline=True)
            if len(media) > 0:
                for i in range (0, len(media)):
                    if i == 0:
                        emb.add_field(name="Medias", value=f"[Attachmet {i+1}]({media[i].url})", inline=False)
                    else:
                        emb.set_field_at(index=len(emb.fields)-1, name="Medias", value=emb.fields[-1].value+" | "+f"[Attachmet {i+1}]({media[i].url})", inline=False)
            await ctx.defer()
            prompt = await ctx.send("Enter a name for this bookmark, should be unique")
            def check(m):
                return m.channel == message.channel and m.author == message.author
            try:
                msg = await client.wait_for('message', check=check, timeout=60)
            except:
                await ctx.send("Timed out")
                return 
            set_bookmark(ctx.author.id, message.id, msg.content, message.content, message.author.name+"#"+message.author.discriminator, message.channel.name, message.guild.name, get_unix(message.created_at), message.jump_url)
            await ctx.respond(f"Bookmark added with name {msg.content}", embed=emb)
            await prompt.delete()
        else:
            await ctx.respond(f"Bookmark with name {msg.content} already exists!")
            await prompt.delete()