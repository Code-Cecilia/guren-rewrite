import discord
from discord.ext import commands
import json
import requests
import asyncpraw
import random
import datetime

with open("./bot_files/settings/settings.json", "r") as redditConfig:
    data = json.load(redditConfig)
    client_id = data.get("r_client_id")
    client_secret = data.get("r_client_secret")
    redirect_uri = data.get("r_redirect_uri")
    user_agent = data.get("r_user_agent")
    username = data.get("r_username")

reddit = asyncpraw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     redirect_uri=redirect_uri, # This is usually default.
                     user_agent=user_agent,
                     username=username)


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

        memes_submissions = await reddit.subreddit('memes') # Searches the memes subreddit, you can use whatever subreddit you want here
        post_to_pick = random.randint(1, 50) # Picks one from 50
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        embed = discord.Embed(timestamp=datetime.datetime.utcnow())
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=f"{submission.url}")

        await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        response = requests.get('https://aws.random.cat/meow') # Cats API
        data = response.json()

        embed = discord.Embed(title = 'Here\'s a meow for you!~')
        embed.set_image(url=data['file'])            

        await ctx.send(embed=embed)    

    @commands.command()
    async def dog(self, ctx):
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        data = response.json()
        embed = discord.Embed(title='Here\'s a dog for you!')
        embed.set_image(url=data["message"]) 

        await ctx.send(embed=embed)     

def setup(bot):
    bot.add_cog(Images(bot))