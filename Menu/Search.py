
from Investment.InvestFuncs import StockInfo
from Database.DBHelper import finapp_stocks
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

#####Company Search
def search_company(update, context):
    if context.user_data['search'] == True:
        ###split user text on name and qty of news
        text = update.message.text.split(' ')
        ###query database for symbol and name
        users_stocks = finapp_stocks.get_stocks(text[0])
        ###set qty news
        context.user_data['qty_news'] = text[1]
        ###keyboard
        keyboard_stocks = [[InlineKeyboardButton('/'.join([x[0],x[1]]) , callback_data= x[0])] for x in users_stocks]
        ##send keyboard to user
        try:
            reply_markup = InlineKeyboardMarkup(keyboard_stocks)
            query = update.callback_query
            query.answer()
            query.edit_message_text('Please choose:', reply_markup=reply_markup)
        except Exception as e:
            print(e)
    else:
        print('No')
        pass

def get_news(update, context):
    try:
        query = update.callback_query
        stock = StockInfo()
        data = stock.get_news(query.data)
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

def search_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Введите тикер.название компании и количество последних новостей Например: 'AAPL 3'")
    context.user_data['search'] = True
