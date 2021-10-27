from discord.ext import commands
import datetime
import logging, logging.config, logging.handlers
import io
import re
from functions.embend_handler import check_attachments

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('main')

link_regex = re.compile(
    '((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)


class MessageHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        links = re.findall(link_regex, message.content)
        if message.attachments:
            await check_attachments(message)


def setup(bot):
    bot.add_cog(MessageHandler(bot))
