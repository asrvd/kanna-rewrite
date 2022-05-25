import json
import pyrebase
from decouple import config

firebaseconfig=json.loads(config("FIREBASE_CONFIG"))
db = pyrebase.initialize_app(firebaseconfig).database()

def set_bookmark(
    user: int, 
    id: int, 
    name: str, 
    content: str, 
    author: str, 
    channel: str, 
    server: str, 
    created: str, 
    link: str
):
    db.child("BOOKMARKS").child(user).child(name.lower()).set(
        {
            "id": id, 
            "content": content, 
            "author": author, 
            "channel": channel, 
            "server": server, 
            "created": created, 
            "link": link
        }
    )
    # print("Bookmark added")

def get_bookmarks(user: int):
    return db.child("BOOKMARKS").child(user).get().val()

def get_bookmark(user: int, name: str):
    return db.child("BOOKMARKS").child(user).child(name.lower()).get().val()

def check_bookmark(user: int, name: str):
    exists = True if db.child("BOOKMARKS").child(user).child(name.lower()).get().val() is not None else False
    return exists

def remove_bookmark(user: int, name: str):
    db.child("BOOKMARKS").child(user).child(name.lower()).remove()
    # print("Bookmark removed")