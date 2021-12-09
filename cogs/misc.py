import discord
from discord.ext import commands
import json
import requests

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----------------------")

    @commands.command(
        name="ping")
    async def ping(self, ctx):
        await ctx.send(f"Pong!: `{round(self.bot.latency * 1000, 2)}`ms.") # Retrives the ping of the bot and multiplies it by 2 rounding by 2. 

    @commands.command(name="joke")
    async def joke(self, ctx):
        response = requests.get('https://api.yomomma.info/')
        data = json.loads(response.text)
        await ctx.send(data['joke'])

def setup(bot):
    bot.add_cog(Misc(bot))