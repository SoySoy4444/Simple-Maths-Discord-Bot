# Created 21/05/20
# https://realpython.com/how-to-make-a-discord-bot-python/
# You can't do simple maths under pressure Discord Bot

import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()