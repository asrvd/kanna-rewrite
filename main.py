import discord
from discord.ext import commands
#from discord_slash import SlashCommand
import os
from decouple import config

intents = discord.Intents.default()
intents.members = True
intents.presences = True


client = commands.Bot(command_prefix=commands.when_mentioned_or('.'), case_insensitive=True, intents=intents)
client.remove_command("help")
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
  await client.change_presence(status=discord.Status.online, activity=discord.Streaming(name="Christmas Carols", url="https://www.twitch.tv/asheeeshh"))
  print('>> Bot is Online.')
  

@client.command()
async def reload(ctx):
  for file in os.listdir("./cogs"):
    if file.endswith(".py") and not file.startswith("_"):
      client.reload_extension(f"cogs.{file[:-3]}")
  await ctx.send("Cogs Reloaded.")


client.load_extension('jishaku')
client.run(str(config("BOT_TOKEN")))
