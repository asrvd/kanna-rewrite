from typing import Any, Type
import kitsu
import asyncio
from ._config import ec
import discord

client = kitsu.Client()


async def get_anime_info(arg: str, user):
    try:
        data = await client.search_anime(arg, limit=1)
        try:
            end = str(data.end_date)[:10]
        except TypeError:
            end = "none"
        try:
            start = str(data.start_date)[:10]
        except TypeError:
            start = "Not Released"
        try:
            eco = data.episode_count
        except TypeError:
            eco = "None"
        try:
            el = data.episode_length
        except TypeError:
            el = "None"
        emb = discord.Embed(
            description=f"**-꒰ About ꒱-**\n*{data.synopsis}*\n\n**-꒰ Overview ꒱-**\n> ❀ Title: `{data.canonical_title}`\n> ❀ JP Title: `{data.title('ja_jp')}`\n> ❀ Type: `{data.show_type}`\n> ❀ Status: `{data.status.capitalize()}`\n> ❀ Popularity: `#{data.popularity_rank}`\n> ❀ Rating Rank: `#{data.rating_rank}`\n> ❀ Average rating: `{data.average_rating}%`\n> ❀ NSFW: `{'Yes' if data.nsfw==True else 'No'}`\n> ❀ Age Rating: `{data.age_rating_guide}`\n> ❀ Episodes: `{eco} @ {el} minutes each`\n> ❀ Aired: `{start} to {end}`",
            color=ec,
        )
        emb.set_author(name="Anime Info", icon_url=user.display_avatar)
        try:
            emb.set_image(url=data.cover_image())
        except AttributeError:
            return
        return emb
    except kitsu.errors.NotFound as e:
        return "Not found"
