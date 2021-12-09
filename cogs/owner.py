import discord
from discord.ext import commands
import sys
import asyncio
import os
import psutil
import speedtest

from discord.shard import ShardInfo

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----------------------")

    # Credits to CorpNewt for finding a fix for asyncio being broken on python 3.9 and for this block of code.

    @commands.is_owner()
    @commands.command()
    async def reboot(self, ctx):
        await ctx.send("Rebooting!")
        try:
            task_list = asyncio.Task.all_tasks()
        except AttributeError:
            try: task_list = asyncio.all_tasks()
            except: task_list = [] 

        for task in task_list:
            try:
                task.cancel()
            except:
                continue
        try:
            await self.bot.close()
            self.bot.loop.stop()
            self.bot.loop.close()
        except:
            pass
        os._exit(3)

    @commands.is_owner()
    @commands.command()
    async def hostinfo(self, ctx):
        embed = discord.Embed(title='System Resource Usage', description='See CPU and memory usage of the system.')
        embed.add_field(name='CPU Usage', value=f'{psutil.cpu_percent()}%', inline=False) # Fetches the CPU usage
        embed.add_field(name='Memory Usage', value=f'{psutil.virtual_memory().percent}%', inline=False) # Fetches the memory usage specifing the percent of it.
        embed.add_field(name='Available Memory', value=f'{round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total),2} %', inline=False) # Calculates the available memory rounding it by 2
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def speedtest(self, ctx):
        st = speedtest.Speedtest()
        st.get_best_server()
        try:
            upload = round(st.upload() / 1000000, 2) # Gets the upload speed, divides it by 100 and rounds it by 2
        except Exception as e:
            pass
            upload = e
        
        try:
            download = round(st.download() / 1000000, 2) # Gets the download speed and rounds it by 2
        except Exception as e:
            pass
            download = e

        embed = discord.Embed(title="Network Stats")
        embed.add_field(name="Download Speed", value=f"{download} mbps.", inline=False)
        embed.add_field(name="Upload Speed", value=f"{upload} mbps.", inline=False)
        
        await ctx.send(embed=embed)

#    @commands.command()
#    @commands.is_owner()
#    async def unload(self, ctx, cog: str):
#        async with ctx.typing():
#            embed = discord.Embed(color=0x808080)
#        for ext in os.listdir("./cogs/"):
#            if ext.endswith(".py") and not ext.startswith("_"):
#                try:
#                    self.bot.unload_extension(f"cogs.{ext[:-3]}")
#                    embed.add_field(name=f"Unloaded: `{ext}`", value='\uFEFF')
#                except Exception as e:
#                    embed.add_field(name=f"Failed to unload: `{ext}`", value=e)
#                await asyncio.sleep(0.5)
#            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog: str):
        async with ctx.typing():
            try:
                self.bot.unload_extension(cog)
            except Exception as e:
                await ctx.send(f"Could not unload {cog}.")
                return
            await asyncio.sleep(0.5)
            await ctx.send(f"{cog} unloaded.")

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog: str):
        async with ctx.typing():
            try:
                self.bot.load_extension(cog)
            except Exception as e:
                await ctx.send(f"Could not load {cog}.")
                return
            await asyncio.sleep(0.5)
            await ctx.send(f"{cog} loaded.")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        async with ctx.typing():
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except Exception as e:
                await ctx.send(f"Could not reload {cog}.")
                return
            await asyncio.sleep(0.5)
            await ctx.send(f"{cog} reloaded.")

def setup(bot):
    bot.add_cog(Owner(bot))