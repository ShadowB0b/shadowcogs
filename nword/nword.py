import asyncio
import logging
import time
from datetime import *
from pathlib import Path
from typing import Tuple

import discord as discord

# Red
from redbot.core import Config, bank, checks, commands
from redbot.core.utils import AsyncIter

author = "Jay_"
version = "0.0.1"


class Nword(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.mute_dict = {}
        self.timedown_lis = [] #'drug': risk of death (0-10)
        self.lastpic = 0
        self.ban_list = []
        self.n_list = {'0':[('f','h')]}
        path = Path(__file__).parent.absolute()
        self.pic_list = [f'{str(path)}\\shame\\nword.png',
                           f'{str(path)}\\shame\\nworddd.png',
                           f'{str(path)}\\shame\\unknown.png',
                           f'{str(path)}\\shame\\rosa.png']
        
    def check_list(self, message):
        user = message.author.id
        if user in self.n_list.keys():
            
            temp = self.n_list[user]
            temp
            print(f'temp - {temp}\n n_list - {self.n_list}')
            self.n_list.update({user: temp})
            return self.n_list[user]
        return 0

    def nnum(self, user):
        num = 0
        for i in self.timedown_lis:

            if i[0] == user.id:
                num += 1
        return num
    
    async def mute_racist(self, ctx, message, seconds = 300):
        nextcord = ctx#ediscor
        reason = '3 strikes your out for a bit'
        desctime = datetime.now().time()
        member_roles = message.author.roles
        print('lol ' + str(message.author.guild_permissions))
        mutedRole = nextcord.utils.get(guild.roles, name="Muted Racist")
        time_convert = {"s":1, "m":60, "h":3600, "d":86400, "w":604800, "mo":31536000}
        tempmute = seconds #e
        if not mutedRole:
            embed = nextcord.Embed(title="Setup Muted Role", description="No Muted role was found, please create one!")
            embed.set_footer(text="Due to issues I can't create one myself...")
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(title="Muted", description=f"{member.mention} was muted for {desctime} for message:\n{message.content}")
            embed.set_image(url="https://c.tenor.com/l1yJ91orR_kAAAAd/yt-battles-youre-muted.gif")
            embed.add_field(name="Reason", value=reason, inline=False)
            await ctx.send(embed=embed)
            embed = nextcord.Embed(title="Muted", description=f"You were muted in {ctx.guild.name} for {desctime}")
            embed.add_field(name="Reason", value=reason)
            embed.set_image(url="https://c.tenor.com/l1yJ91orR_kAAAAd/yt-battles-youre-muted.gif")
            await member.send(embed=embed)
            await member.add_roles(mutedRole, reason=reason)
            await asyncio.sleep(seconds)
            embed = nextcord.Embed(title="Unmuted", description=f"You were unmuted in {ctx.guild.name}")
            await member.send(embed=embed)
            embed = nextcord.Embed(title="Unmuted", description=f"Unmuted {member.mention}")
            await ctx.send(embed=embed)
            
            await member.remove_roles(mutedRole)

    @commands.command(alias='d')
    async def dbg(self, message):
        print(f'{self.check_list(message)}\n{self.n_list}\n{self.timedown_lis}')
        await message.channel.send(f'{str(self.nnum())}\n{self.n_list}\n{self.timedown_lis}' )
               
        
           
    @commands.command()
    @checks.is_owner()
    async def wipenword(self, ctx):
        self.n_list = {}
        self.timedown_lis = []

    def remove_user(self, user_id, seconds):
        for f in self.timedown_lis:
            if user_id == f[0]:
                timedel = datetime.now().timetuple()[-1] - seconds
                print(f' ,,,,,,,,,,,,, timedel {timedel}')
                if timedel >= seconds:
                    self.timedown_lis.remove(f)
                    print(f'remove_user removed {str(f)}')
    
    def index_list(self, value):
        dic = {}

        for s in self.timedown_lis:
            if s[0] not in dic.keys():
                dic.update({s[0]: []}) 

    def is_banned(self, user_id):
        return user_id in self.ban_list

    async def add_strike(self, message):
        id = message.author.id
        if id in self.n_list.keys():
            temp = self.n_list[id]
            temp.append((id, datetime.now(), message.author))
            self.n_list[id] = temp
        else:
            self.n_list[id] = (id, datetime.now(), message.author)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == True:
            return
        wordlist = ['nigga', 'nigger']
        for ind in range(len(wordlist)):
            if wordlist[ind] in message.content:
                await self.add_strike(message)
                await message.channel.send(f'{message.author.mention} might be racist, he said the nword {str(self.check_list(message))} times'
                )



        
        
        
        