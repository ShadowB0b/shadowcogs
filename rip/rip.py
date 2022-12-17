import asyncio

from datetime import datetime, timedelta
from functools import partial

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import discord
from redbot.core import Config, checks, commands
from redbot.core.bot import Red
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils import AsyncIter, deduplicate_iterables, mod
from redbot.core.utils.chat_formatting import humanize_list, pagify, quote
from redbot.core.utils.common_filters import filter_invites
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
from redbot.core.utils.predicates import MessagePredicate

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService



class Rift(commands.Cog):



    def __init__(self, bot: Red):
        
        self.bot = bot
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        

