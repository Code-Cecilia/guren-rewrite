from discord.ext import commands
import sys

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----------------------")

    @commands.is_owner()
    @commands.command()
    async def reboot(self, ctx):
        await ctx.send("Rebooting!")
        await sys.exit() # fix exception or fix retarded self.bot.logput

def setup(bot):
    bot.add_cog(Owner(bot))