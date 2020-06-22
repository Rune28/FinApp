from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def start(update, context):
    keyboard = [[InlineKeyboardButton("Portfolio", callback_data='portfolio'),
                 InlineKeyboardButton("Search company", callback_data='search')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)
