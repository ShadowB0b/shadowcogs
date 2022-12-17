import discord

from redbot.core import commands

class VoiceMaster(commands.Cog):
    """Voice channel moderation"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def vcmute(self, ctx: commands.Context, *, member: discord.Member):
        """Mute a member in a voice channel"""
        if not member.voice:
            return await ctx.send("This member is not in a voice channel")
        if member.voice.mute:
            return await ctx.send("This member is already muted")
        try: 
            await member.edit(mute=True)
        except discord.Forbidden:
            return await ctx.send("I don't have permission to mute that member")
        await ctx.send(f"{member.mention} has been muted")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def vcunmute(self, ctx: commands.Context, *, member: discord.Member):
        """Unmute a member in a voice channel"""
        if not member.voice:
            return await ctx.send("This member is not in a voice channel")
        if not member.voice.mute:
            return await ctx.send("This member is not muted")
        try: 
            await member.edit(mute=False)
        except discord.Forbidden:
            await ctx.send("I don't have permission to unmute that member")
        await ctx.send(f"{member.mention} has been unmuted")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def deafen(self, ctx: commands.Context, *, member: discord.Member):
        """Deafen a member in a voice channel"""
        if not member.voice:
            return await ctx.send("This member is not in a voice channel")
        if member.voice.deaf:
            return await ctx.send("This member is already deafened")
        try:
            await member.edit(deafen=True)
        except discord.Forbidden:
            return await ctx.send("I don't have permission to deafen this member")
        await ctx.send(f"{member.mention} has been deafened")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def undeafen(self, ctx: commands.Context, *, member: discord.Member):
        """Undeafen a member in a voice channel"""
        if not member.voice:
            return await ctx.send("This member is not in a voice channel")
        if not member.voice.deaf:
            return await ctx.send("This member is not deafened")
        try:
            await member.edit(deafen=False)
        except discord.Forbidden:
            return await ctx.send("I do not have the permissions to undeafen this member")
        await ctx.send(f"{member.mention} has been undeafened")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def vckick(self, ctx: commands.Context, *, member: discord.Member):
        """Kick a member from a voice channel"""
        if not member.voice:
            return await ctx.send("This member is not in a voice channel")
        try:
            await member.edit(voice_channel=None)
        except discord.Forbidden:
            return await ctx.send("I don't have permission to kick this member from the voice channel")
        await ctx.send(f"{member.mention} has been kicked from the voice channel")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def vclock(self, ctx: commands.Context):
        """Lock a voice channel"""
        if not ctx.author.voice:
            return await ctx.send("You are not in a voice channel")
        try:
            await ctx.author.voice.channel.edit(reason=f"{ctx.author} used vclock", user_limit=1)
        except discord.Forbidden:
            return await ctx.send("I don't have permission to lock this voice channel")
        await ctx.send("This voice channel has been locked")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def vcunlock(self, ctx: commands.Context):
        """Lock a voice channel"""
        if not ctx.author.voice:
            return await ctx.send("You are not in a voice channel")
        try:
            await ctx.author.voice.channel.edit(reason=f"{ctx.author} used vcunlock", user_limit=0)
        except discord.Forbidden:
            return await ctx.send("I don't have permission to lock this voice channel")
        await ctx.send("This voice channel has been unlocked")