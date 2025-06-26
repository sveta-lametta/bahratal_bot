from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import logging
import os

# Этапы анкеты
NAME, GENDER, AGE, TYPE, ROLE = range(5)
results = []

gender_kb = ReplyKeyboardMarkup([["👦 М", "👧 Ж", "🌈 Другое"]], one_time_keyboard=True, resize_keyboard=True)
type_kb = ReplyKeyboardMarkup([
    ["🐢 Предпочитаю общаться с 1–2 людьми или быть один"],
    ["🐍 Чувствую себя нормально и в одиночку, и в компании"],
    ["🦅 Люблю быть среди людей, легко завожу знакомства"]
], one_time_keyboard=True, resize_keyboard=True)
role_kb = ReplyKeyboardMarkup([
    ["🔧 Поддерживать", "💡 Придумывать идеи"],
    ["🧭 Руководить", "👀 Наблюдать"]
], one_time_keyboard=True, resize_keyboard=True)

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Привет! Как тебя зовут?")
    return NAME

def get_name(update: Update, context: CallbackContext) -> int:
    context.user_data['name'] = update.message.text
    update.message.reply_text("Укажи свой пол:", reply_markup=gender_kb)
    return GENDER

def get_gender(update: Update, context: CallbackContext) -> int:
    context.user_data['gender'] = update.message.text
    update.message.reply_text("Сколько тебе лет?")
    return AGE

def get_age(update: Update, context: CallbackContext) -> int:
    context.user_data['age'] = update.message.text
    update.message.reply_text("Как ты чувствуешь себя в компании других людей?", reply_markup=type_kb)
    return TYPE

def get_type(update: Update, context: CallbackContext) -> int:
    context.user_data['type'] = update.message.text.split(" ", 1)[1]
    update.message.reply_text("Что тебе ближе в команде?", reply_markup=role_kb)
    return ROLE

def get_role(update: Update, context: CallbackContext) -> int:
    context.user_data['role'] = update.message.text.split(" ", 1)[1]
    update.message.reply_text("Спасибо! Твои ответы записаны ✅")
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Опрос отменён.")
    return ConversationHandler.END

def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            GENDER: [MessageHandler(Filters.text & ~Filters.command, get_gender)],
            AGE: [MessageHandler(Filters.text & ~Filters.command, get_age)],
            TYPE: [MessageHandler(Filters.text & ~Filters.command, get_type)],
            ROLE: [MessageHandler(Filters.text & ~Filters.command, get_role)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
