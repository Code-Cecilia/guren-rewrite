import discord
from discord.ext import commands
import json
import os

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

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        owner = guild.owner
        try:
            await owner.send(f"Thanks for having me in: {guild.name}.\n"
                             f"Your server's config files will be deleted, along with the mute files, and custom prefix.")
        except:
            print(f'couldn\'t send message to owner of {guild.owner}')
        if os.path.exists(f'bot_files/guilds/guild{guild.id}.json'):
            os.remove(f'./bot_config/guilds/guild{guild.id}.json')

        if os.path.exists(f'./bot_files/servers/mutes/guild{guild.id}.json'):
            os.remove(f'./bot_files/servers/mutes/guild{guild.id}.json')

        with open('bot_files/servers/prefixes/prefixes.json', 'r') as prefixFile:
            data = json.load(prefixFile)
        if str(guild.id) in data.keys():
            data.pop(str(guild.id))

        with open('prefixes.json', 'w') as prefixFile:
            json.dump(data, prefixFile)


def setup(bot):
    bot.add_cog(eventHandler(bot))