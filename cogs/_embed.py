import discord
from ._config import ec
import datetime
import calendar


def get_unix(date: datetime.datetime):
    u = calendar.timegm(date.utctimetuple())
    return f"<t:{u}:R>"

# Marriage Embeds
def get_embed(arg:str, ctx, u=None):
    if arg == "m":
        memb = discord.Embed(
            description=f"· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·\n●˚◞♡  ⃗ ꒰{ctx.author.mention}꒱ has proposed to ꒰{u.mention}꒱\n\n●˚◞♡  ⃗ ꒰{u.mention}꒱ Do you accept this `proposal`?\n· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·\n",
            color=ec
        )
        memb.set_author(
            name="˚₊· ͟͟͞͞➳❥ Marriage Proposal",
            icon_url=ctx.author.display_avatar
        )
        memb.set_thumbnail(url="https://thumbs.gfycat.com/ClassicSecondaryKinkajou-max-1mb.gif")
        memb.set_footer(
            text=f"✿ Made by Kanna Chan\n✿ Use k.help for help\n✿ Requested by {ctx.author.name.capitalize()}",
            icon_url=ctx.author.display_avatar
        )
        return memb
    elif arg == "a":
        emb = discord.Embed(description=f"· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·\n●˚◞♡  ⃗ {ctx.author.mention} and {u.mention} are a **Married Couple** now!\n\n●˚◞♡  ⃗ You can view your **Marriage Card** by using command `kana marriage` now!\n· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·\n", color=ec)
        emb.set_author(
            name="˚₊· ͟͟͞͞➳❥ Prposal Accepted 💖",
            icon_url=ctx.author.display_avatar
        )
        emb.set_thumbnail(url="https://thumbs.gfycat.com/ClassicSecondaryKinkajou-max-1mb.gif")
        emb.set_image(url="https://data.whicdn.com/images/343437654/original.gif?t=1588100320")
        emb.set_footer(
            text=f"✿ Made by Kanna Chan\n✿ Use k.help for help\n✿ Requested by {ctx.author.name.capitalize()}",
            icon_url=ctx.author.display_avatar
        )
        return emb
    elif arg == "d":
        emb = discord.Embed(description=f"· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·\n●˚◞♡  ⃗ {u.mention} has declined the **Marriage Proposal** by {ctx.author.mention}\n\n●˚◞♡  ⃗ The proposal was **Declined**, you have to find someone else :(\n· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·\n", color=ec)
        emb.set_author(
            name="˚₊· ͟͟͞͞➳❥ Proposal Declined 💔",
            icon_url=ctx.author.display_avatar
        )
        emb.set_thumbnail(url="https://thumbs.gfycat.com/ClassicSecondaryKinkajou-max-1mb.gif")
        emb.set_footer(
            text=f"✿ Made by Kanna Chan\n✿ Use k.help for help\n✿ Requested by {ctx.author.name.capitalize()}",
            icon_url=ctx.author.display_avatar
        )
        return emb

def get_rps_embed(arg:str, ctx, choice:str=None, cb:str=None):
    choice_dict = {
        "r":"rock",
        "s":"scissors",
        "p":"paper"
    }
    if arg == "g":
        gemb = discord.Embed(description="> *Rock, Paper, Scissors..*\n> Click on the `Buttons` to play the Game!", color=ec)
        gemb.set_author(
            name=f"{ctx.author.name}'s RPS Game.",
            icon_url=ctx.author.display_avatar
        )
        gemb.set_footer(
            text="You have 20 seconds to choose!",
            icon_url=ctx.author.display_avatar
        )
        return gemb
    elif arg == "w":
        wemb = discord.Embed(description=f"> *GG, you won the Game!*\n> You chose `{choice_dict[choice].capitalize()}` and I chose `{choice_dict[cb].capitalize()}`.", color=ec)
        wemb.set_author(
            name=f"{ctx.author.name}'s RPS Game.",
            icon_url=ctx.author.display_avatar
        )
        wemb.set_footer(
            text="Use /rps to play again!",
            icon_url=ctx.author.display_avatar
        )
        return wemb
    elif arg == "l":
        lemb = discord.Embed(description=f"> *Sad, you lost the game :(*\n> You chose `{choice_dict[choice].capitalize()}` and I chose `{choice_dict[cb].capitalize()}`.", color=ec)
        lemb.set_author(
            name=f"{ctx.author.name}'s RPS Game.",
            icon_url=ctx.author.display_avatar
        )
        lemb.set_footer(
            text="Use /rps to play again!",
            icon_url=ctx.author.display_avatar
        )
        return lemb
    elif arg == "d":
        demb = discord.Embed(description=f"> *OwO, it's a draw!*\n> You chose `{choice_dict[choice].capitalize()}` and I chose `{choice_dict[choice].capitalize()}` too.", color=ec)
        demb.set_author(
            name=f"{ctx.author.name}'s RPS Game.",
            icon_url=ctx.author.display_avatar
        )
        demb.set_footer(
            text="Use /rps to play again!",
            icon_url=ctx.author.display_avatar
        )
        return demb

def get_logger_embed(arg, guild: discord.Guild):
    emb = discord.Embed(description=f"● Guild Name: {guild.name}\n● Member Count: {guild.member_count}\n● Owner: {guild.owner.name}\n● Region: {guild.region}\n● Created At: {get_unix(guild.created_at)}", color=ec)
    emb.timestamp = datetime.datetime.utcnow()
    emb.set_thumbnail(url=guild.icon_url)
    return emb