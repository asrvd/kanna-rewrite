import discord
from discord.ext import commands
#from discord_slash import SlashCommand
import os

intents = discord.Intents.default()
intents.members = True


client = commands.Bot(command_prefix=commands.when_mentioned_or('.'), case_insensitive=True, intents=intents)
#slash = SlashCommand(client, sync_commands=True)

def load_cogs():
  for file in os.listdir("./cogs"):
    if file.endswith(".py") and not file.startswith("_"):
      client.load_extension(f"cogs.{file[:-3]}")

load_cogs()

@client.event
async def on_ready():
  print(">> Cogs Loaded.")
  print(f">> Logged in as : {client.user.name} \n>> ID : {client.user.id}")
  print(f">> Total Servers : {len(client.guilds)}")
  print('>> Bot is Online.')


client.run("OTIyODg3MzE3MjE4Mjc5NDQ0.YcH_yg.7qGodcuL_W1V5soWQ7LOM9-o6Ak")

