import asyncio

import discord
from discord.ext import commands
from discord.utils import get

from lucid_bot.lucid_embed import lucid_embed


class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mute")
    @commands.has_permissions(kick_members=True)
    async def _mute(self, ctx: commands.Context, *args) -> None:

        if not args:
            embed = lucid_embed(
                ctx,
                title="Punishment -",
                description="Which user should be muted?",
            )

            message: discord.Message = await ctx.send(embed=embed)

            while True:

                try:
                    mute_user_message: discord.Message = await self.bot.wait_for(
                        "message", timeout=15
                    )

                except asyncio.TimeoutError:
                    embed = lucid_embed(
                        ctx,
                        fail=True,
                        title="Timeout -",
                        description="Sorry, you took too long to respond.",
                    )
                    await message.edit(embed=embed)

                    return None

                if mute_user_message.author.id == ctx.author.id:
                    await mute_user_message.delete()

                    try:
                        role = get(ctx.guild.roles, name="Muted")

                        if not role:
                            role: discord.Role = await ctx.guild.create_role(
                                name="Muted"
                            )

                            for channel in ctx.guild.channels:
                                await channel.set_permissions(
                                    role,
                                    send_messages=False,
                                    speak=False,
                                )

                        await mute_user_message.mentions[0].add_roles(role)
                        await ctx.message.delete()

                        embed = lucid_embed(ctx, success=True).set_author(
                            name=f"| Successfully muted {mute_user_message.mentions[0]}.",
                            icon_url="https://i.imgur.com/4yUeOVj.gif",
                        )
                        await message.edit(embed=embed)

                        return None

                    except IndexError:
                        embed = lucid_embed(
                            ctx,
                            fail=True,
                            title="Punishment Failed -",
                            description="Did you mention a user?",
                        )
                        await message.edit(embed=embed)

                        return None

                    except discord.errors.Forbidden:
                        embed = lucid_embed(
                            ctx,
                            fail=True,
                            title="Permissions Error -",
                            description="Are you trying to mute another "
                            "moderator/administrator?",
                        )
                        await message.edit(embed=embed)

                        return None
        else:
            mute_user: str = ctx.message.mentions[0]
            await ctx.message.delete()

            try:
                role: discord.Role = get(ctx.guild.roles, name="Muted")

                if not role:
                    role = await ctx.guild.create_role(name="Muted")

                    for channel in ctx.guild.channels:
                        await channel.set_permissions(
                            role, send_messages=False, speak=False
                        )

                await mute_user.add_roles(role)

                embed = lucid_embed(ctx, success=True).set_author(
                    name=f"| Successfully muted {mute_user}",
                    icon_url="https://i.imgur.com/4yUeOVj.gif",
                )
                await ctx.send(embed=embed)

                return None

            except IndexError:
                embed = lucid_embed(
                    ctx,
                    fail=True,
                    title="Punishment Failed -",
                    description="Did you mention a user?",
                )
                await ctx.send(embed=embed)

                return None

            except discord.errors.Forbidden:
                embed = lucid_embed(
                    ctx,
                    fail=True,
                    title="Permissions Error -",
                    description="Are you trying to ban another "
                    "moderator/administrator?",
                )
                await ctx.send(embed=embed)

                return None


def setup(bot):
    bot.add_cog(Mute(bot))
