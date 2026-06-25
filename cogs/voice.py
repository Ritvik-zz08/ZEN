"""
Voice Cog — Voice Channel connection commands.
Requires:
    pip install PyNaCl
"""

import discord
from discord.ext import commands


class Voice(commands.Cog, name="Voice"):
    """🔊 Voice channel commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── Zjoin ─────────────────────────────────────────────────────────────
    @commands.command(name="join", aliases=["connect"])
    async def join(self, ctx: commands.Context):
        """Join the voice channel you are currently in."""
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send(
                embed=discord.Embed(
                    description="⚠️ You need to be in a voice channel first!",
                    color=0xFFA500,
                )
            )
            return

        channel = ctx.author.voice.channel

        # If already in a voice channel, move to the new one
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()

        await ctx.send(
            embed=discord.Embed(
                description=f"✅ Joined **{channel.name}**",
                color=0x2ECC71,
            )
        )

    # ── Zleave ────────────────────────────────────────────────────────────
    @commands.command(name="leave", aliases=["disconnect"])
    async def leave(self, ctx: commands.Context):
        """Disconnect from the current voice channel."""
        if ctx.voice_client is None:
            await ctx.send(
                embed=discord.Embed(
                    description="❌ I am not connected to any voice channel.",
                    color=0xFF4444,
                )
            )
            return

        channel_name = ctx.voice_client.channel.name
        await ctx.voice_client.disconnect()
        await ctx.send(
            embed=discord.Embed(
                description=f"👋 Disconnected from **{channel_name}**",
                color=0x3498DB,
            )
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Voice(bot))
