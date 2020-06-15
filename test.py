# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 12:03:21 2020

@author: aovch
"""

token = '1166987527:AAF6t4J0TY-tTOJNEzxcxYDts27vqQjdDCM'



import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler,Filters
from Investment.InvestFuncs import StockInfo
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    keyboard = [[InlineKeyboardButton("Portfolio", callback_data='portfolio'),
                 InlineKeyboardButton("Search company", callback_data='search')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


#####Company Search
def search_company(update, context):
    if context.user_data['search'] == True:
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
Нужна подписка: {i[6]}""")
            else:
                update.message.reply_text("К сожалению, новостей нет")
        except Exception as e:
            update.message.reply_text("Введите верный тикер")
    else:
        print('No')
        pass

def search_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Введите тикер компании и количество последних новостей Например: AAPL 3'".format(query.data))
    context.user_data['search'] = True


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