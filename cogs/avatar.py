import discord
from discord.ext import commands
from discord.ui import View, Button
from discord.commands import slash_command
import os
from PIL import Image
from io import BytesIO
from ._config import gi, ec
import requests
import random


class Avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(
        name="av",
        description="Get a user's Default Avatar or Shared Avatar of 2 users."
    )
    async def av(self, ctx, user1:discord.User=None, user2:discord.User=None):
        if user1 is None and user2 is None:
            u = ctx.author
            asset = u.display_avatar
            emb=discord.Embed(color=ec)
            emb.set_author(
                name=f"{u.display_name}'s Avatar",
                icon_url=u.display_avatar
            )
            emb.set_image(url=ctx.author.display_avatar)
            emb.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=self.client.user.display_avatar
            )
            await ctx.respond(embed=emb)
        elif user1 is not None and user2 is None:
            u = user1
            emb=discord.Embed(color=ec)
            emb.set_author(
                name=f"{u.display_name}'s Avatar",
                icon_url=u.display_avatar
            )
            emb.set_image(url=ctx.author.display_avatar)
            emb.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=self.client.user.display_avatar
            )
            await ctx.respond(embed=emb)
        elif user1 is None and user2 is not None:
            u = user2
            emb=discord.Embed(color=ec)
            emb.set_author(
                name=f"{u.display_name}'s Avatar",
                icon_url=u.display_avatar
            )
            emb.set_image(url=ctx.author.display_avatar)
            emb.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=self.client.user.display_avatar
            )
            await ctx.respond(embed=emb)
        elif user1 is not None and user2 is not None:
            bg = Image.new(mode="RGBA", size=(1000, 500))
            a1 = user1.display_avatar.replace(size=512)
            a2 = user2.display_avatar.replace(size=512)
            await a1.save(f"./images/generated/{user1.id}.png")
            await a2.save(f"./images/generated/{user2.id}.png")
            pfp1=Image.open(f"./images/generated/{user1.id}.png").resize((500, 500))
            pfp2=Image.open(f"./images/generated/{user2.id}.png").resize((500, 500))
            bg.paste(pfp1, (0, 0))
            bg.paste(pfp2, (500, 0))
            bg.save(f"./images/generated/shared{user1.id}.png")
            file = discord.File(f"./images/generated/shared{user1.id}.png", filename="shared.png")
            await ctx.respond(file=file)
            os.system(f"rm -rf images/generated/shared{user1.id}.png")
            os.system(f"rm -rf images/generated/{user1.id}.png")
            os.system(f"rm -rf images/generated/{user2.id}.png")

class AV(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['pfp', "avatar"])
    async def av(self, ctx, *user:discord.User):
        if len(user) == 0:
            emb=discord.Embed(color=ec)
            emb.set_author(
                name=f"{ctx.author.display_name}'s Avatar",
                icon_url=ctx.author.display_avatar
            )
            emb.set_image(url=ctx.author.display_avatar)
            emb.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=self.client.user.display_avatar
            )
            await ctx.send(embed=emb)
        elif len(user) == 1:
            emb=discord.Embed(color=ec)
            emb.set_author(
                name=f"{user[0].display_name}'s Avatar",
                icon_url=user[0].display_avatar
            )
            emb.set_image(url=user[0].display_avatar)
            emb.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=self.client.user.display_avatar
            )
            await ctx.send(embed=emb)
        elif len(user) >= 2:
            animated = []
            for m in user:
                animated.append(m.display_avatar.is_animated())

            imgs = []
            for mem in user:
                url = requests.get(mem.display_avatar.url)
                im = Image.open(BytesIO(url.content))
                imgs.append(im)

            s = len(imgs)
            # print(animated)
            all_animated = all(animated)
            all_not_animated = not any(animated)
            # print(all_animated, all_not_animated)
            if all_animated:  # ANIMATED ############
                frames = []

                s = len(imgs)
                print("S", s)
                d = 250
                bg = Image.new(mode="RGBA", size=(d * s, d))

                for gif in imgs:
                    f = []
                    while True:
                        try:
                            gif.seek(gif.tell() + 1)
                            f.append(gif.copy().resize((d, d)))
                        except Exception as e:
                            frames.append(f)
                            break

                frames_imgs = []
                s = len(frames)
                f_no = 0
                while True:
                    i = 0
                    brk = False
                    bg = Image.new(mode="RGBA", size=(d * s, d))
                    for x in range(0, s):
                        try:
                            bg.paste(frames[i][f_no], (d * x, 0))
                            i += 1
                            frames_imgs.append(bg)
                        except Exception as e:
                            print(e, i)
                            brk = True
                    f_no += 1
                    if brk:
                        break
                # print(frames_imgs)
                if frames_imgs == []:
                    frames_imgs = imgs

                # print(frames_imgs)
                frames_imgs[0].save(
                    f"./images/generated/{ctx.author.id}.gif",
                    save_all=True,
                    append_images=frames_imgs[:],
                    loop=0,
                    quality=1,
                )
                file = discord.File(
                    f"./images/generated/{ctx.author.id}.gif", filename="pic.gif"
                )
                emb = discord.Embed(title="", description=f"", color=ec)
                emb.set_image(url="attachment://pic.gif")
                emb.set_author(
                    name="Multiple Avatars",
                    icon_url=ctx.author.display_avatar
                )
                emb.set_footer(
                    text=f"❀ Requested by {ctx.author.display_name}\n❀ Made by Kanna Chan",
                    icon_url=self.client.user.display_avatar
                )
                await ctx.send(embed=emb, file=file)
                os.system(f"rm -rf images/generated/{ctx.author.id}.gif")
            else:
                s = len(imgs)
                bg = Image.new(mode="RGBA", size=(500 * s, 500))
                i = 0
                for x in range(0, s):
                    try:
                        bg.paste(imgs[i].resize((500, 500)), (500 * x, 0))
                        i += 1
                    except Exception as e:
                        print(e, i)
                        pass
                bg.save(f"./images/generated/{ctx.author.id}.png", quality=10)
                file = discord.File(
                    f"./images/generated/{ctx.author.id}.png", filename="pic.jpg"
                )
                emb = discord.Embed(title="", description=f"", color=ec)
                emb.set_author(
                    name="Multiple Avatars",
                    icon_url=ctx.author.display_avatar
                )
                emb.set_footer(
                    text=f"❀ Requested by {ctx.author.display_name}\n❀ Made by Kanna Chan",
                    icon_url=self.client.user.display_avatar
                )
                emb.set_image(url="attachment://pic.jpg")
                await ctx.send(embed=emb, file=file)
                os.system(f"rm -rf images/generated/{ctx.author.id}.png")

    @commands.command(aliases=['avguild', 'avg', 'pfpg'])
    async def pfpguild(self, ctx, mem: discord.Member=None):
        if mem.guild_avatar is not None:
            emb=discord.Embed(color=ec)
            emb.set_author(
                name=f"{mem.display_name}'s Guild Avatar",
                icon_url=ctx.author.display_avatar
            )
            emb.set_image(url=mem.guild_avatar)
            emb.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=self.client.user.display_avatar
            )
            await ctx.send(embed=emb)
        else:
            await ctx.reply("The user doesn't have a `Guild Avatar`!")

    @commands.command(aliases=['avc', 'pfpc'])
    async def pfpcol(self, ctx, *, size):
        ref = {
            "5x5":500,
            "6x6":600,
            "7x7":700,
            "8x8":800,
            "9x9":900,
            "10x10":1000
        }
        pfp_list = []
        msg = await ctx.send("Making the collage..(can take upto 1 minute)")
        for i in range(0, int(size[0])*int(size[0])):
            mem = random.choice(ctx.guild.members)
            url = requests.get(mem.display_avatar.url)
            im = Image.open(BytesIO(url.content)).resize((100, 100))
            pfp_list.append(im)
        bg = Image.new(mode="RGBA", size=(ref[size], ref[size]))
        for j in range(0, ref[size], 100):
            for k in range(0, ref[size], 100):
                img = pfp_list.pop(0)
                bg.paste(img, (k, j))
        bg.save(f"./images/generated/pfpcollage{ctx.author.id}.png")
        file = discord.File(f"./images/generated/pfpcollage{ctx.author.id}.png", "pfpcollage.png")
        emb = discord.Embed(title="", description=f"", color=ec)
        emb.set_author(
            name=f"Avatar Collage {size}",
            icon_url=ctx.author.display_avatar
        )
        emb.set_footer(
            text=f"❀ Requested by {ctx.author.display_name}\n❀ Made by Kanna Chan",
            icon_url=self.client.user.display_avatar
        )
        emb.set_image(url=f"attachment://pfpcollage.png")
        await ctx.send(embed=emb, file=file)
        await msg.delete()
        os.system(f"rm -rf images/generated/pfpcollage{ctx.author.id}.png")

def setup(client):
    client.add_cog(Avatar(client))
    client.add_cog(AV(client))
    print("Avatar Loaded.")
    
    