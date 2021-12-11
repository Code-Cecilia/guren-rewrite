import json
import random

import discord
import requests
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----------------------")

    @commands.command(
        name="ping",
        description="Shows the latency of the bot to the API")
    async def ping(self, ctx):
        await ctx.send(f"Pong!: `{round(self.bot.latency * 1000, 2)}`ms.") # Retrives the ping of the bot and multiplies it by 2 rounding by 2. 

    @commands.command(
        name="joke",
        aliases=['momjoke', 'mj'],
        description="Retrieves a Yo mama! joke from an API.")
    async def joke(self, ctx):
        response = requests.get('https://api.yomomma.info/')
        data = json.loads(response.text)
        embed = discord.Embed(title=data['joke'], color=discord.Colour.random())
        await ctx.send(embed=embed)

    @commands.command(
        name="fact",
        aliases=['rf', 'uf', 'uselessfact'],
        description="Useless facts."
    )
    async def fact(self, ctx):
        response = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
        data = json.loads(response.text)
        embed = discord.Embed(title=data['text'], color=discord.Colour.random())
        await ctx.send(embed=embed)        

    @commands.command(
        name='nocontext',
        aliases=['nc'],
        description="Retrieves a no context reddit submission from the subreddit nocontext."
    )
    async def NoContext(self, ctx):
        choice = self.bot.reddit.get_random_title("nocontext")
        embed = discord.Embed(title=choice, color=discord.Colour.random())
        await ctx.send(embed=embed)

    @commands.command(
        name="invite",
        aliases=['botinvite', 'i'],
        description="Sends an invite link for the bot."
    )
    async def invite(self, ctx):
        # await ctx.send(f"Invite me to your server using this link: https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8")
        embed = discord.Embed(color=discord.Colour.random())
        embed.add_field(name=f"", value=f"**Invite me to your server using this [link](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8)**")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))
