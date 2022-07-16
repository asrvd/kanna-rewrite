import discord
from discord.ext import commands
import os
from decouple import config

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.message_content = True

client = commands.Bot(
    command_prefix=commands.when_mentioned_or(
        "kanna ", "kana ", "k.", "K.", "Kanna ", "Kana "
    ),
    case_insensitive=True,
    intents=intents,
)
client.remove_command("help")


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
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="Shield Hero S2"
        ),
    )
    print(">> Kanna is Online.")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(f"Missing required argument, `{error.param}`")
    elif isinstance(error, commands.BadArgument):
        if ctx.command.usage is not None:
            await ctx.reply(f"Invalid arguments, Example: `{ctx.command.usage}`")
        else:
            await ctx.reply("Incorrect arguments given")


@client.command()
async def reload(ctx):
    for file in os.listdir("./cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.reload_extension(f"cogs.{file[:-3]}")
    await ctx.send("Cogs Reloaded.")


# client.load_extension('jishaku')
client.run(str(config("BOT_TOKEN")))
