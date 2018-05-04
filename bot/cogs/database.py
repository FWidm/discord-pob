from discord.ext import commands

import config
from bot.discord_bot import bot
from bot.db import repository


def setup(bot):
    bot.add_cog(Database(bot))


class Database():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def overview(self, ctx, *classes):
        # todo: add user role check

        if config.allow_pming and ctx.message.channel.is_private:
            str = repository.get_overview(list(classes))
            await self.bot.send_message(ctx.message.author, str)

    @commands.command(pass_context=True)
    async def find(self, ctx, *conditions):
        if 'help' in conditions:
            await bot.send_message(ctx.message.author,
                                   "Specify conditions such as `id=1`, `ascendency=Jugg`, `main_skill=Glacial` and more.\nAvailable attributes include: {}".format(
                                       None))
            return
        query_params = {}
        last_key = ""
        for entry in conditions:
            try:
                key, val = entry.split("=")[0:2]
                last_key = key
                query_params[key] = val
            except ValueError:
                if last_key != "":
                    query_params[last_key] += " " + entry

        print(conditions, query_params, len(query_params))
        result = ""
        limit = query_params.get('limit') or 5
        offset = query_params.get('offset') or 0

        print(query_params.get('limit'), limit)
        if len(conditions) < 1:
            result += "You can specify various conditions, `!find help` will display all options.\n" \
                      "Showing a selection of up to {} builds.\n".format(limit)
        try:
            result_set, query_info = repository.find(query_params, limit=int(limit), offset=int(offset))

            for entity in result_set:
                output_class = entity.ascendency if entity.ascendency != "None" else entity.character
                result += "ID: {} - {} - lvl {} {}".format(entity.id,
                                                           entity.main_skill,
                                                           entity.level,
                                                           output_class)
                result += "  -  Pastebin: <https://pastebin.com/{}>".format(
                    entity.paste_key) if entity.paste_key != 'unkown' else ""
                result += "\n"
            result += "\n-- **Info** --\n" + query_info if query_info else ""
            await bot.send_message(ctx.message.author, result if result != "" else "No Match found.")
        except ValueError:
            await bot.send_message(ctx.message.author, "**Error** : `limit` and `offset` need to be integers.")
