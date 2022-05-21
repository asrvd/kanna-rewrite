from typing import Any, Type
import kitsu
import asyncio
from ._config import ec
import discord

client = kitsu.Client()

async def get_manga_info(arg: str, user):
    try:
        data = await client.search_manga(arg, limit=1)
        try:
            end = str(data.end_date)[:10]
        except TypeError:
            end = "none"
        try:
            start = str(data.start_date)[:10]
        except TypeError:
            start = "Not Released"
        try:
            cco = data.chapter_count
        except TypeError:
            cco = "None"
        try:
            vco = data.volume_count
        except TypeError:
            vco = "None"
        try:
            se = data.serialization
        except TypeError:
            se = "None"
        emb = discord.Embed(
        description=f"**-꒰ About ꒱-**\n*{data.synopsis}*\n\n**-꒰ Overview ꒱-**\n> ❀ Title: `{data.canonical_title}`\n> ❀ Status: `{data.status.capitalize()}`\n> ❀ Popularity: `#{data.popularity_rank}`\n> ❀ Rating Rank: `#{data.rating_rank}`\n> ❀ Average rating: `{data.average_rating}%`\n> ❀ Age Rating: `{data.age_rating_guide}`\n> ❀ Chapters: `{cco}`\n> ❀ Volumes: `{vco}`\n> ❀ Serialization: `{se}`\n> ❀ Published: `{start} to {end}`",
        color=ec
        )
        emb.set_author(
            name="Manga Info",
            icon_url=user.display_avatar
        )
        try:
            emb.set_image(url=data.cover_image())
        except AttributeError:
            return
        return emb
    except kitsu.errors.KitsuError as e:
        return "Not found"
