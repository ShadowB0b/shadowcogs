"""
MIT License

Copyright (c) 2020-present phenom4n4n

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# original invoke hook logic from https://github.com/mikeshardmind/SinbadCogs/tree/v3/noadmin

 # Made by Jay_ for all the homies at Blackout

import wget
import datetime
import time
import discord
from redbot.core import commands
from redbot.core.bot import Red
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from os.path import exists
import asyncio
import os
from PIL import Image


base_path="home\\cky37373\\lib\\site-packages\\redbot\\cogs\\"

class Homies(commands.Cog):
    """
    Lets make commands for all the homies
    """
   
    __version__ = "0.0.4"

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.today = datetime.datetime.today()
        self.URL = 'https://svs.gsfc.nasa.gov/Gallery/moonphase.html'
        self.driver = None
        self.phases = ['New Moon', 'Waxing Crescent', 'First Quarter', 'Waxing Gibbous', 'Full', 'Waning Gibbous', 'Last Quarter', 'Waning Crescent']
        self.used = 0
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        self.mol_ind = 0
        self.mol_num = ['1','2','3']
        self.mol_filepath = base_path + 'homies\\molly\\molly'
        self.thrt_filepath = base_path + 'homies\\throat\\throat'
        self.thrt_ind = 9
        self.thrt_num = ['1','2','3','4','5','6','7','8','9','10','11']


    def deftermine_phase(self,days=0.0):
        amount = days/27
        if amount >= .95 or amount < .05:
            return 'New Moon'
        if amount >=.05 and amount <.24:
            return 'Waxing Crescent'
        if amount >= .24 and amount < .26:
            return 'First Quarter'
        if amount >= .26 and amount < .45:
            return 'Waxing Gibbous'
        if amount >= .45 and amount < .55:
            return 'Full Moon'
        if amount >= .55 and amount < .74:
            return 'Waning Gibbous'
        if amount >= .74 and amount <.76:
            return 'Last Quarter'
        if amount >= .76 and amount < .95:
            return 'Waning Crescent'

    def wait_for_file(filepath, timeout=30):
        loops = 0
        result = True
        while not exists(filepath):
            asyncio.sleep(1)
            loops+= 1
            if loops>timeout:
                result = False
                break
        return result

    @commands.command()
    async def moony(self, ctx):
        await ctx.send('Standby...')
        f = base_path + 'homies\\moony\\moony.gif'
        with open(f, 'r+') as pic:
            await ctx.send(file=discord.File(f, f))

    @commands.command()
    async def moon(self, ctx):
        await ctx.send('Standby')
        self.driver = webdriver.Chrome('./chromedriver',options=self.options)
        driver = self.driver
        driver.get(self.URL)
        month,day =datetime.datetime.now().month, datetime.datetime.now().day
        if not exists(base_path + 'homies\\pics\\moon_' + str(month) + '_' + str(day) + '.jpg'):
            await ctx.send('You are the first to check the moon phase today, standby so I can download the image.')
            
            
            imgs = driver.find_element(By.XPATH, '//img[@id="moon_image"]')
            url = imgs.get_attribute('src')
            f = wget.download(url,out=base_path + 'homies\\pics\\moon_' + str(month) + '_' + str(day) + '.jpg')
            result = True
            if result:
                with open(f, 'r+') as pic:
                    await ctx.send(file=discord.File(f, f))
                    
                    phase = driver.find_element(By.XPATH, '//*[@id="moon_info_table"]/table/tbody/tr[2]/td[2]')
                    days = phase.text.split('(')[-1]
                    d = days.split('d')
                    hours = d[1].split('h')
                    mins = hours[1].split('m')
                    print(f'\n{d[0]}d {hours[0]}h {mins[0]}m')
                    days = float(d[0]) + float(hours[0])/60.0 + float(mins[0])/720.0
                    await ctx.send(self.deftermine_phase(days)+ "  " + phase.text)
                    self.used = 1
                print(url)
                
        else:
            print(f'You are the {str(self.used + 1)} person to use this today')
            f = base_path + 'homies\\pics\\moon_' + str(month) + '_' + str(day) + '.jpg'
            with open(f, 'r+') as pic:
                await ctx.send(file=discord.File(f, f))
                phase = driver.find_element(By.XPATH, '//*[@id="moon_info_table"]/table/tbody/tr[2]/td[2]')
                days = phase.text.split('(')[-1]
                d = days.split('d')
                hours = d[1].split('h')
                mins = hours[1].split('m')
                print(f'\n{d[0]}d {hours[0]}h {mins[0]}m')
                days = float(d[0]) + float(hours[0])/60.0 + float(mins[0])/720.0
                await ctx.send(self.deftermine_phase(days)+ "  " + phase.text)
                self.used += 1
        self.driver.close()

    @commands.command()
    async def moonlanding(self, ctx):
        self.driver = webdriver.Chrome('./chromedriver',options=self.options)
        driver = self.driver
        driver.get(self.URL)
        link = driver.find_element(By.XPATH, '//*[@id="map_link"]').get_attribute('href')

        month,day =datetime.datetime.now().month, datetime.datetime.now().day
        f = wget.download(link,out=base_path+'homies\\pics\\moon_' + str(month) + '_' + str(day) + 'landing.tif')
        
           
        outfile = base_path + 'homies\\pics\\moon_' + str(month) + '_' + str(day) + 'landing.jpg'
        try:
            im = Image.open(base_path + 'homies\\pics\\moon_' + str(month) + '_' + str(day) + 'landing.tif')
            im.save(outfile, "JPEG", quality=100)
            
        except Exception as e:
            print(type(e))
            print(e.args)
            await ctx.send('error converting file')
            driver.quit()
        else:
            with open(f, 'r+') as pic:
                await ctx.send(file=discord.File(f, f))
            driver.quit()
            
    @commands.command()
    async def homies(self, ctx):
        await ctx.send('>nova\n>throat\n>moon\n>moonlanding (download a high quality image of the moon with points of interest labeled)\n')

    @commands.command()
    async def nova(self, ctx):
        await ctx.send('I want head pats')
        await ctx.send(file=discord.File(self.mol_filepath+self.mol_num[self.mol_ind] + '.gif', self.mol_filepath+self.mol_num[self.mol_ind] + '.gif'))
        if self.mol_ind + 1 >= len(self.mol_num):
            self.mol_ind = 0
        else:
            self.mol_ind += 1

    @commands.command()
    async def throat(self, ctx):
        ext = '.gif'
        await ctx.send('LMAO get a load of this creature')
        if str(self.thrt_ind + 1) in ['8','9','10','11']:
            ext = '.jpg'
        await ctx.send(file=discord.File(self.thrt_filepath+self.thrt_num[self.thrt_ind] + ext, self.mol_filepath+self.thrt_num[self.thrt_ind] + ext))
        if self.thrt_ind + 1 >= len(self.thrt_num):
            self.thrt_ind = 0
        else:
            self.thrt_ind += 1

        