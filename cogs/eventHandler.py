import discord
from discord.ext import commands

class eventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----------------------")

    @commands.Cog.listener(name='on_command')
    async def print(self, ctx, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        server = guild.name
        user = ctx.author
        command = ctx.command
        print(f'{server} > {user} > {command}')

def setup(bot):
    bot.add_cog(eventHandler(bot))