import json

import discord
import requests
from discord.ext import commands

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
        result_dict = self.bot.reddit.get_post_data("memes")
        embed = discord.Embed(title=result_dict["title"], color=discord.Colour.random())
        embed.set_footer(
            text=f"Author: u/{result_dict['author']} | {int(result_dict['like_ratio']*100)}% Upvoted")
        embed.set_image(url=result_dict['url'])
        await ctx.send(embed=embed)

    @commands.command(
        name="cat",
        description="Retrieves a random cat image from the API."
    )
    async def cat(self, ctx):
        response = requests.get('https://aws.random.cat/meow') # Cats API
        data = response.json()

        embed = discord.Embed(title = 'Here\'s a meow for you!~')
        embed.set_image(url=data['file'])            

        await ctx.send(embed=embed)    

    @commands.command(
        name="dog",
        description="Retrieves a random dog image from the API."
    )
    async def dog(self, ctx):
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        data = response.json()
        embed = discord.Embed(title='Here\'s a dog for you!')
        embed.set_image(url=data["message"]) 

        await ctx.send(embed=embed)     

    @commands.command()
    async def fox(self, ctx):
        """ ela fica aqui """
        response = requests.get('https://randomfox.ca/floof/')
        data = json.loads(response.text)
        embed = discord.Embed(title="Here's a fox for you!~", color=discord.Colour.random())# , description=f"{data['image']}")
        embed.set_image(url=f"{data['image']}")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Images(bot))
