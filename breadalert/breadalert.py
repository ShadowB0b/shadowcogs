# Developed by Redjumpman for Redbot.
# Inspired by the snail race mini game.

# Standard Library
import asyncio
import random
from typing import Literal

# Red
from redbot.core import Config, bank, commands, checks
from redbot.core.utils import AsyncIter
from redbot.core.errors import BalanceTooHigh

# Discord
import discord


__author__ = "jay_"
__version__ = "0.0.1"



class BreadAlert(commands.Cog):
    """Tells jay when bread joins vc"""

    def __init__(self, bot):
        self.bot = bot
        self.bread = "363681440669630465"


    def get_last_bot_message(self, ctx):

        for a in range(len(ctx.channel.messages), 0):
            if ctx.channel.messages[a].author.id == self.bot.id:
                print(ctx.channel.messages[a])
                return ctx.channel.messages[a]



    @commands.command()
    async def breadalert(self,ctx):
        print(ctx.guild.member(self.bread))