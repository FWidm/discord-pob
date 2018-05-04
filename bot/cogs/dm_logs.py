import asyncio

from discord.ext import commands

import config
from util import chat_logging
from util.logging import log


def setup(bot):
    bot.add_cog(DmLogging(bot))


class DmLogging():
    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.export_dm_logs())

    @commands.command()
    async def export_logs(self):
        await self.export_dm_logs()

    async def export_dm_logs(self):
        while not self.bot.is_closed:
            log.info("Exporting all DMs. channels: {}".format(len(self.bot.private_channels)))

            for ch in self.bot.private_channels:
                recipient = ch.recipients[0]
                if recipient:
                    latest_date = chat_logging.get_latest_date_utc(recipient)
                    msgs = []
                    async for msg in self.bot.logs_from(ch, after=latest_date):
                        if not msg.author.bot:
                            msgs.append(msg)

                    # print("Msgs={}".format(msgs))
                    chat_logging.write_to_file(recipient, msgs)

            await asyncio.sleep(config.dm_poll_rate_seconds)  # task runs every x seconds

    async def trigger_export_logs(self):
        await self.bot.wait_until_login()
        await self.export_dm_logs()
