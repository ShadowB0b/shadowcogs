import asyncio
import random
import time
from typing import Literal
import discord

# Red
from redbot.core import Config, bank, commands, checks
from redbot.core.utils import AsyncIter


author = "Jay_"
version = "0.0.2"


class PF(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 
        self.baseURL = 'https://cdn.discordapp.com/'

    @commands.command()
    async def pf(self, ctx: commands.Context, User: discord.User):
        print(User)
        usr = self.bot.get_user(User)
        embed = discord.Embed(description="PFP")
        embed.set_author(name=f"{usr}", icon_url=usr.avatar_url)
        embed.set_image(url=usr.avatar_url)
        await ctx.send(embed=embed)
