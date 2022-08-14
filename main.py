import os
import logging

from discord.ext import commands

from src import handlers

BOT = commands.Bot(command_prefix='$')
log = logging.getLogger(__name__)


def setup_command():
    BOT.add_command(handlers.ping)
    BOT.add_command(handlers.rate)

    for command in BOT.commands:
        log.info(f"command --> {command}")


def main():
    token = os.environ['TOKEN']

    log.info("setuping handlers...")
    setup_command()

    log.info("running bot...")
    BOT.run(token)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
