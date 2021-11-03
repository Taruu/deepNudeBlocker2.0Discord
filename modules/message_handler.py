from discord.ext import commands
import datetime
import logging, logging.config, logging.handlers
import io

import asyncio
import discord
import settings
from functions.embend_handler import CheckContent

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('main')


class MessageHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = None
        self.check_content = CheckContent(self.send_log)
        asyncio.create_task(self.start())

    async def start(self):
        if not self.log_channel:
            logger.info("Init log channel")
            self.log_channel = await self.bot.fetch_channel(
                settings.log_chat_id)

    async def send_local_log(self, message, deleted):
        """Send local log for server admin"""
        embed = discord.Embed()
        embed.add_field(name=f"User {message.author.name}",
                        value=f"""{message.author.id}""",
                        inline=False)

        embed.add_field(name=f"Guild {message.guild.name}",
                        value=f"""{message.guild.name}""",
                        inline=False)

        embed.add_field(name=f"Channel",
                        value=f"""{message.channel.id}""",
                        inline=True)

        embed.add_field(name=f"Message",
                        value=f"""{message.id}""",
                        inline=False)

        embed.add_field(name=f"Deleted?",
                        value=f"""{deleted}""",
                        inline=True)
        embed.set_footer(text=f"Checked by {self.bot.user.name}",
                         icon_url=self.bot.user.avatar_url)

        server_log_chat = await message.guild.fetch_channels()
        for chat in filter(
                lambda channel: channel.name == settings.log_chat_word,
                server_log_chat):
            try:
                await chat.send(embed=embed)
                break
            except:
                pass

    async def send_log(self, message, deleted):
        """Send system log"""
        embed = discord.Embed()
        embed.add_field(name=f"User id",
                        value=f"""{message.author.id}""",
                        inline=False)

        embed.add_field(name=f"Guild id",
                        value=f"""{message.guild.id}""",
                        inline=False)

        embed.add_field(name=f"Channel id",
                        value=f"""{message.channel.id}""",
                        inline=True)
        embed.add_field(name=f"Message id",
                        value=f"""{message.id}""",
                        inline=False)

        embed.add_field(name=f"Deleted?",
                        value=f"""{deleted}""",
                        inline=True)
        embed.set_footer(text=f"Checked by {self.bot.user.name}",
                         icon_url=self.bot.user.avatar_url)

        await self.log_channel.send(embed=embed)
        asyncio.create_task(self.send_local_log(message, deleted))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.attachments:
            await self.check_content.check_attachments(message)
        await self.check_content.check_urls(message)


def setup(bot):
    bot.add_cog(MessageHandler(bot))
