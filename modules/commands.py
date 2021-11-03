import asyncio

import discord
from discord.ext import commands
import datetime
import settings
import logging, logging.config, logging.handlers
import io
import re

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('main')

link_regex = re.compile(
    '((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)


class ChannelWatcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx):
        embed = discord.Embed()
        embed.add_field(name="How do I use this bot?",
                        value="""
                        This is very simple. Give the bot permission to delete messages.
                        After that, the bot will begin to delete all images that it can recognize.
                        If you want to exclude some channels, just block the bot to read these channels.
                        """,
                        inline=False)
        embed.add_field(name="My Discord server for contact",
                        value=f"[https://discord.gg/{settings.link_code}](https://discord.gg/{settings.link_code})")
        embed.set_footer(text="Bot by Taruu#0821",
                         icon_url="http://taruu.ru/avatar.png")
        await ctx.reply(embed=embed)


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(ChannelWatcher(bot))
    pass
