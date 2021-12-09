from discord.ext import commands

class error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----------------------")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("You are not the owner of this bot to use this command! If you think this a mistake please try again.")

def setup(bot):
    bot.add_cog(error(bot))