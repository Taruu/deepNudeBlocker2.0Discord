from bestconfig import Config

import re
import logging
import logging.config
import logging.handlers

logger_discord = logging.getLogger('discord')
logger_discord.setLevel(logging.INFO)
# handler = logging.FileHandler(filename=f'logs/discord/discord-{datetime.datetime.utcnow().strftime("%Y-%M-%d-%H-00")}.log', encoding='utf-8', mode='a')
handler = logging.handlers.TimedRotatingFileHandler('logs/discord/discord.log',
                                                    'H', 12, 15)
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

logger_discord.addHandler(handler)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('main')

config = Config()
bot_token = config.get('BOT_TOKEN')
server_url = config.get("HOST.IMAGE_CHECK_SERVER")
server_token = config.get("SERVER_TOKEN")
topgg_token = config.get("TOP_GG_TOKEN")

coefficient_unsafe = config.get("COEFFICIENT.UNSAFE")

link_code = config.get("DISCORD.LINK_CODE")
log_chat_id = config.get("DISCORD.LOG_CHAT")
log_chat_word = config.get("DISCORD.LOG_CHAT_LOCAL")

regex_str = """http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"""

link_regex = re.compile(regex_str, re.DOTALL)
