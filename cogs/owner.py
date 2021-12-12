import asyncio
import os
import sys

import discord
import psutil
import speedtest
from discord.ext import commands
from discord.shard import ShardInfo


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----------------------")

    # Credits to CorpNewt for finding a fix for asyncio being broken on python 3.9 and for this block of code.

    @commands.is_owner()
    @commands.command(
        name="reboot",
        aliases=['restart'],
        description="Reboots the bot instance. Useful for when running in a script that loops the task of running the main file."
    )
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
    @commands.command(
        name="hostinfo",
        aliases=['hi', 'sysinfo'],
        description="Shows the information of the system where i am currently hosted."
    )
    async def hostinfo(self, ctx):
        if sys.platform.startswith('linux'):
            platform1 = "Linux x64"
        elif sys.platform.startswith('win32'):
            platform1 = "Windows x64"
        embed = discord.Embed(title='System Information')
        embed.add_field(name='CPU Usage', value=f'{psutil.cpu_percent()}%', inline=False) # Fetches the CPU usage
        embed.add_field(name='Memory Usage', value=f'{psutil.virtual_memory().percent}%', inline=False) # Fetches the memory usage specifing the percent of it.
        embed.add_field(name='Available Memory', value=f'{round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total),2} %', inline=False) # Calculates the available memory rounding it by 2
        embed.add_field(name="Operating System in Use:", value=f'{platform1}', inline=False)
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command(
        name="speedtest",
        aliases=['st'],
        description="Runs a speed test to the best possible server."
    )
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

    @commands.is_owner()
    @commands.command(
        name="unload",
        description="Unloads a specific cog."
    )
    async def unload(self, ctx, cog: str):
        async with ctx.typing():
            try:
                self.bot.unload_extension(cog)
            except Exception as e:
                await ctx.send(f"Could not unload {cog}.")
                return
            await asyncio.sleep(0.5)
            await ctx.send(f"{cog} unloaded.")

    @commands.is_owner()
    @commands.command(
        name="load",
        description="Loads a specific cog. It must be unloaded to be loaded."
    )
    async def load(self, ctx, cog: str):
        async with ctx.typing():
            try:
                self.bot.load_extension(cog)
            except Exception as e:
                await ctx.send(f"Could not load {cog}.")
                return
            await asyncio.sleep(0.5)
            await ctx.send(f"{cog} loaded.")

    @commands.is_owner()
    @commands.command(
        name="reload",
        description="Reloads a specific cog."
    )
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
