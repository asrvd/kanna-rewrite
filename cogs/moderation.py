import discord
from discord.ext import commands
from discord.ui import View, Button
from discord.commands import slash_command
import datetime

class Mod(commands.Cog):
    def __init__(self, client):
        self.client=client
    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, user:discord.Member=None, *, reason:str = None):
        if user is None:
            await ctx.reply("You need to mention someone to ban!")
        else:
            await user.ban(reason=reason)
            await ctx.send(f"> `🔨` *Banned {user}*\n> *Reason - {reason if reason is not None else 'None'}*")
            await user.send(embed=discord.Embed(description=f"You were banned from **{ctx.guild.name}**\nReason ~ **{reason}**"))

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user:discord.Member=None, *, reason:str = None):
        if user is None:
            await ctx.reply("You need to mention someone to ban!")
        else:
            await user.kick(reason=reason)
            await ctx.send(f"> `🚪` *Kicked {user}*\n> *Reason - {reason if reason is not None else 'None'}*")
            await user.send(embed=discord.Embed(description=f"You were kicked from **{ctx.guild.name}**\nReason ~ **{reason}**"))

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, user:discord.Member=None, time="1m", *, reason:str = None):
        time_unit = {"s":"seconds", "m":"minutes", "h":"hours", "d":"days"}
        time_convert = {"s": 1, "h":3600, "d":86400, "m" : 60}
        tempmute= int(time[:-1]) * time_convert[time[-1]]
        until = discord.utils.utcnow() + datetime.timedelta(seconds=tempmute)
        await user.timeout(until)
        await ctx.reply(
            f'> `⏲`**{user}** was timed out for **{f"{time[:-1]} {time_unit[time[-1]]}"}**.\n> Reason: **{reason}**'
        )

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, user:discord.Member=None):
        if user.timed_out:
            await user.remove_timeout()
            await ctx.reply(f"> `⏲`**{user}** was unmuted by **{ctx.author.name}**.")
        else:
            await ctx.reply("> The user is not Muted/TimedOut~")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id):
        if self.client.get_user(int(user_id)) is None:
            await ctx.reply("Couldn't find any user with this id!")
        else:
            user = self.client.get_user(int(user_id))
            print(user)
            banned_members = await ctx.guild.bans()
            member_name, member_discriminator = str(user).split("#")

            for ban_entry in banned_members:
                u = ban_entry.user
                if (u.name, u.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.reply(f'Unbanned {user.mention}')
                    link = await ctx.channel.create_invite(max_age = 0, max_uses = 0)
                    await user.send(f"You were unbanned from server **{ctx.guild.name}**\nyou can join the server using this link: {link}")
                else:
                    await ctx.reply("The user is not banned from this guild!")
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def lock(self, ctx, channel:discord.TextChannel=None, *, reason:str = None):
        channel = ctx.channel if channel is None else channel
        reason = "None" if reason is None else reason
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.reply(f'> `🔒` {channel.mention} locked.\n> Reason: **{reason}**.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unlock(self, ctx, channel:discord.TextChannel=None, *, reason:str = None):
        channel = ctx.channel if channel is None else channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages is False:
            overwrite.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.reply(f'> `🔓` {channel.mention} Unlocked.')
        else:
            await ctx.reply("Channel is not locked!")

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def purge(self, ctx, count: int = 1):
        await ctx.channel.purge(limit=count)
        await ctx.send(f'Purged {count} messages from channel.', delete_after=15)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"Try again in {error.retry_after:.2f} seconds.", delete_after=10)

    @ban.error
    async def ban_error(self, ctx, error):
        #print(error)
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You don't have enough permissions to use this command.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply("Kanna doesn't have the required permissions to use this action! `Ban Members` or  `Administrator` permissions required!")

    @unban.error
    async def unban_error(self, ctx, error):
        #print(error)
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You don't have enough permissions to use this command.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply("Kanna doesn't have the required permissions to use this action! `Ban Members` or  `Administrator` permissions required!")

    @kick.error
    async def kick_error(self, ctx, error):
        #print(error)
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You don't have enough permissions to use this command.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply("Kanna doesn't have the required permissions to use this action! `Kick Members` or  `Administrator` permissions required!")

    @mute.error
    async def mute_error(self, ctx, error):
        #print(error)
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You don't have enough permissions to use this command.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply("Kanna doesn't have the required permissions to use this action! `Moderate Members` or  `Administrator` permissions required!")

    @unmute.error
    async def unmute_error(self, ctx, error):
        #print(error)
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You don't have enough permissions to use this command.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply("Kanna doesn't have the required permissions to use this action! `Moderate Members` or  `Administrator` permissions required!")

    @lock.error
    async def lock_error(self, ctx, error):
        #print(error)
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You don't have enough permissions to use this command.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply("Kanna doesn't have the required permissions to use this action! `Manage Channels` or  `Administrator` permissions required!")

    @unlock.error
    async def unlock_error(self, ctx, error):
        #print(error)
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You don't have enough permissions to use this command.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply("Kanna doesn't have the required permissions to use this action! `Manage Channels` or  `Administrator` permissions required!")

def setup(client):
    client.add_cog(Mod(client))
    print(">> Mod Loaded.")
