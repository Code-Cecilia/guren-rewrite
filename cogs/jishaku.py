# This is the jishaku cog.

from discord.ext import commands

from jishaku.features.python import PythonFeature
from jishaku.features.root_command import RootCommand

class Jishaku(PythonFeature, RootCommand):
    pass

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----------------------")

def setup(bot: commands.Bot):
    bot.add_cog(Jishaku(bot=bot))