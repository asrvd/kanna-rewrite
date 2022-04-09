from os import name
import discord
from ._config import ec

cont = "<:reply:928274405358993418>"
cont2 = "<:reply_cont:962182412467572787>"

#Embed Descriptions

utildesc = f"**-꒰ Instructions ꒱-**\n> ❀ `[ ]`: Optional.\n> ❀ `< >`: Required.\n\n**-꒰ Commands ꒱-**\n> ❀ `afk [message]`\n> {cont} sets your AFK status.\n> ❀ `define <text>`\n> {cont2} get the defintion of any word/line.\n> {cont} slash command available!\n> ❀ `spotify <user>`\n> {cont2} display the user's spotify activity.\n> {cont} slash command available!\n> ❀ `ui [user]`\n> {cont} displays info about any user.\n> ❀ `enlarge <emote>`\n> {cont} enlarge emotes.\n> ❀ `lyrics <song name>`\n> {cont2} get lyrics for any song.\n> {cont} slash command available.\n> ❀ Welcome Message `BETA`\n> {cont2} `wsetup <#channel>` set up welcome message for your server.\n> {cont} `wdisable` disable welcome messages for your server.\n> ❀ Chat with Kanna \n> {cont2} `chat_setup` Creates a new channel to chat with kanna.\n> {cont2} `chat_disable` Disables chat setup for server.\n> {cont} `chat_enable` Enables chat setup again.\n\n**-꒰ Avatar Commands ꒱-**\n> ❀ `av [user1/id] [user2/id]..`\n> {cont2} displays avatars aligned in one image.\n> {cont2} useful for shared avatars.\n> {cont2} pass one user/userID for 1 avatar.\n> {cont} only 2 avatars can be seen at a time for `slash command`\n> ❀ `avc <size>`\n> {cont2} creates a collage using random avatars from server.\n> {cont2} sizes: `5x5 | 6x6 | 7x7 | 8x8 | 9x9 | 10x10`\n> ❀ `avg <member>`\n> {cont} shows `Guild Avatar` of member if present.\n> ❀ `banner [user]`\n> {cont} sends banner of the user."

gamedesc = f"**-꒰ Instructions ꒱-**\n> ❀ `[ ]`: Optional.\n> ❀ `< >`: Required.\n\n**-꒰ Games ꒱-**\n> ❀ `rps <user>`\n> {cont2} play a game of Rock, Paper, Scissors with your friend.\n> {cont} slash command available!\n> ❀ `ship [user1] [user2]`\n> {cont2} ship two people to see their compatibilty.\n> {cont} slash command available!\n> ❀ `gte <user>`\n> {cont2} play a game of `Guess the Emote` with your friend.\n> {cont} slash command available.\n> ❀ `f <user/anything>`\n> {cont2} Pay your respects to a User or Anything, Kanna will coun the respects!\n> {cont} slash command available."

moddesc = f"**-꒰ Instructions ꒱-**\n> ❀ `[ ]`: Optional.\n> ❀ `< >`: Required.\n\n**-꒰ Commands ꒱-**\n> ❀ `mute <user> [duration] [reason]`\n> {cont2} mutes/timeouts user for `[duration]` ~ default - `1 minute`\n> {cont2} time should be in format `number|suffix(d/m/s)`.\n> {cont2} example: `mute @asheeshh 3m` will mute the user for `3 Minutes`.\n> {cont} slash command available!\n> ❀ `unmute <user>`\n> {cont2} unmutes a muted member.\n> {cont} slash command available!\n> ❀ `ban <user/user id> [reason]`\n> {cont2} Bans a member from guild.\n> {cont} slash command available!\n> ❀ `unban <user id>`\n> {cont2} unbans a banned member ~ `user ID` is needed!\n> {cont2} example: `unban 926870214254153739`.\n> {cont} slash command available!\n> ❀ `kick <user> [reason]`\n> {cont2} kicks a member from guild.\n> {cont} slash command avaialble!\n> ❀ `lock [channel]`\n> {cont2} locks the text channel.\n> {cont2} if None given locks the one where message was sent.\n> {cont} slash command avaialble!\n> ❀ `unlock [channel]`\n> {cont2} unlocks a locked channel.\n> {cont2} if None given unlocks the one where message was sent.\n> {cont} slash command avaialble!"

fundesc = f"**-꒰ Instructions ꒱-**\n> ❀ `[ ]`: Optional.\n> ❀ `< >`: Required.\n\n**-꒰ Action Commands ꒱-**\n> `bonk`, `kiss`, `kill`, `baka`, `boop`, `bite`, `cuddle`, `tickle`, `throw`, `tease`, `stare`, `punch`, `rawr`, `slap`, `pout`, `handhold`, `poke`, `flower`, `pat`, `nom`, `feed`, `love`, `lurk`, `highfive`, `hug`, `lick`, `wink`, `kick`\n\n> use `/action` for slash commands.\n\n**-꒰ Marriage Commands ꒱-**\n> ❀ `marry <user>`\n> {cont} marry a person virtually.\n> ❀ `divorce <partner>`\n> {cont} get divorced with your partner.\n\n**-꒰ Card Commands ꒱-**\n> ❀ `simpcard <user/thing>`\n> {cont2} creates a simpcard *blush*.\n> {cont} slash command available!\n> ❀ `gaycard`\n> {cont2} creates a gaycard.\n> {cont} slash command available!\n> ❀ `uwucard <user>`\n> {cont2} show your love for a person with this card uwu.\n> {cont} slash command available!\n\n**-꒰ Response Commands ꒱-**\n> ❀ `simp <user>`\n> {cont2} simp on anyone using kanna's pickup lines!\n> {cont} slash command available!\n> ❀ `aq`\n> {cont} sends a random anime quote.\n> ❀ `roast <user>`\n> {cont2} roast anyone using kanna's cruel words.\n> {cont} slash command available!\n> ❀ `dadjoke`\n> {cont2} get a random dadjoke.\n> {cont} slash command available!\n> ❀ `uwuify <text>`\n> {cont2} uwuify youwr wowds uwu.\n> {cont} slash command available!\n\n**-꒰ Image Commands ꒱-**\n> ❀ `meow`\n> {cont2} get a random cute catto image.\n> {cont} slash command available!\n> ❀ `woof`\n> {cont2} get a random cute doggo image.\n> {cont} slash command available!"

memedesc = f"**-꒰ Instructions ꒱-**\n> ❀ `[ ]`: Optional.\n> ❀ `< >`: Required.\n\n**-꒰ Normal Commands ꒱-**\n> `meme`, `headpat <user>`, `triggered <user>`, `gay <user>`, `eject <user>`, `rip <user>`, `hug <user>`, `bed <user>`, `batslap <user>`, `nani <user>`, `cuddle <user>`, `buttons <text1> <text2>`, `spiderman <text1> <text2>`, `tweet <text> [user]`, `tis <user>`, `gayrate`, `simprate`, `kawaiirate`\n\n**-꒰ Slash Commands ꒱-**\n> `/meme`, `/headpat <user>`, `/triggered`, `/gay`, `/meme eject <user>`, `/meme rip <user>`, `/meme hug <user>`, `/meme bed <user>`, `/meme batslap <user>`, `/meme nani <user>`, `/meme cuddle <user>`, `/meme buttons <text1> <text2>`, `/meme spiderman <text1> <text2>`, `/meme tweet <text> [user]`, `/meme tis <text1> <text2>`, `/gayrate`, `/simprate`, `/kawaiirate`"

ref = { #This dictionary sends the respective descriptions.
    "utility":utildesc,
    "games":gamedesc,
    "fun":fundesc,
    "moderation":moddesc,
    "memes":memedesc
}

cmd_ref={
    "utility":"Utility Commands",
    "fun":"Fun Related Commands",
    "games":"List of Games available",
    "moderation":"Moderation Commands",
    "memes":"Meme related Commands"
}

def get_help_embed(arg:str, user):
    emb = discord.Embed(description=ref[arg.lower()], color=ec)
    emb.set_author(
        name=cmd_ref[arg.lower()],
        icon_url=user.display_avatar
    )
    return emb
