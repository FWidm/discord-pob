import asyncio
import random
from urllib.error import HTTPError

import discord
import os
from discord.ext import commands
from discord.ext.commands import CommandInvokeError

import config
import util
from bot import pob_output
from bot import pob_parser

from util import pastebin
from util.discord_util import parse_nick_or_name
from util.logging import log
from bot.db import repository
import defusedxml.ElementTree as ET

bot = commands.Bot(command_prefix='!', description="x")
bot.remove_command('help')


def load_examples():
    pastebins = open(os.path.join('in', 'pastebins.txt')).readlines()
    for paste in pastebins:
        parse_pob("X", paste, False)


@bot.event
async def on_ready():
    log.info('Logged in: uname={}, id={}'.format(bot.user.name, bot.user.id))
    # load_examples()
    if config.presence_message:
        await bot.change_presence(game=discord.Game(name=config.presence_message))


@bot.command()
async def load(extension_name: str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))


@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def help(ctx):
    if ctx.message.channel.is_private:
        await bot.send_message(ctx.message.author,
                               "Paste your pastebin here for a quick overview or use `!pob <pastebin link>` for a detailed response. "
                               "Alternatively get an overview about parsed pastebins by using `!overview` or search for builds with `!find`.")


@bot.command(pass_context=True)
# @commands.cooldown(1, 5, commands.BucketType.user)
async def pob(ctx, *, key):
    if not config.allow_pming and ctx.message.channel.is_private:
        return
    embed = parse_pob(parse_nick_or_name(ctx.message.author), ctx.message.content)
    try:
        if embed:
            await bot.send_message(ctx.message.channel, embed=embed)
    except discord.Forbidden:
        log.info("Tried pasting in channel without access.")
        # await ctx.say(arg)


@bot.event
async def on_message(message):
    """
    Handle message events
    :param message:
    :return: None
    """
    # call bot commands, if not a bot command, check the message for pastebins
    # better way to do this would probably be to create the context, then check if its valid, then invoke it. If its valid,its a command, if not, its not. You could backport this to async pretty ez

    # todo: replace async with rewrite of the bot, then use on_command_completion
    if message.author.bot:
        return

    if (message.channel.name in config.active_channels or (message.channel.is_private and config.allow_pming)) \
            and not util.starts_with("!pob", message.content[:4]) \
            and "pastebin.com/" in message.content:
        # check if valid xml
        # send message
        log.debug("A| {}: {}".format(message.channel, message.content))
        embed = parse_pob(parse_nick_or_name(message.author), message.content, minify=True)
        if embed:
            await bot.send_message(message.channel, embed=embed)
    else:
        await bot.process_commands(message)


def parse_pob(author, content, minify=False):
    """
    Trigger the parsing of the pastebin link, pass it to the output creating object and send a message back
    :param channel: receiving channel
    :param author: user sending the message
    :param paste_key: pastebin paste key
    :param argument: optional: arguments to determine the output
    :return: Embed
    """
    paste_keys = pastebin.fetch_paste_key(content)
    if len(paste_keys) >= 1:
        xml = None
        paste_key = random.choice(paste_keys)
        log.info("Parsing pastebin with key={} from author={}, other keys={}".format(paste_key, author, paste_keys))

        try:
            xml = pastebin.get_as_xml(paste_key)
        except HTTPError as err:
            log.error("Invalid pastebin-url msg={}".format(err))
        if xml:
            build = pob_parser.parse_build(xml)
            # print(build)
            try:
                embed = pob_output.generate_response(parse_nick_or_name(author), build, minified=minify)
                log.debug("embed={}; thumbnail={}; length={}".format(embed, embed.thumbnail, embed.__sizeof__()))

                repository.add_statistics(author, build, paste_key, role=None, category="DEMO")
                return embed
            except Exception as e:
                log.error("Could not parse pastebin={} - Exception={}, Msg={}".format(paste_key, type(e).__name__, e))
                raise e
