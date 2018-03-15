import telebot
bot = telebot.TeleBot("503578488:AAEmi4K0-arlUIGXzg6WEsnCbaGQiReR-oQ")
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, u"Bom dia, eu sou a secretária Lucy. No que posso ajudá-lo?")
bot.polling()