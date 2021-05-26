from datetime import datetime

import discord
from discord.colour import Color


def lucid_embed(ctx=None, success: bool = None, fail: bool = None, **kwargs):
    if success:
        kwargs["color"] = Color.green()

    elif fail:
        kwargs["color"] = Color.red()

    else:
        kwargs["color"] = int("2F3136", 16)


    embed = discord.Embed(**kwargs, timestamp=datetime.utcnow())

    if ctx:
        embed.set_footer(text=ctx.author)

    return embed
