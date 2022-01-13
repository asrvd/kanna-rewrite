import discord
from discord.ext import commands

class Status(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.statuses = [
            {"w":"Miss Kobayashi's Dragon Maid"},
            {"p":"Rolling in a Blanket"},
            {"l":"BlackBear"},
            {"w":f"k.help in {len(self.client.guilds)} Servers"},
            {"w":"Snowfall ❄"}
        ]
        self.activity = {
            "w":"Watching",
            "p":"Playing",
            "l":"Listening"
        }
        self.ref = {
            "1":"w",
            "2":"p",
            "3":"l",
            "4":"w",
            "5":"w"
        }
        self.discord_activity = {
            "w":discord.ActivityType.watching,
            "p":discord.ActivityType.playing,
            "l":discord.ActivityType.listening,
        }
    
    @commands.command()
    @commands.is_owner()
    async def cp(self, ctx, arg):
        print(arg)
        st = self.statuses[int(arg)-1][self.ref[str(arg)]]
        ac = self.activity[self.ref[str(arg)]]
        await ctx.send(f"{st} -> {ac}")
        await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=self.discord_activity[self.ref[str(arg)]], name=st))

def setup(client):
    client.add_cog(Status(client))
    print(">> Status Loaded.")
