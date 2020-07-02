# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:01:33 2020

@author: aovch
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 16:56:39 2020

@author: aovch
"""

import logging

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)
from Investment.InvestFuncs import StockInfo

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SELECT_NODE,Portfolio, News,SEARCH = map(chr, range(0,4))

(START_OVER,DONE,BACK) = map(chr, range(4, 7))

END = ConversationHandler.END



def start(update, context):
    keyboard = [[InlineKeyboardButton("Portfolio", callback_data=str(Portfolio)),
                 InlineKeyboardButton("Search company", callback_data=str(News))]]
    
    text = 'Choice your destiny:'
    
    reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
    ###prerequsites for multilevel menu
    if context.user_data.get(START_OVER):
        context.user_data[START_OVER] = True
    else:
        context.user_data[START_OVER] = False
    context.user_data['search'] = False
    ####does program start 1st time
    
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
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Введите тикер компании и количество последних новостей Например: AAPL 3'")
    context.user_data[START_OVER] = True
    context.user_data['search'] = True
    return SEARCH

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def stop(update, context):
    """End Conversation by command."""
    update.message.reply_text('Okay, bye.')
    return END

def search_company(update, context):
    print(context.user_data['search'] == True and update.message.text.split(' ')[0] != '/start')
    if context.user_data['search'] == True and update.message.text.split(' ')[0] != '/start':
        text = update.message.text.split(' ')
        try:
            stock = StockInfo()
            data = stock.get_news(text[0],text[1])
            if len(data)>0:
                for i in data:
                    if i[6]:
                        subs = 'Да'
                    else:
                        subs = 'Нет'
                    update.message.reply_text(f"""Время: {i[0]}
Заголовок: {i[1]}
Источник:{i[2]}
Анонс:{i[3]}
Ссылка:{i[4]}
Язык:{i[5]}
Нужна подписка: {subs}""")
            else:
                update.message.reply_text("К сожалению, новостей нет")
        except:
            update.message.reply_text("Введите верный тикер")
    else:
        print("Here")
        return BACK
        pass


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
        CallbackQueryHandler(back_to_menu, pattern='^' + str(DONE) + '$'),
    ]
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        
        states={
            SELECT_NODE: selection_handlers,
            SEARCH: [MessageHandler(Filters.text, search_company),],
            BACK: [CallbackQueryHandler(back_to_menu, pattern='^' + str(BACK) + '$')]
        },
        fallbacks=[CommandHandler('stop', stop),
                   CommandHandler('help', help)],
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
