import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
import config
import languages

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# States
LANGUAGE, Q1, Q2, Q3, Q4, Q5, Q6 = range(7)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Reset user data
    context.user_data.clear()
    
    # Language selection keyboard
    keyboard = [['English 🇺🇸', 'Русский 🇷🇺', 'Қазақша 🇰🇿']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "Please choose your language / Пожалуйста, выберите язык / Тілді таңдаңыз:",
        reply_markup=reply_markup
    )
    return LANGUAGE

async def language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lang_code = 'en'
    if 'Русский' in text:
        lang_code = 'ru'
    elif 'Қазақша' in text:
        lang_code = 'kz'
    
    context.user_data['lang'] = lang_code
    texts = languages.TEXTS[lang_code]
    
    await update.message.reply_text(texts['language_selected'])
    
    # Ask Q1
    keyboard = [texts['q1_opts']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(texts['q1'], reply_markup=reply_markup)
    return Q1

async def q1_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q1'] = update.message.text
    lang_code = context.user_data['lang']
    texts = languages.TEXTS[lang_code]
    
    # Ask Q2
    keyboard = [texts['q2_opts']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(texts['q2'], reply_markup=reply_markup)
    return Q2

async def q2_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q2'] = update.message.text
    lang_code = context.user_data['lang']
    texts = languages.TEXTS[lang_code]
    
    # Ask Q3
    keyboard = [texts['q3_opts']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(texts['q3'], reply_markup=reply_markup)
    return Q3

async def q3_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q3'] = update.message.text
    lang_code = context.user_data['lang']
    texts = languages.TEXTS[lang_code]
    
    # Ask Q4
    keyboard = [texts['q4_opts']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(texts['q4'], reply_markup=reply_markup)
    return Q4

async def q4_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q4'] = update.message.text
    lang_code = context.user_data['lang']
    texts = languages.TEXTS[lang_code]
    
    # Ask Q5
    keyboard = [texts['q5_opts']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(texts['q5'], reply_markup=reply_markup)
    return Q5

async def q5_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q5'] = update.message.text
    lang_code = context.user_data['lang']
    texts = languages.TEXTS[lang_code]
    
    # Ask Q6
    keyboard = [texts['q6_opts']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(texts['q6'], reply_markup=reply_markup)
    return Q6

async def q6_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q6'] = update.message.text
    lang_code = context.user_data['lang']
    texts = languages.TEXTS[lang_code]
    
    # Finish
    answers = context.user_data
    result_text = texts['done']
    result_text += f"1. {answers.get('q1')}\n"
    result_text += f"2. {answers.get('q2')}\n"
    result_text += f"3. {answers.get('q3')}\n"
    result_text += f"4. {answers.get('q4')}\n"
    result_text += f"5. {answers.get('q5')}\n"
    result_text += f"6. {answers.get('q6')}\n\n"
    
    # Simple logic for recommendation (Placeholder)
    # In a real app, this would query a DB or use more complex logic
    rec = ""
    q1_val = answers.get('q1')
    
    if lang_code == 'en':
        rec = "Based on your preferences, we recommend visiting the National Parks!"
    elif lang_code == 'ru':
        rec = "На основе ваших предпочтений, мы рекомендуем посетить Национальные Парки!"
    else:
        rec = "Сіздің қалауыңыз бойынша Ұлттық саябақтарға баруды ұсынамыз!"
        
    await update.message.reply_text(result_text + rec, reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text(texts['restart'])
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Canceled / Отменено / Болдырмау", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, language_choice)],
            Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, q1_response)],
            Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, q2_response)],
            Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, q3_response)],
            Q4: [MessageHandler(filters.TEXT & ~filters.COMMAND, q4_response)],
            Q5: [MessageHandler(filters.TEXT & ~filters.COMMAND, q5_response)],
            Q6: [MessageHandler(filters.TEXT & ~filters.COMMAND, q6_response)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    application.add_handler(conv_handler)
    
    print("Bot is running...")
    application.run_polling()
