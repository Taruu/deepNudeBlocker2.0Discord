#TODO rewrite to own code or another library
from discord.ext import commands
from embend_handler import  FileChek
import settings

# the prefix is not used in this example
print(commands)

bot = commands.Bot(command_prefix='/')
file_check = FileChek()

@bot.event
async def on_message(message):
    if message.attachments:
        await file_check.check_attachments(message.attachments)
    print(f'Message from {message.author}: {message.content}')

bot.run(settings.token)