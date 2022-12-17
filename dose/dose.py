import asyncio
import random
import time
import datetime
from typing import Literal
import discord

# Red
from redbot.core import Config, bank, commands, checks
from redbot.core.utils import AsyncIter


author = "Jay_"
version = "0.0.2"


class Dose(commands.Cog):

    def __init__(self, bot):
        self.bot = bot #'drug': risk of death (0-10)
        self.drugs = {}
        self.user_status_list = []
        self.user_died = []
        self.message_ind = 0
        self.drugs = {'fent':{'class':'depressant','death':-10},
                      'meth':{'class':'stim','death':4},
                      'ketamine':{'class':'disso','death':-8},
                      'heroin':{'class':'depressant', 'death':-7}
                      ,'liquor':{'class': 'depressant', 'death':-8},
                      'xanax':{'class':'depressant', 'death':-7},
                      'adderall':{'class':'stim','death':2},
                      'coke':{'class':'stim', 'death':7}}
        self.depressant_list = [' gets quite groggy and stumbles around like a drunk asshole',
                           ' falls over and passes out',
                           ' passes out on the steps of a church',
                           ' Forgot their wallet at the club on a tuesday' ]
        self.stim_list = ['\'s heart explods, boom',
                     ' has vibrated out of existence',
                     ' forgot to drink water']
        self.disso_list = [' does some weird shit',
                       ' met Ketamine Chick']


    def drug_effects(self, drug):
        if self.drugs[drug]['class'] == 'depressant':
            temp = self.message_ind
            self.message_ind += 1
            t = temp % len(self.depressant_list)
            return self.depressant_list[t]
        if self.drugs[drug]['class'] == 'stim':
            temp = self.message_ind
            self.message_ind += 1
            t = temp % len(self.stim_list)
            return self.stim_list[t]
        if self.drugs[drug]['class'] == 'disso':
            temp = self.message_ind
            self.message_ind += 1
            t = temp % len(self.disso_list)
            return self.disso_list[t]
 
  
    def status_multiplier(self, user, status):
        lis = []
        for s in self.user_status_list:
            if user.id == s[0]:
                lis.append(s)
        print(lis)
        return lis
    
    def total_score(self, user):
        total = 0
        for i in self.user_status_list:
            if i[0]== user.id:
                
                s = self.drugs[i[1]]['death']
                total += self.drugs[i[1]]['death']
        return total

    def remove_drugs(self, user):
        for s in self.user_status_list:
            if s[0] == user.id:
                self.user_status_list.remove(s)
    

    @commands.command()
    @checks.is_owner()
    async def debug(self, ctx, user: discord.Member):
        print(self.user_status_list)  


    @commands.command(alias="xanax")
    async def xan(self,ctx,user:discord.Member):
     
        in_list = False
        for m in self.user_status_list:
            
            if m[0] == user.id:
                n = self.status_multiplier(user, 'depressant')
                s = self.total_score(user)
                if s < 0:
                    s *= s
                    s = abs(s)
                elif s > 0:
                    s -= 8
                    s = abs(s)
                death = random.randrange(0,s)
                if death > 30:
                    
                    await ctx.send(f'{ctx.author.mention} tried, but {user.name} didn\'t make it. RIP.')
                    self.remove_drugs(user)
                    return False
                else:
                    in_list=True
                    self.remove_drugs(user)
                    await ctx.send(f'{ctx.author.mention} has saved {user.name} with a death score of {death}!')
                    return True
        if not in_list:
            await ctx.send(f'{user.mention}, apparently you need to chill the fuck out. Here\'s a xanax.')
            return False



    