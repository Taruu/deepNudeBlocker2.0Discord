from bestconfig import Config
config = Config()
bot_token = config.get('BOT_TOKEN')
server_url = config.get("HOST.IMAGE_CHECK_SERVER")
server_token = config.get("SERVER_TOKEN")
print(server_url)
