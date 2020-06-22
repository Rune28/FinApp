from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler,Filters



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
