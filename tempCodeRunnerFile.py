
@client.event
async def on_ready():
  print(">> Cogs Loaded.")
  print(f">> Logged in as : {client.user.name} \n>> ID : {client.user.id}")
  print(f">> Total Servers : {len(client.guilds)}")
  print('>> Bot is Online.')


client.run("OTIyODg3MzE3MjE4Mjc5NDQ0.YcH_yg.7qGodcuL_W1V5soWQ7LOM9-o6Ak")

