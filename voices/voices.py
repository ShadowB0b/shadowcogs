"""
Copyright 2021 Onii-chan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging

import aiohttp
import discord
from redbot.core import commands




class Voices(commands.Cog):
    """Get images of animals!"""

    def __init__(self, bot):
        self.bot = bot

    __author__ = ["Jay_ and Geet"]
    __version__ = "0.0.1" 

@commands.Cog.listener() 
async def on_voice_state_update(self, member, before, after):
    conf = await self.config.all_guilds()
