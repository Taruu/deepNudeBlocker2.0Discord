# TODO rewrite to own code or another library
from discord.ext import commands
import discord
import logging
import settings
import topgg
import functions.loader as loader

logger = logging.getLogger('main')
bot = commands.Bot(command_prefix='/')
bot.topggpy = topgg.DBLClient(bot, settings.topgg_token)


@bot.event
async def on_ready():
    try:
        # print bot information
        logger.info(bot.user.name)
        logger.info(bot.user.id)
        logger.info('Discord.py Version: {}'.format(discord.__version__))
        logger.info("Ready when you are xd")
        logger.info("I am running on " + bot.user.name)
        logger.info("With the ID: " + str(bot.user.id))
        await loader.load_modules(bot)
        await bot.topggpy.post_guild_count()
    except Exception as e:
        logger.error(e)


bot.run(settings.bot_token)
