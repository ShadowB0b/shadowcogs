import random
import asyncio
import discord
from redbot.core import commands, bank, checks
from redbot.core.config import Config
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.predicates import MessagePredicate
import datetime

author = "Jay_"
version = "1.0.0"

class Awo(commands.Cog):
    '''Custom Wolf Pack cog made by Jay_ for Blackout.
        Wolfpack or die
        '''
    

    def __init__(self, bot):
        self.bot = bot
        self.pic = 'https://cdn.pixabay.com/photo/2022/04/01/15/41/wolf-7105065_960_720.jpg'
        self.image = ""
        self.pic_path ='C:\\Users\\justm\\redenv\\Lib\\site-packages\\redbot\\cogs\\awo\\wolf.jpg'
        self.last_awo = None
        self.payout_list = {}
        self.second_half = '. Here\'s {str(num)} {await bank.get_currency_name(ctx.guild)}.'
        self.message_list = [f'You answered the awo, I seent it',f'Shake that bussy, awoooo, awooooo.']
        self.awo_index = 0

    

    @commands.command()
    @checks.is_owner()
    async def addmessage(self, ctx, message):
        self.message_list.append(message)
    #This command adds the
    @commands.command()
    async def wolfpack(self,ctx):
        is_wolf = False
        for i in ctx.author.roles:
            if i.id == 1048830223107506258:
                is_wolf = True
                await ctx.send(f'{ctx.author.mention} is already Wolf Packl. Awoooooooooo')
                return
        await ctx.send(f'{ctx.author.mention} So you want to be a Wolllfffffff?\n(say yes to accept)')
        pred = MessagePredicate.yes_or_no(ctx)        
        event = "message"
        try:
            await ctx.bot.wait_for(event, check=pred, timeout=30)
        except asyncio.TimeoutError:
            with contextlib.suppress(discord.NotFound):
                await query.delete()
            return
        if pred.result:
            mem = ctx.guild.get_member(ctx.author.id)                
            await mem.add_roles(ctx.guild.get_role(1048830223107506258), reason=f"Welcome to Wolf Pack. >awo")
            await ctx.send(f'{ctx.author.mention} welcome to Wolf Pack. >awo')

    async def closest_awo(self, ctx):
    
        if self.last_awo is None:

            return
        if ctx.author.id == self.last_awo[0].id:
            return
        cur_time = datetime.datetime.now()
        dif = cur_time - self.last_awo[1]
        if dif <= datetime.timedelta(seconds=30):  
            num = random.randrange(1000, 3500)
            if ctx.author.id not in self.payout_list.keys():
                await ctx.send(f'{self.message_list[self.awo_index % (len(self.message_list) - 1)]}. Here\'s {str(num)} {await bank.get_currency_name(ctx.guild)}.')
                await bank.deposit_credits(ctx.author, num)
                self.awo_index += 1
                self.payout_list[ctx.author.id] = datetime.datetime.now()
            if self.last_awo[0].id not in self.payout_list.keys():
                self.awo_index += 1    
                self.payout_list[self.last_awo[0].id] = datetime.datetime.now()
                await bank.deposit_credits(self.last_awo[0], num)
        else:
            self.last_awo = (ctx.author, datetime.datetime.now())
            return
                
        if ctx.author.id in self.payout_list.keys():
            t = datetime.datetime.now() - self.payout_list[ctx.author.id]
            if t >= datetime.timedelta(hours=1):

                await ctx.send(f'{self.message_list[self.awo_index % (len(self.message_list) - 1)]}. Here\'s {str(num)} {await bank.get_currency_name(ctx.guild)}.')
                await bank.deposit_credits(ctx.author, num )
                self.awo_index += 1    
                self.payout_list[ctx.author.id] = datetime.datetime.now()
            else:
                self.last_awo = (ctx.author, datetime.datetime.now())
                     
        if self.last_awo[0].id in self.payout_list.keys():

            t = datetime.datetime.now() - self.payout_list[self.last_awo[0].id]
            if t >= datetime.timedelta(hours=1):

                await ctx.send(f'{self.message_list[self.awo_index % (len(self.message_list) - 1)]}Here\'s {str(num)} {await bank.get_currency_name(ctx.guild)}.')
                self.awo_index += 1                
                await bank.deposit_credits(self.last_awo[0], num )
                self.payout_list[self.last_awo[0].id] = datetime.datetime.now()
            else:
                self.last_awo = (ctx.author, datetime.datetime.now())          
            
        self.last_awo = (ctx.author, datetime.datetime.now())
            
    
            
        
    @commands.command()
    @checks.is_owner()
    async def awolist(self, ctx):
        st = ""
        for i in self.payout_list.keys():
            st = st +'\n'+ str(self.bot.get_user(i)) + str(self.payout_list[i]) + '\n'
        if len(st) > 0:
            await ctx.send(st)
        else:
            await ctx.send('Nobody got paid yet.')
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def awo(self, ctx):
        for r in ctx.author.roles:
            if r.id == 1048830223107506258:
                await ctx.send(file=discord.File(self.pic_path, 'wolf.jpg'))
                await ctx.send(f'AWOOOOOOOOOoooooOOOOOOOOOOOOOO')
                if self.last_awo is None:
                    self.last_awo = (ctx.author, datetime.datetime.now())
                    return
                else:                    
                    await self.closest_awo(ctx)
                    return
            
        await ctx.send(f'You ain\'t pack. Type >wolfpack to join. :wolf:')
        
