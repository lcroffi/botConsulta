import telebot
bot = telebot.TeleBot("503578488:AAEmi4K0-arlUIGXzg6WEsnCbaGQiReR-oQ")
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, u"Olá, eu sou a Lucy!")
bot.polling()