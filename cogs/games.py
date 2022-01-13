from datetime import time
import random
from typing import Union
import discord
from discord import emoji
from discord import user
from discord.ext import commands
from discord.ui import View, Button
from discord.commands import slash_command, Option
from ._embed import get_rps_embed
from PIL import Image, ImageDraw
import random
from ._config import gi

el1 = ["😀", "😶", "😄", "😑", "🙄", "🤣", "🥰", "😁"]
el2 = ["😅", "😆", "😉", "😋", "😎", "😘", "😊", "😍", "😗"]
el3 = ["😙", "😚", "🙂", "🤗", "🤨", "😐", "🤔", "😃", "😂"]

def game_logic(choice_user, choice_bot, ctx):
    logic_dict ={
        "r":"s",
        "s":"p",
        "p":"r"
    }
    #print(choice_bot, choice_user)
    if choice_bot == choice_user:
        #print("tie")
        return get_rps_embed("d", ctx, choice_user, choice_bot)
    elif logic_dict[choice_user] == choice_bot:
        #print("win")
        return get_rps_embed("w", ctx, choice_user, choice_bot)
    elif logic_dict[choice_user] != choice_bot and choice_user != choice_bot:
        #print("lose")
        return get_rps_embed("l", ctx, choice_user, choice_bot)

def get_ship(user_list:list):
    love = random.randint(0, 101)
    if love >= 0 and love <= 15:
        quote = "Not in this life.."
    elif love > 15 and love <= 25:
        quote = "Looks impossible..but who knows?"
    elif love > 25 and love <= 50:
        quote = "Maybe.."
    elif love > 50 and love <= 70:
        quote = "Quite Possible.."
    elif love > 70 and love <= 90:
        quote = "Should already be in this relationship!!"
    elif love > 90 and love <= 101:
        quote = "Fated partners uwu"
    ship = f"> {user_list[0].mention} + {user_list[1].mention} = **{love}%** of LOVE <:kannawee:877036162122924072>\n> *{quote}*"
    return ship

class GTEView(View):
    def __init__(self, ctx, user_list: list, user:discord.User, partner:discord.User):
        super().__init__(timeout=20)
        self.user_list = user_list
        self.user = user
        self.partner = partner
        self.ctx = ctx
        self.choice1 = None
        self.choice2 = None
        self.turn = 0
        def shuffle():
            ref ={
                "1":el1,
                "2":el2,
                "3":el3
            }
            for button in self.children:
                button.emoji = random.choice(ref[button.custom_id])
        shuffle()

    @discord.ui.button(emoji=None, style=2, custom_id="1")
    async def b1_callback(self, button, interaction):
        if self.turn == 0:
            self.choice1 = button.emoji
            self.user_list.pop(0)
            self.user_list.append(self.partner)
            await interaction.response.edit_message(content=f"Time to guess the emoji! {self.user_list[0].mention}", view=self)
            self.turn += 1
        elif self.turn == 1:
            self.choice2 = button.emoji
            if self.choice1 is self.choice2:
                for btn in self.children:
                    btn.disabled = True
                await interaction.response.edit_message(content=f"Congratulations! {self.user_list[0].mention}, You guessed the emoji correctly, it was {button.emoji}!", view=self)
                self.choice1=None
                self.choice2=None
            else:
                for btn in self.children:
                    btn.disabled = True
                await interaction.response.edit_message(content=f"Oh shet! {self.user_list[0].mention}, You couldn't guess the emoji correctly, it was {button.emoji}!", view=self)
                self.choice1=None
                self.choice2=None

    @discord.ui.button(emoji=None, style=2, custom_id="2")
    async def b2_callback(self, button, interaction):
        if self.turn == 0:
            self.choice1 = button.emoji
            self.user_list.pop(0)
            self.user_list.append(self.partner)
            await interaction.response.edit_message(content=f"Time to guess the emoji! {self.user_list[0].mention}", view=self)
            self.turn += 1
        elif self.turn == 1:
            self.choice2 = button.emoji
            if self.choice1 is self.choice2:
                for btn in self.children:
                    btn.disabled = True
                await interaction.response.edit_message(content=f"Congratulations! {self.user_list[0].mention}, You guessed the emoji correctly, it was {button.emoji}!", view=self)
                self.choice1=None
                self.choice2=None
            else:
                for btn in self.children:
                    btn.disabled = True
                await interaction.response.edit_message(content=f"Oh shet! {self.user_list[0].mention}, You couldn't guess the emoji correctly, it was {button.emoji}!", view=self)
                self.choice1=None
                self.choice2=None

    @discord.ui.button(emoji=None, style=2, custom_id="3")
    async def b3_callback(self, button, interaction):
        if self.turn == 0:
            self.choice1 = button.emoji
            self.user_list.pop(0)
            self.user_list.append(self.partner)
            await interaction.response.edit_message(content=f"Time to guess the emoji! {self.user_list[0].mention}", view=self)
            self.turn += 1
        elif self.turn == 1:
            self.choice2 = button.emoji
            if self.choice1 is self.choice2:
                for btn in self.children:
                    btn.disabled = True
                await interaction.response.edit_message(content=f"Congratulations! {self.user_list[0].mention}, You guessed the emoji correctly, it was {button.emoji}!", view=self)
                self.choice1=None
                self.choice2=None
            else:
                for btn in self.children:
                    btn.disabled = True
                await interaction.response.edit_message(content=f"Oh shet! {self.user_list[0].mention}, You couldn't guess the emoji correctly, it was {button.emoji}!", view=self)
                self.choice1=None
                self.choice2=None

    async def interaction_check(self, interaction):
        if interaction.user in self.user_list:
            return True
        else:
            if interaction.user == self.user:
                await interaction.response.send_message("This is not your turn!", ephemeral = True)
            else:
                await interaction.response.send_message("This game is not for you!", ephemeral=True)
            return False
    
    async def on_timeout(self):
        self.choice1 = None
        self.choice2 = None
        for btn in self.children:
            btn.disabled=True
        await self.ctx.edit(view=self)

class ShipView(View):
    def __init__(self, user_list, ctx):
        super().__init__(timeout=40)
        self.user_list = user_list
        self.ctx = ctx

    @discord.ui.button(label="Ship Again", style=2, emoji=discord.PartialEmoji(name="explosion_heart", animated = True, id = 877426228775227392))
    async def callback(self, button, interaction):
        desc = get_ship(self.user_list)
        await interaction.response.edit_message(content=desc)
    
    async def interaction_check(self, interaction):
        if interaction.user in self.user_list:
            return True
        else:
            await interaction.response.send_message("This UI is not for you!", ephemeral=True)
            return False
    
    async def on_timeout(self):
        for button in self.children:
            button.disabled = True
        await self.ctx.edit(view=self)


class RPSView(View):
    def __init__(self, ctx, cb):
        self.ctx=ctx
        self.cb = cb
        super().__init__(timeout=20)
    
    @discord.ui.button(label="Rock", style=2, emoji="✊")
    async def rock_callback(self, button, interaction):
        emb = game_logic("r", self.cb, self.ctx)
        button.style = discord.ButtonStyle.green
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(embed=emb, view=self)

    @discord.ui.button(label="Paper", style=2, emoji="✋")
    async def paper_callback(self, button, interaction):
        emb = game_logic("p", self.cb, self.ctx)
        button.style = discord.ButtonStyle.green
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(embed=emb, view=self)

    @discord.ui.button(label="Scissors", style=2, emoji="✌")
    async def sc_callback(self, button, interaction):
        emb = game_logic("s", self.cb, self.ctx)
        button.style = discord.ButtonStyle.green
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(embed=emb, view=self)
    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This game is not for you!", ephemeral=True)
            return False
        else:
            return True
    async def on_timeout(self):
        for button in self.children:
            button.disabled = True
        await self.ctx.edit(view=self) 

class FView(View):
    def __init__(self, ctx, query):
        super().__init__(timeout=10)
        self.user_list=[]
        self.ctx = ctx
        self.query = query
    
    @discord.ui.button(label="Pay Respect", style=2, emoji=discord.PartialEmoji(name="pressf", id=926119493896392785))
    async def callback(self, button, interaction):
        self.user_list.append(interaction.user.id)
        await interaction.response.send_message(f"**{interaction.user.name} has paid their respect!**")

    async def interaction_check(self, interaction):
        if interaction.user.id not in self.user_list:
            return True
        else:
            await interaction.response.send_message("You have already paid your respect!", ephemeral=True)

    async def on_timeout(self):
        for button in self.children:
            button.disabled = True
        await self.ctx.edit(view=self)
        await self.ctx.send(f"**{len(self.user_list)}** {'users' if len(self.user_list) > 1 else 'user'} paid their RESPECT to **{self.query}**.")


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(
        name="rps",
        description="Classic RPS game using Buttons."
    )
    async def rps(self, ctx):
        choice_bot = random.choice(["r", "s", "p"])
        emb = get_rps_embed("g", ctx)
        view = RPSView(ctx, choice_bot)
        await ctx.respond(embed=emb, view=view)

    @slash_command(
        name="ship",
        description="Ship yourself with other users and get cancelled UwU"
    )
    async def ship(self, ctx, user1:discord.User=None, user2:discord.User=None):
        if user1 is None and user2 is None:
            user1, user2 = ctx.author
        elif user1 is None and user2 is not None:
            user1 = ctx.author
        elif user1 is not None and user2 is None:
            user2 = ctx.author
        a1 = user1.display_avatar.with_size(512)
        a2 = user2.display_avatar.with_size(512)
        await a1.save(f"images/generated/{user1.id}.png")
        await a2.save(f"images/generated/{user2.id}.png")
        pfp1=Image.open(f"images/generated/{user1.id}.png").resize((400, 400))
        pfp2=Image.open(f"images/generated/{user2.id}.png").resize((400, 400))
        mask=Image.open(f"images/generated/mask.jpg")
        bg=Image.new('RGBA', (1200, 500), (255, 0, 0, 0))
        bg.paste(pfp1, (37, 28), mask)
        bg.paste(pfp2, (752, 27), mask)
        bg.save(f'images/generated/back{user1.id}.png')
        overlay = Image.open('./images/assets/overlay.png')
        base = Image.open(f'images/generated/back{user1.id}.png').convert('RGBA')
        final=Image.alpha_composite(base, overlay)
        final.save(f'images/generated/final{user1.id}.png')
        des = get_ship([user1, user2])
        file = discord.File(f'images/generated/final{user1.id}.png')
        view = ShipView([user1, user2], ctx)
        await ctx.respond(des, file=file, view=view)


    @slash_command(
        name="f",
        description="Pay respect to a User or Anything!"
    )
    async def f(
        self, ctx,
        user: Option(discord.User, "Pay respect to a User.", required=False),
        other: Option(str, "Pay respect to any other thing.", required=False)
    ):
        if user is not None and other is not None:
            await ctx.respond("Please chosse any one out of `User` or `Other`!", ephemeral=True)
        elif user is not None and other is None:
            q = user
        elif user is None and other is not None:
            q = other
        view = FView(ctx, q)
        await ctx.respond(f"> It's time to Pay Respect to **{q}**\nPress **F** to pay your respects!", view=view)
        
    @slash_command(
        name="gte",
        description="Play a game of Guess the Emote with a friend."
    )
    async def gte(self, ctx, user:discord.User):
        if user == ctx.author:
            await ctx.respond("You can't play with yourself baka!")
        elif user != ctx.author:
            view = GTEView(ctx, [ctx.author], ctx.author, user)
            await ctx.respond(f"{user.mention}, you have been challenged by {ctx.author.mention} for a game of `Guess The Emote`\n**{ctx.author.display_name}** goes first, choose any emoji!", view=view)

class NGames(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rps(self, ctx):
        emb = get_rps_embed("g", ctx)
        choice_bot = random.choice(["r", "s", "p"])
        view = RPSView(ctx, choice_bot)
        msg = await ctx.send(embed=emb, view=view)
        async def timeout():
            for btn in view.children:
                btn.disabled=True
            await msg.edit(view=view)
        view.on_timeout = timeout

    @commands.command()
    async def ship(self, ctx, user1:discord.User=None, user2:discord.User=None):
        if user1 is None and user2 is None:
            user1, user2 = ctx.author
        elif user1 is None and user2 is not None:
            user1 = ctx.author
        elif user1 is not None and user2 is None:
            user2 = ctx.author
        a1 = user1.display_avatar.with_size(512)
        a2 = user2.display_avatar.with_size(512)
        await a1.save(f"images/generated/{user1.id}.png")
        await a2.save(f"images/generated/{user2.id}.png")
        pfp1=Image.open(f"images/generated/{user1.id}.png").resize((400, 400))
        pfp2=Image.open(f"images/generated/{user2.id}.png").resize((400, 400))
        mask=Image.open(f"images/generated/mask.jpg")
        bg=Image.new('RGBA', (1200, 500), (255, 0, 0, 0))
        bg.paste(pfp1, (37, 28), mask)
        bg.paste(pfp2, (752, 27), mask)
        bg.save(f'images/generated/back{user1.id}.png')
        overlay = Image.open('./images/assets/overlay.png')
        base = Image.open(f'images/generated/back{user1.id}.png').convert('RGBA')
        final=Image.alpha_composite(base, overlay)
        final.save(f'images/generated/final{user1.id}.png')
        des = get_ship([user1, user2])
        file = discord.File(f'images/generated/final{user1.id}.png')
        view = ShipView([user1, user2], ctx)
        msg = await ctx.send(des, file=file, view=view)
        async def timeout():
            for btn in view.children:
                btn.disabled=True
            await msg.edit(view=view)
        view.on_timeout = timeout


    @commands.command()
    async def f(
        self, ctx,
        u: Union[discord.User, str]=None
    ):
        if u is None:
            u = ctx.author
        view = FView(ctx, str(u))
        msg = await ctx.send(f"> It's time to Pay Respect to `{str(u)}`\nPress **F** to pay your respects!", view=view)
        async def timeout():
            for btn in view.children:
                btn.disabled=True
            await msg.edit(view=view)
        view.on_timeout = timeout
        
    @commands.command()
    async def gte(self, ctx, user:discord.User):
        if user == ctx.author:
            await ctx.reply("You can't play with yourself baka!")
        elif user != ctx.author:
            view = GTEView(ctx, [ctx.author], ctx.author, user)
            msg = await ctx.send(f"{user.mention}, you have been challenged by {ctx.author.mention} for a game of `Guess The Emote`\n**{ctx.author.display_name}** goes first, choose any emoji!", view=view)
            async def timeout():
                for btn in view.children:
                    btn.disabled=True
                await msg.edit(view=view)
            view.on_timeout = timeout

    
        
def setup(client):
    client.add_cog(Games(client))
    client.add_cog(NGames(client))
    print(">> Games Loaded.")
