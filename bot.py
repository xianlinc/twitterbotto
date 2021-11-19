#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from Capturing import Capturing

from Storage import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def test(update, context):
    """Send a message when the command /test is issued."""
    update.message.reply_markdown_v2('Bot is up')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_markdown_v2('Help!')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def check_stalked(update, context):

    update.message.reply_markdown_v2("Here are the new following for stalked accounts:")
    # get a list of handles of stalked accounts
    handle_list = get_account_list()

    # for each account, check for new following
    for handle in handle_list:
        with Capturing() as output:
            following_list = check_for_new_following(handle)
        if following_list == []:
            continue
        update.message.reply_markdown_v2("\n".join(output))


def stalk(update, context):
    with Capturing() as output:
        add_account("".join(context.args))
    update.message.reply_markdown_v2("\n".join(output))


def list(update, context):
    with Capturing() as output:
        get_account_list()
    update.message.reply_markdown_v2("\n".join(output))


def markdown(update, context):
    update.message.reply_markdown_v2("[inline URL](http://www.twitter.com/zhusu/)")

def check(update, context):
    with Capturing() as output:
        check_for_new_following("".join(context.args))
    update.message.reply_markdown_v2("\n".join(output))


def dao(update, context):
    with Capturing() as output:
        get_dao_list()
    update.message.reply_markdown_v2("\n".join(output))


def contains(update, context):
    with Capturing() as output:
        db_contains("".join(context.args))
    update.message.reply_markdown_v2("\n".join(output))


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(os.getenv("TELEGRAM_API"), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("check_stalked", check_stalked))
    dp.add_handler(CommandHandler("stalk", stalk))
    dp.add_handler(CommandHandler("list", list))
    dp.add_handler(CommandHandler("check", check))
    dp.add_handler(CommandHandler("dao", dao))
    dp.add_handler(CommandHandler("contains", contains))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    TOKEN = os.getenv("TELEGRAM_API")
    PORT = int(os.getenv('PORT', '8443'))
    updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN,
                        webhook_url="https://twitterbotto.herokuapp.com/" + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
