import discord
from discord.ext import commands
from discord.commands import slash_command
import aiohttp
from discord.ui import Button, View
import weeby
import uwuify
from ._config import gi
from decouple import config

token = str(config("WTOKEN"))
w = weeby.Weeby(str(config("WTOKEN")))


class SimpView(View):
    def __init__(self, ctx, auth, one_being_simped_on):
        self.ctx = ctx
        self.auth = auth
        self.obso = one_being_simped_on
        super().__init__(timeout=20)

    @discord.ui.button(
        label="Simp Back",
        style="2",
        emoji=discord.PartialEmoji(name="Kannawee", id=877036162122924072),
    )
    async def y_callback(self, button, interaction):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://getpickuplines.herokuapp.com/lines/random") as r:
                resp = await r.json()
                pl = resp["line"]
                await interaction.response.send_message(
                    f"> {interaction.user.mention} simps back on {self.auth.mention} <:cute_stare:882300914101289031>\n> `{pl}`"
                )

    @discord.ui.button(
        label="Ignore",
        style="2",
        emoji=discord.PartialEmoji(name="kanna_no", id=877038775686021130),
    )
    async def n_callback(self, button, interaction):
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self)

    async def interaction_check(self, interaction):
        if interaction.user == self.obso:
            return True
        else:
            await interaction.response.send_message(
                "This Pickup Line is not for you!", ephemeral=True
            )
            return False

    async def on_timeout(self):
        for button in self.children:
            button.disabled = True
        await self.ctx.edit(view=self)


class Response(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(
        name="simp", description="Simp on any user by sending a Pick Up Line 😳"
    )
    async def simp(self, ctx, user: discord.User):
        await ctx.defer()
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://getpickuplines.herokuapp.com/lines/random") as r:
                resp = await r.json()
                pl = resp["line"]
                view = SimpView(ctx, ctx.author, user)
                await ctx.respond(
                    f"> {ctx.author.mention} simps on {user.mention} <:cute_stare:882300914101289031>\n> `{pl}`",
                    view=view,
                )

    @slash_command(name="dadjoke", description="Get a random DadJoke!")
    async def dadjoke(self, ctx):
        headers = {"Authorization": f"Bearer {token}"}
        await ctx.defer()
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                "https://weebyapi.xyz/json/dadjoke", headers=headers
            ) as r:
                resp = await r.json()
                await ctx.respond(f"*{resp['response']}*")

    @slash_command(name="roast", description="Roast any user!")
    async def roast(self, ctx, user: discord.User = None):
        user = ctx.author if user is None else user
        headers = {"Authorization": f"Bearer {token}"}
        await ctx.defer()
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://weebyapi.xyz/json/roast", headers=headers) as r:
                resp = await r.json()
                await ctx.followup.send(
                    f"> *{ctx.author.mention} roasts {user.mention} (´。＿。｀)*\n> *`{resp['response']}`*"
                )

    @slash_command(name="uwuify", description="Turn your text to uwu one :3")
    async def uwuify(self, ctx, text: str):
        await ctx.respond(uwuify.uwu(text))


class NResponse(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def simp(self, ctx, user: discord.User):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://getpickuplines.herokuapp.com/lines/random") as r:
                resp = await r.json()
                pl = resp["line"]
                view = SimpView(ctx, ctx.author, user)
                msg = await ctx.send(
                    f"> {ctx.author.mention} simps on {user.mention} <:cute_stare:882300914101289031>\n> `{pl}`",
                    view=view,
                )

                async def timeout():
                    for btn in view.children:
                        btn.disabled = True
                    await msg.edit(view=view)

                view.on_timeout = timeout

    @commands.command()
    async def roast(self, ctx, user: discord.User = None):
        user = ctx.author if user is None else user
        headers = {"Authorization": f"Bearer {token}"}
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://weebyapi.xyz/json/roast", headers=headers) as r:
                resp = await r.json()
                await ctx.send(
                    f"> *{ctx.author.mention} roasts {user.mention} (´。＿。｀)*\n> *`{resp['response']}`*"
                )

    @commands.command()
    async def dadjoke(self, ctx):
        headers = {"Authorization": f"Bearer {token}"}
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                "https://weebyapi.xyz/json/dadjoke", headers=headers
            ) as r:
                resp = await r.json()
                await ctx.reply(f"*{resp['response']}*")

    @commands.command()
    async def uwuify(self, ctx, *, text: str):
        await ctx.reply(uwuify.uwu(text))


def setup(client):
    client.add_cog(Response(client))
    client.add_cog(NResponse(client))
    print(">> Response Loaded")
