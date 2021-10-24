#TODO rewrite to own code or another library
from discord.ext import commands
from embend_handler import check_attachments
import settings

# the prefix is not used in this example
print(commands)

bot = commands.Bot(command_prefix='/')


@bot.event
async def on_message(message):
    if message.attachments:
        checed_files = await check_attachments(message)
    print(f'Message from {message.author}: {message.content}')

bot.run(settings.bot_token)