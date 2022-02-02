import discord
from discord.commands import slash_command
from discord.ext.commands.errors import CommandInvokeError
from discord.ui import Button, View
from discord.ext import commands, tasks
from ._embed import get_embed
from ._config import gi, ec
import pyrebase
import datetime
import random
import json
from pytz import timezone
from decouple import config

cont = "<:reply:928274405358993418>"
cont2 = "<:reply_cont:928276632232398869>"

firebaseconfig=json.loads(config("FIREBASE_CONFIG"))

firebase = pyrebase.initialize_app(firebaseconfig)
db = firebase.database()

def create(mem1, mem2):    #stores marriage info in database
    now = str(datetime.date.today())
    db.child("MARRIAGE").child(mem1).set({"PARTNER": mem2, "TIME": now, "DATES": 0, "HEARTS": 0, "DATE_TODAY": False})

def mcheck(user1, user2 = None):   
    auth1 = db.child("MARRIAGE").child(user1).get().val()
    auth2 = db.child("MARRIAGE").child(user2).get().val()
    all_users = db.child("MARRIAGE").get()
    if all_users.each() != None:
        for user in all_users.each():
            partner = db.child("MARRIAGE").child(user.key()).child("PARTNER").get().val()
            if partner == user1 or partner == user2:
                return True
                break
    if auth1 != None or auth2 != None:
        return True
    else:
        return False

def add_date_hearts(user1, user2, heart: int):
    auth = db.child("MARRIAGE").child(user1).get().val()
    if auth is None:
        pri = user2
    else:
        pri = user1
    d = int(db.child("MARRIAGE").child(pri).child("DATES").get().val())
    h = int(db.child("MARRIAGE").child(pri).child("HEARTS").get().val())
    db.child("MARRIAGE").child(pri).update({"DATES":d+1, "HEARTS":h+heart, "DATE_TODAY": "True"})

def get_date_heart(user):
    auth = db.child("MARRIAGE").child(user).get().val()
    if auth == None:
        all_users = db.child("MARRIAGE").get()
        if all_users.each() != None:
            for users in all_users.each():
                partner = db.child("MARRIAGE").child(users.key()).child("PARTNER").get().val()
                if partner == user:
                    user = users.key()
            d = db.child("MARRIAGE").child(user).child("DATES").get().val()
            h = db.child("MARRIAGE").child(user).child("HEARTS").get().val()
    else:
        d = db.child("MARRIAGE").child(user).child("DATES").get().val()
        h = db.child("MARRIAGE").child(user).child("HEARTS").get().val()
    return d, h

def check_date(user):
    auth = db.child("MARRIAGE").child(user).get().val()
    if auth == None:
        all_users = db.child("MARRIAGE").get()
        if all_users.each() != None:
            for users in all_users.each():
                partner = db.child("MARRIAGE").child(users.key()).child("PARTNER").get().val()
                if partner == user:
                    user = users.key()
            d = db.child("MARRIAGE").child(user).child("DATE_TODAY").get().val()
    else:
        d = db.child("MARRIAGE").child(user).child("DATE_TODAY").get().val()
    return True if d == "True" else False
    

def scheck(user):   #checks if user is married or not
    auth1 = db.child("MARRIAGE").child(user).get().val()
    all_users = db.child("MARRIAGE").get()
    if all_users.each() != None:
        for users in all_users.each():
            partner = db.child("MARRIAGE").child(users.key()).child("PARTNER").get().val()
            if partner == user:
                return True
                break
    if auth1 != None:
        return True
    else:
        return False

def return_partner(user):  #returns ID of partner
    auth = db.child("MARRIAGE").child(user).get().val()
    if auth == None:
        all_users = db.child("MARRIAGE").get()
        if all_users.each() != None:
            for users in all_users.each():
                partner = db.child("MARRIAGE").child(users.key()).child("PARTNER").get().val()
                if partner == user:
                    p = users.key()
                    break
    else:
        p = db.child("MARRIAGE").child(user).child("PARTNER").get().val()
    return p

def check_partner(user1, user2):   #checks if person is his/her partner
    auth1 = db.child("MARRIAGE").child(user1).child("PARTNER").get().val()
    auth2 = db.child("MARRIAGE").child(user2).child("PARTNER").get().val()
    if user1 == auth2 or user2 == auth1:
        return True
    else:
        return False

def return_time(user):   #returns date of marriage
    auth = db.child("MARRIAGE").child(user).get().val()
    if auth == None:
        all_users = db.child("MARRIAGE").get()
        if all_users.each() != None:
            for users in all_users.each():
                partner = db.child("MARRIAGE").child(users.key()).child("PARTNER").get().val()
                if partner == user:
                    user = users.key()
            time = db.child("MARRIAGE").child(user).child("TIME").get().val()
    else:
        time = db.child("MARRIAGE").child(user).child("TIME").get().val()
    return time

def remove(user1, user2):  #removes user info after divorce
    list = [user1, user2]
    for user in list:
        auth = db.child("MARRIAGE").child(user).get().val()
        if auth != None:
            db.child("MARRIAGE").child(user).remove()

class MarryView(View):
    def __init__(self, ctx, joke):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.joke = joke
    @discord.ui.button(
        label="ㅤYesㅤ", 
        style=discord.ButtonStyle.success,
        emoji="💖"
    )
    async def yes_callback(self, button, interaction):
        for button in self.children:
            button.disabled = True
        emb = get_embed("a", self.ctx, self.joke)
        create(self.ctx.author.id, self.joke.id)
        await interaction.response.edit_message(embed=emb, view=self)
    @discord.ui.button(
        label="ㅤNoㅤ", 
        style=discord.ButtonStyle.danger,
        emoji="💔"
    )
    async def no_callback(self, button, interaction):
        for button in self.children:
            button.disabled = True
        emb = get_embed("d", self.ctx, self.joke)
        await interaction.response.edit_message(embed=emb, view=self)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user == self.joke:
            #await interaction.response.send_message("NO", ephemeral=True)
            return True
        else:
            await interaction.response.send_message("This is not for you!", ephemeral=True)
            return False

    async def on_timeout(self):
        for btn in self.children:
            btn.disabled=True
        await self.ctx.edit(view=self)

class DivView(View):
    def __init__(self, ctx, partner):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.partner = partner
    
    @discord.ui.button(
        label="ㅤYesㅤ", 
        style=discord.ButtonStyle.danger,
        emoji="💔"
    )
    async def yes_callback(self, button, interaction):
        for button in self.children:
            button.disabled = True
        remove(self.ctx.author.id, self.partner.id)
        await interaction.response.edit_message(content=f"`{interaction.user}` has divorced with {self.partner} ╯︿╰", view=self)
    @discord.ui.button(
        label="ㅤNoㅤ", 
        style=discord.ButtonStyle.success,
        emoji="💝"
    )
    async def no_callback(self, button, interaction):
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(content=f"{interaction.user} decided not to divorce {self.partner} (╯▽╰ )", view=self)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user == self.ctx.author:
            #await interaction.response.send_message("NO", ephemeral=True)
            return True
        else:
            await interaction.response.send_message("This message is not for you!", ephemeral=True)
            return False

    async def on_timeout(self):
        for btn in self.children:
            btn.disabled=True
        await self.ctx.edit(view=self)

class Button(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.command()
    # async def mr(self, ctx, u:discord.User=None):
    #     if u is None:
    #         u = ctx.author
    #     view = MarryView(ctx)
    #     await ctx.send("Marriage Proposal", view=view)

    @slash_command(
        name="marry", 
        description="Virtually marry a person uwu"
    )
    async def s(self, ctx, u:discord.User):
        if u == ctx.author:
            await ctx.respond("You want to marry yourself.. I feel bad for you emo boy/girl :pensive: May you get a real partner soon, I'll pray for you. And `NO`, I won't allow self marriage, sorry for that.")    
        elif u.bot:
            if u.id == self.client.user.id:
                await ctx.respond("I'm underage!! ewww don't tell me you're into younger girls, you `PEDO`, I'm calling the FBI.")
            else:
                await ctx.respond("Okay, so you want to marry a `BOT` now, look it's okay to be single and not able being able to impress real girls/boys or egirls/ebois but you can't show your weakness like this in public by trying to marry a bot. Also, I'm a bot myself, and I won't allow it at all, sorry for that.")
        else:
            await ctx.defer()
            if not mcheck(ctx.author.id, u.id):
                e = get_embed("m", ctx, u)
                view = MarryView(ctx, u)
                await ctx.respond(u.mention, embed=e, view=view)
            else:
                await ctx.respond("Wait.. You're already married, control your emotions!")
    
    @slash_command(
        name="marriage",
        description="See anyone's marriage status."
    )
    async def marriage(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        await ctx.defer()
        if scheck(user.id):
            partner = self.client.get_user(int(return_partner(user.id)))
            partner_name = str(partner)
            then = return_time(user.id)
            d, h = get_date_heart(user.id)
            dt = check_date(user.id)
            thatday = datetime.datetime.strptime(then ,'%Y-%m-%d')
            month = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
            emb = discord.Embed(description=f"· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·\n●˚◞♡  ⃗ ꒰**{user}**꒱ is married to ꒰**{partner_name}**꒱ uwu\n{cont2} ✿ Married since **{thatday.day} {month[thatday.month]}, {thatday.year}**\n{cont2} ✿ Dates Together: **{d}**\n{cont2} ✿ Hearts: **{h}**\n{cont} ✿ Dated Today? **{'Yes!' if dt is True else 'No!'}**\n· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·", color=ec)
            emb.set_author(
                name=f"˚₊· ͟͟͞͞➳❥ {ctx.author.name.lower()}'s Marriage Card",
                icon_url=ctx.author.display_avatar
            )
            emb.set_footer(
            text=f"❀ Requested by {ctx.author.display_name}\n❀ Made by Kanna Chan",
            icon_url=self.client.user.display_avatar
            )
            await ctx.respond(embed=emb)
        else:
            await ctx.respond("They/You are not married yet.")

    @slash_command(
        name="date",
        description="Date your partner to get hearts!"
    )
    async def date(self, ctx, partner: discord.User):
        if check_partner(ctx.author.id, partner.id):
            await ctx.defer()
            if check_date(ctx.author.id) is False:
                heart = random.randint(30, 101)
                add_date_hearts(ctx.author.id, partner.id, heart)
                emb = discord.Embed(description=f"●˚◞♡  ⃗ ꒰{ctx.author.display_name}꒱ and ꒰{partner.display_name}꒱ go on a date together uwu\n{cont} ✿ **{heart}** hearts collected!", color=ec)
                emb.set_author(
                    name="Date",
                    icon_url=ctx.author.display_avatar
                )
                emb.set_image(url="https://i.pinimg.com/originals/c2/49/9c/c2499c5b2e996102e50ec939603999d3.gif")
                emb.set_footer(
                    text=f"❀ Requested by {ctx.author.display_name}\n❀ Made by Kanna Chan",
                    icon_url=self.client.user.display_avatar
                )
                await ctx.respond(embed=emb)
            else:
                await ctx.respond("You already dated once today, You can date gain tomorrow.")
        else:
            await ctx.respond("Either you have forgot who your partner is that you want to divorce or your partner doesn't exist which means you aren't married. Check you marital status using `kana marriage`.")

    @slash_command(
        name = "divorce",
        description = "Divorce with your partner cus why not."
    )
    async def divorce(self, ctx, partner:discord.User):
        if check_partner(ctx.author.id, partner.id):
            view = DivView(ctx, partner)
            await ctx.respond(f"{ctx.author.mention}\nAre you sure you want to get divorce with `{partner}`?", view=view)
        else:
            await ctx.respond("Either you have forgot who your partner is that you want to divorce or your partner doesn't exist which means you aren't married. Check you marital status using `kana marriage`.")

    
class NMarriage(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reset_date_status.start()

    async def get_lb(self, auth):
        lb_dict = {}
        user_list = []
        desc = f""
        all_users = db.child("MARRIAGE").get()
        for user in all_users.each():
            uid = user.key()
            user_list.append(uid)
            h = db.child("MARRIAGE").child(uid).child("HEARTS").get().val()
            lb_dict[uid] = h
        sort_lb = dict(sorted(lb_dict.items(), key=lambda x: x[1], reverse=True))
        slb = dict(list(sort_lb.items())[:10])
        print(slb)
        for u in slb: 
            #print(await self.client.fetch_user(int(u)))
            pos = list(slb.keys()).index(u) + 1
            he = sort_lb[u]
            if pos == 1:
                d, he = get_date_heart(int(u))
                desc += f"`#01.` `{await self.client.fetch_user(int(u))} + {await self.client.fetch_user(return_partner(int(u)))}`\n> {cont2} Dates Together: `{d}`\n> {cont} Hearts: `{he}`\n"
            elif pos == 10:  # ONE SPACE LESSER
                d, he = get_date_heart(int(u))
                desc += f"`#{str(pos)}.` `{await self.client.fetch_user(int(u))} + {await self.client.fetch_user(return_partner(int(u)))}`\n> {cont2} Dates Together: `{d}`\n> {cont} Hearts: `{he}`\n"
            else:
                d, he = get_date_heart(int(u))
                desc += f"`#0{str(pos)}.` `{await self.client.fetch_user(int(u))} + {await self.client.fetch_user(return_partner(int(u)))}`\n> {cont2} Dates Together: `{d}`\n> {cont} Hearts: `{he}`\n"
        posi = list(sort_lb.keys()).index(str(auth.id)) + 1
        if posi > 10:
            d, he = get_date_heart(int(auth.id))
            desc += f".\n.\n`#{str(posi)}.` `{auth} + {await self.client.fetch_user(return_partner(int(auth.id)))}`\n> {cont2} Dates Together: `{d}`\n> {cont} Hearts: `{he}`\n"
        emb = discord.Embed(description=f"\n{desc}\n", color=ec)
        emb.set_author(
            name="Global Marriage Leaderboard",
            icon_url=auth.display_avatar
        )
        emb.set_footer(
            text=f"❀ Requested by {auth.display_name}\n❀ Made by Kanna Chan",
            icon_url=self.client.user.display_avatar
        )
        return emb

    async def get_guild_lb(self, guild: discord.Guild, auth):
        lb_dict = {}
        desc = f""
        all_users = db.child("MARRIAGE").get()
        for user in all_users.each():
            uid = user.key()
            if guild.get_member(int(uid)) is not None:
                h = db.child("MARRIAGE").child(uid).child("HEARTS").get().val()
                lb_dict[uid] = h
        sort_lb = dict(sorted(lb_dict.items(), key=lambda x: x[1], reverse=True))
        slb = dict(list(sort_lb.items())[:10])
        for u in slb: 
            #print(await self.client.fetch_user(int(u)))
            pos = list(slb.keys()).index(u) + 1
            he = sort_lb[u]
            if pos == 1:
                d, he = get_date_heart(int(u))
                desc += f"`#01.` `{await self.client.fetch_user(int(u))} + {await self.client.fetch_user(return_partner(int(u)))}`\n> {cont2} Dates Together: `{d}`\n> {cont} Hearts: `{he}`\n"
            elif pos == 10:  # ONE SPACE LESSER
                d, he = get_date_heart(int(u))
                desc += f"`#{str(pos)}.` `{await self.client.fetch_user(int(u))} + {await self.client.fetch_user(return_partner(int(u)))}`\n> {cont2} Dates Together: `{d}`\n> {cont} Hearts: `{he}`\n"
            else:
                d, he = get_date_heart(int(u))
                desc += f"`#0{str(pos)}.` `{await self.client.fetch_user(int(u))} + {await self.client.fetch_user(return_partner(int(u)))}`\n> {cont2} Dates Together: `{d}`\n> {cont} Hearts: `{he}`\n"
        posi = list(sort_lb.keys()).index(str(auth.id)) + 1
        if posi > 10:
            d, he = get_date_heart(int(auth.id))
            desc += f".\n.\n`#{str(posi)}.` `{auth} + {await self.client.fetch_user(return_partner(int(auth.id)))}`\n> {cont2} Dates Together: `{d}`\n> {cont} Hearts: `{he}`\n"
        emb = discord.Embed(description=f"\n{desc}\n", color=ec)
        emb.set_author(
            name="Guild Marriage Leaderboard",
            icon_url=auth.display_avatar
        )
        emb.set_footer(
            text=f"❀ Requested by {auth.display_name}\n❀ Made by Kanna Chan",
            icon_url=self.client.user.display_avatar
        )
        return emb

    @commands.command()
    async def divorce(self, ctx, partner:discord.User):
        if check_partner(ctx.author.id, partner.id):
            view = DivView(ctx, partner)
            msg = await ctx.send(f"{ctx.author.mention}\nAre you sure you want to get divorce with `{partner}`?", view=view)
            async def timeout():
                for btn in view.children:
                    btn.disabled=True
                await msg.edit(view=view)
            view.on_timeout = timeout
        else:
            await ctx.send("Either you have forgot who your partner is that you want to divorce or your partner doesn't exist which means you aren't married. Check you marital status using `kana marriage`.")
    
    @commands.command()
    async def marriage(self, ctx, user:discord.User=None):
        user = ctx.author if user is None else user
        ms1 = await ctx.send("Checking your details..")
        if scheck(user.id):
            await ms1.delete()
            msg=await ctx.send("Getting your marriage card..")
            partner = self.client.get_user(int(return_partner(user.id)))
            partner_name = str(partner)
            then = return_time(user.id)
            d, h = get_date_heart(user.id)
            dt = check_date(user.id)
            thatday = datetime.datetime.strptime(then ,'%Y-%m-%d')
            month = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
            emb = discord.Embed(description=f"· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·\n●˚◞♡  ⃗ ꒰**{user}**꒱ is married to ꒰**{partner_name}**꒱ uwu\n{cont2} ✿ Married since **{thatday.day} {month[thatday.month]}, {thatday.year}**\n{cont2} ✿ Dates Together: **{d}**\n{cont2} ✿ Hearts: **{h}**\n{cont} ✿ Dated Today? **{'Yes!' if dt is True else 'No!'}**\n· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·", color=ec)
            emb.set_author(
                name=f"˚₊· ͟͟͞͞➳❥ {ctx.author.name.lower()}'s Marriage Card",
                icon_url=ctx.author.display_avatar
            )
            emb.set_footer(
            text=f"❀ Requested by {ctx.author.display_name}\n❀ Made by Kanna Chan",
            icon_url=self.client.user.display_avatar
            )
            await ctx.send(embed=emb)
            await msg.delete()
        else:
            await ms1.delete()
            await ctx.reply("They/You are not married yet.")

    @commands.command()
    async def marry(self, ctx, u:discord.User=None):
        if u == ctx.author:
            await ctx.reply("You want to marry yourself.. I feel bad for you emo boy/girl :pensive: May you get a real partner soon, I'll pray for you. And `NO`, I won't allow self marriage, sorry for that.")
        elif u is None:
            await ctx.reply("Who do you want to marry? Please use this command correctly, `kana marry @someone_who_likes_discord_marriages`.")
        elif u.bot:
            if u.id == self.client.user.id:
                await ctx.reply("I'm underage!! ewww don't tell me you're into younger girls, you `PEDO`, I'm calling the FBI.")
            else:
                await ctx.reply("Okay, so you want to marry a `BOT` now, look it's okay to be single and not able being able to impress real girls/boys or egirls/ebois but you can't show your weakness like this in public by trying to marry a bot. Also, I'm a bot myself, and I won't allow it at all, sorry for that.")
        else:
            if not mcheck(ctx.author.id, u.id):
                mg = await ctx.send("Getting your documents ready..")
                e = get_embed("m", ctx, u)
                view = MarryView(ctx, u)
                msg = await ctx.send(u.mention, embed=e, view=view)
                await mg.delete()
                async def timeout():
                    for btn in view.children:
                        btn.disabled=True
                    await msg.edit(view=view)
                view.on_timeout = timeout
            else:
                await ctx.reply("Wait.. You're already married, control your emotions!")
    
    @commands.command()
    async def date(self, ctx, partner: discord.User=None):
        if partner is None:
            await ctx.reply("Please use this command like `kana date @partner`.")
        else:
            if check_partner(ctx.author.id, partner.id):
                if check_date(ctx.author.id) is False:
                    heart = random.randint(30, 101)
                    add_date_hearts(ctx.author.id, partner.id, heart)
                    emb = discord.Embed(description=f"●˚◞♡  ⃗ ꒰{ctx.author.display_name}꒱ and ꒰{partner.display_name}꒱ go on a date together uwu\n{cont} ✿ **{heart}** hearts collected!", color=ec)
                    emb.set_author(
                        name="Date",
                        icon_url=ctx.author.display_avatar
                    )
                    emb.set_image(url="https://i.pinimg.com/originals/c2/49/9c/c2499c5b2e996102e50ec939603999d3.gif")
                    emb.set_footer(
                        text=f"❀ Requested by {ctx.author.display_name}\n❀ Made by Kanna Chan",
                        icon_url=self.client.user.display_avatar
                    )
                    await ctx.send(embed=emb)
                else:
                    await ctx.reply("You already dated once today, You can date gain tomorrow.")
            else:
                await ctx.reply("Either you have forgot who your partner is or it seems you are not married yet, poor guy. Check your marital staus by sending `kana marriage`.")


    @commands.command()
    @commands.is_owner()
    async def mds(self, ctx):
        all_users = db.child("MARRIAGE").get()
        if all_users.each() != None:
            for users in all_users.each():
                db.child("MARRIAGE").child(users.key()).update({"DATE_TODAY":"False"})
        owner = self.client.get_user(self.client.owner_id)
        await owner.send("`>> Marriage Date Status has been RESET.`")

    @commands.command()
    async def mlb(self, ctx, *, arg: str = None):
        if arg == None:
            await ctx.send(embed = await self.get_guild_lb(ctx.guild, ctx.author))
        elif arg.lower() == "guild":
            await ctx.send(embed = await self.get_guild_lb(ctx.guild, ctx.author))
        elif arg.lower() == "global":
            await ctx.send(embed = await self.get_lb(ctx.author))
        
        else:
            emb = discord.Embed(description="Commands Available:\n> `mlb guild` for server marriage leaderboard.\n> `mlb global` for global marriage leaderboard.", color=ec)
            emb.set_author(
                name="Invalid Argument!",
                icon_url=ctx.author.display_avatar
            )
            await ctx.send(embed=emb)

    @commands.command()
    @commands.is_owner()
    async def upr(self, ctx):
        us = db.child("MARRIAGE").get()
        for u in us.each():
            db.child("MARRIAGE").child(u.key()).update({"DATE_TODAY":"False"})
        await ctx.send("done")

    @tasks.loop(minutes=60.0, reconnect=True)
    async def reset_date_status(self):
        now = datetime.datetime.now(timezone('Asia/Kolkata'))
        if now.hour == 0:
            all_users = db.child("MARRIAGE").get()
            for users in all_users.each():
                db.child("MARRIAGE").child(users.key()).update({"DATE_TODAY":"False"})
            owner = self.client.get_user(784363251940458516)
            await owner.send("`>> Marriage Date Status has been RESET.`")
    

def setup(client):
    client.add_cog(Button(client))
    client.add_cog(NMarriage(client))
    print(">> Marriage Loaded.")

        
