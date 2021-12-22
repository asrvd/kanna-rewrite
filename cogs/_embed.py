import discord

# Marriage Embeds
def get_embed(arg:str, ctx, u=None):
    if arg == "m":
        memb = discord.Embed(
            description=f"· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·\n●˚◞♡  ⃗ ꒰{ctx.author.mention}꒱ has proposed to ꒰{u.mention}꒱\n\n●˚◞♡  ⃗ ꒰{u.mention}꒱ Do you accept this `proposal`?\n· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·\n",
            color=0xFF5959
        )
        memb.set_author(
            name="˚₊· ͟͟͞͞➳❥ Marriage Proposal",
            icon_url=ctx.author.display_avatar
        )
        memb.set_thumbnail(url="https://thumbs.gfycat.com/ClassicSecondaryKinkajou-max-1mb.gif")
        memb.set_footer(
            text=f"● Made by Kanna Chan\n● Use /help for help\n● Requested by {ctx.author.name.capitalize()}",
            icon_url=ctx.author.display_avatar
        )
        return memb
    elif arg == "a":
        emb = discord.Embed(description=f"· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·\n●˚◞♡  ⃗ {ctx.author.mention} and {ctx.author.mention} are a **Married Couple** now!\n\n●˚◞♡  ⃗ You can view your **Marriage Certificate** by clicking below now!\n· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·\n", color=0xFF5959)
        emb.set_author(
            name="˚₊· ͟͟͞͞➳❥ Prposal Accepted 💖",
            icon_url=ctx.author.display_avatar
        )
        emb.set_thumbnail(url="https://thumbs.gfycat.com/ClassicSecondaryKinkajou-max-1mb.gif")
        emb.set_image(url="https://data.whicdn.com/images/343437654/original.gif?t=1588100320")
        emb.set_footer(
            text=f"● Made by Kanna Chan\n● Use /help for help\n● Requested by {ctx.author.name.capitalize()}",
            icon_url=ctx.author.display_avatar
        )
        return emb
    elif arg == "d":
        emb = discord.Embed(description=f"· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·\n●˚◞♡  ⃗ {ctx.author.mention} has declined the **Marriage Proposal** by {ctx.author.mention}\n\n●˚◞♡  ⃗ The proposal was **Declined**, you have to find someone else :(\n· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·\n", color=0xFF5959)
        emb.set_author(
            name="˚₊· ͟͟͞͞➳❥ Proposal Declined 💔",
            icon_url=ctx.author.display_avatar
        )
        emb.set_thumbnail(url="https://thumbs.gfycat.com/ClassicSecondaryKinkajou-max-1mb.gif")
        emb.set_footer(
            text=f"● Made by Kanna Chan\n● Use /help for help\n● Requested by {ctx.author.name.capitalize()}",
            icon_url=ctx.author.display_avatar
        )
        return emb