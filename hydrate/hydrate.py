
from typing import Literal
import datetime
import discord
import asyncio
# Red
from redbot.core import Config, bank, commands, checks
from redbot.core.utils import AsyncIter


author = "Jay_"
version = "0.0.3"


class Fire(commands.Cog):

    def __init__(self, bot):
        self.bot = bot #'drug': risk of death (0-10)
        self.role = 1046329985473986620
        self.channel = 1030564322352562257
        self.last_timestamp = datetime.datetime.now()

        

    @commands.command()
    @checks.is_owner()
    async def hydrate(self, ctx: commands.Context):
       ctx.send(f'@everyone drink some water you crusty hoes.\nReminder brought to you by {ctx.author.mention}')

    def run(self):
        s = discord.get_guil
    