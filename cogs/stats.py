"""
This file updates the database with stats of bot evry hour.
These stats are used in the website/API.
"""

import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import command
import json
from decouple import config
import json
import pyrebase

firebaseconfig = json.loads(config("FIREBASE_CONFIG"))

firebase = pyrebase.initialize_app(firebaseconfig)
db = firebase.database()


def update_stats(servers: int, members: int):
    db.child("stats").child("servers").set(servers)
    db.child("stats").child("members").set(members)


class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.update_stats.start()

    @tasks.loop(minutes=60.0, reconnect=True)
    async def update_stats(self):
        servers = len(self.client.guilds)
        members = len(self.client.users)
        update_stats(servers, members)

    @commands.command()
    @commands.is_owner()
    async def us(self, ctx):
        self.update_stats()
        await ctx.send("Updated stats.")


def setup(client):
    client.add_cog(Stats(client))
    print(">> Stats loaded")
