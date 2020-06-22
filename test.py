# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 12:03:21 2020

@author: aovch
"""

token = '1166987527:AAF6t4J0TY-tTOJNEzxcxYDts27vqQjdDCM'


import logging

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler,Filters
from Menu.Start import start
from Menu.Search import search_company,search_menu

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)
    db = updater.dispatcher
    print('Bot inited')
    db.add_handler(CommandHandler('start', start))
    db.add_handler(CallbackQueryHandler(search_menu))
    db.add_handler(MessageHandler(Filters.text, search_company))
    db.add_handler(CommandHandler('help', help))
    db.add_error_handler(error)
    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()