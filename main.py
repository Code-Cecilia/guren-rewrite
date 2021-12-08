import asyncio # Used for loop tasks
import json # Used for json databases and data storing
import os # Reads majority of files

import discord # Using Pycord
from discord.ext import commands

####### Used Flags ########
intents = discord.Intents
intents.messages = True
intents.bans = True
intents.guilds = True
intents.reactions = True
intents.guild_messages = True
intents.typing = True
intents.members = True
intents.voice_states = True
############################

with open("./bot_files/settings/settings.json", 'r') as configFile: # Points to the settings.json file and calls it configFile in the code.
    data = json.load(configFile)
    token = data.get("token") # Token Data
