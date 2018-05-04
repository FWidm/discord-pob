import sys

import os

import config
from bot.discord_bot import bot
from util.logging import log

if __name__ == '__main__':
    token = config.token  # create config.py file and enter a new string!
    if token:
        # Add all extensions here before loading the bot.
        startup_extensions = ["bot.cogs.database",
                              "bot.cogs.dm_logs"]

        log.info("Starting pob discord bot...")
        for extension in startup_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                log.error('Failed to load extension {}\n{}'.format(extension, exc))

        bot.run(token)
