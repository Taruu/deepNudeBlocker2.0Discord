from discord.ext.commands import *
import discord
import glob
import logging.config, logging

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('main')


class ModulesLoader:
    def __init__(self, bot):
        self.bot = bot

    def load_ext(self, moduleName):
        try:
            self.bot.load_extension(moduleName)
        except ExtensionNotFound as e:
            logger.error(f"Module {moduleName} ExtensionNotFound, \n {e}")
        except NoEntryPointError as e:
            logger.error(f"Module {moduleName} NoEntryPointError, \n {e}")
        except ExtensionFailed as e:
            logger.error(f"Module {moduleName} ExtensionFailed, \n {e}")
        except ExtensionAlreadyLoaded as e:
            logger.error(f"Module {moduleName} ExtensionAlreadyLoaded, \n {e}")
        else:
            logger.info(f"Load Module {moduleName}")

    async def load_all_modules(self):
        logger.info("Load all modules")
        list_all_modules = list(map(
            lambda item: item.replace('/', '.')[:-3],
            glob.glob("modules/*.py")))
        for moduleName in list_all_modules:
            self.load_ext(moduleName)


async def load_modules(bot):
    modulesLoader = ModulesLoader(bot)
    return await modulesLoader.load_all_modules()
