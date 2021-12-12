import json  # Used for json databases and data storing
import os  # Reads majority of files

from pathlib import Path
import discord  # Using Pycord
from discord.ext import commands

from utils import Reddit

####### Used Flags ########
intents = discord.Intents()
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
    owner = data.get("owner") # Owner Data
    client_id = data.get("r_client_id")
    client_secret = data.get("r_client_secret")
    redirect_uri = data.get("r_redirect_uri")
    user_agent = data.get("r_user_agent")
    username = data.get("r_username")
    random_api_key = data.get("random_api_key")

with open("./bot_files/configs/status.json", 'r') as statusFile: # I decided to opt for the status data in the JSON for more ease of use. 
    data = json.load(statusFile)
    statuses = data.get("statuses")

# I call my bot instance as bot, which means i will have to use bot everytime i want to mention it or create a command, etc. Thats its name.
bot = commands.AutoShardedBot(
    command_prefix='$', # Temporary prefix
    owner_id=owner, # Grabs the owner id from the settings.json
    case_insensitive=True, # Allows upper case and lower case letters in commands, easier for mobile users with some keyboards.
    intents=intents # Needs the flags enabled in order to work properly. These were discord API changes and later i will have to request message intent.
)

bot.token = token
bot.version = "0.1"
bot.reddit = Reddit.reddit_login(
    r_client_id = client_id,
    r_client_secret = client_secret,
    r_redirect_uri = redirect_uri,
    r_user_agent = user_agent,
    r_username = username
)

bot.api = random_api_key

@bot.event # Login event.
async def on_ready():
    print("\n----------------------")
    print('Logged in as', bot.user.name) # Prints the username of the bot.
    print('Bot ID:', bot.user.id) # Prints the user ID of the bot.
    print('Bot latency:', round(bot.latency * 1000, 2)) # Shows the bot latency to the API in the console.
    print('Running discord.py version ' + discord.__version__) # Shows the current library version.
    print("\n----------------------")

async def presence():
    await bot.wait_until_ready()
    while not bot.is_closed():
        # if you wish to change the status to one in the config please uncomment the line below and change discord.Streaming to game.
        # game = discord.Game(statuses)
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name="i don\'t know", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

# Status that can be set:
#
# online
# offline
# idle
# dnd
# invisible
# do_not_disturb - alias for dnd
#

############### Command Handler ##################

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f'cogs.{filename[:-3]}')

###################################################

bot.loop.create_task(presence())
bot.run(bot.token) 

# Will only work if they are not inside the cogs loading loop - reminder`
