# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 16:56:39 2020

@author: aovch
"""

import logging

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SELECT_NODE,Portfolio, News = map(chr, range(0,3))

(START_OVER,DONE) = map(chr, range(4, 6))

END = ConversationHandler.END



def start(update, context):
    keyboard = [[InlineKeyboardButton("Portfolio", callback_data=str(Portfolio)),
                 InlineKeyboardButton("Search company", callback_data=str(News))]]
    
    text = 'Choice your destiny:'
    
    reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    if context.user_data.get(START_OVER):
        context.user_data[START_OVER] = True
    else:
        context.user_data[START_OVER] = False
    print(context.user_data[START_OVER])
    if context.user_data[START_OVER]:
        update.callback_query.answer()
        update.callback_query.edit_message_text(text='Start again:', reply_markup=reply_markup)
    else:
        update.message.reply_text(text=text, reply_markup=reply_markup)

    return SELECT_NODE

def back_to_menu(update, context):
    """Return to top level conversation."""
    context.user_data[START_OVER] = True
    start(update, context)

    return END


def choose_portfolio(update, context):
    update.callback_query.answer()
    keyboard = [[InlineKeyboardButton("Done", callback_data=str(DONE))]]
    
    text = 'Sorry, portfolio is still in work'
    
    reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)

    update.callback_query.edit_message_text(text, reply_markup=reply_markup)

def choose_news(update, context):
    update.callback_query.answer()
    update.callback_query.edit_message_text(
        'Sorry, news is still in work')
    context.user_data[START_OVER] = True
    start(update, context)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def stop(update, context):
    """End Conversation by command."""
    update.message.reply_text('Okay, bye.')
    return END

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater('', use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    selection_handlers = [
        CallbackQueryHandler(choose_portfolio, pattern='^' + str(Portfolio) + '$'),
        CallbackQueryHandler(choose_news, pattern='^' + str(News) + '$'),
        CallbackQueryHandler(back_to_menu, pattern='^' + str(DONE) + '$')
    ]
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        
        states={
            SELECT_NODE: selection_handlers,
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    dp.add_handler(conv_handler)
    
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
