from discord.ext import commands
from discord.ext import tasks
import logging, logging.config, logging.handlers

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('main')


class LoopFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_stats.start()

    @tasks.loop(minutes=30)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count."""
        try:
            await self.bot.topggpy.post_guild_count()
            logger.info(f"Posted server count ({self.bot.topggpy.guild_count})")
        except Exception as e:
            logger.info(f"Failed to post server count\n{e.__class__.__name__}: {e}")


def setup(bot):
    bot.add_cog(LoopFunctions(bot))
