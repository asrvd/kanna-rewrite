import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from io import BytesIO
import os
import pyrebase
import datetime

gi=[843823778755641344]
firebaseconfig=...
firebase = pyrebase.initialize_app(firebaseconfig)
db = firebase.database()

def create(mem1, mem2):    #stores marriage info in database
    now = str(datetime.date.today())
    db.child("MARRIAGE_TEST").child(mem1).set({"PARTNER": mem2, "TIME": now})

def mcheck(user1, user2 = None):   
    auth1 = db.child("MARRIAGE_TEST").child(user1).get().val()
    auth2 = db.child("MARRIAGE_TEST").child(user2).get().val()
    all_users = db.child("MARRIAGE_TEST").get()
    if all_users.each() != None:
        for user in all_users.each():
            partner = db.child("MARRIAGE_TEST").child(user.key()).child("PARTNER").get().val()
            if partner == user1 or partner == user2:
                return True
                break
    if auth1 != None or auth2 != None:
        return True
    else:
        return False

def scheck(user):   #checks if user is married or not
    auth1 = db.child("MARRIAGE_TEST").child(user).get().val()
    all_users = db.child("MARRIAGE_TEST").get()
    if all_users.each() != None:
        for users in all_users.each():
            partner = db.child("MARRIAGE_TEST").child(users.key()).child("PARTNER").get().val()
            if partner == user:
                return True
                break
    if auth1 != None:
        return True
    else:
        return False

def return_partner(user):  #returns ID of partner
    auth = db.child("MARRIAGE_TEST").child(user).get().val()
    if auth == None:
        all_users = db.child("MARRIAGE_TEST").get()
        if all_users.each() != None:
            for users in all_users.each():
                partner = db.child("MARRIAGE_TEST").child(users.key()).child("PARTNER").get().val()
                if partner == user:
                    p = users.key()
                    break
    else:
        p = db.child("MARRIAGE_TEST").child(user).child("PARTNER").get().val()
    return p

def check_partner(user1, user2):   #checks if person is his/her partner
    auth1 = db.child("MARRIAGE_TEST").child(user1).child("PARTNER").get().val()
    auth2 = db.child("MARRIAGE_TEST").child(user2).child("PARTNER").get().val()
    if user1 == auth2 or user2 == auth1:
        return True
    else:
        return False

def return_time(user):   #returns date of marriage
    auth = db.child("MARRIAGE_TEST").child(user).get().val()
    if auth == None:
        all_users = db.child("MARRIAGE_TEST").get()
        if all_users.each() != None:
            for users in all_users.each():
                partner = db.child("MARRIAGE_TEST").child(users.key()).child("PARTNER").get().val()
                if partner == user:
                    user = users.key()
            time = db.child("MARRIAGE_TEST").child(user).child("TIME").get().val()
    else:
        time = db.child("MARRIAGE_TEST").child(user).child("TIME").get().val()
    return time

def remove(user1, user2):  #removes user info after divorce
    list = [user1, user2]
    for user in list:
        auth = db.child("MARRIAGE_TEST").child(user).get().val()
        if auth != None:
            db.child("MARRIAGE_TEST").child(user).remove()


class marriage(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @cog_ext.cog_slash(
        name="Marry",
        description="Virtually marry a person uwu",
        guild_ids=gi,
        options=[
            create_option(
                name="user",
                description="user you want to marry.",
                option_type=6,
                required=True
            )
        ]
    )
    async def marry(self, ctx, user:discord.User=None):
        
