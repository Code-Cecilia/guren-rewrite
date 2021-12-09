import discord
from discord.ext import commands
import json
import requests
import asyncpraw
import random
import datetime

reddit = asyncpraw.Reddit(client_id="Your client id here",
                     client_secret="Your client secret here",
                     redirect_uri="http://localhost:8080", # This is usually what is default.
                     user_agent="Your user agent here",
                     username="Your user name here")


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----------------------")
    
    @commands.command(
        name="meme",
        description="Posts a meme from the subreddit r/memes"
    )
    async def meme(self, ctx):
        """Sends a random meme"""

        memes_submissions = await reddit.subreddit('memes')
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        embed = discord.Embed(timestamp=datetime.datetime.utcnow())
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=f"{submission.url}")

        await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        response = requests.get('https://aws.random.cat/meow')
        data = response.json()

        embed = discord.Embed(title = 'Here\'s a meow for you!~')
        embed.set_image(url=data['file'])            

        await ctx.send(embed=embed)            

def setup(bot):
    bot.add_cog(Images(bot))