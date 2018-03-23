import telepot
from chatbot import chatbot

telegram = telepot.Bot('503578488:AAEmi4K0-arlUIGXzg6WEsnCbaGQiReR-oQ')

bot = chatbot('Lucy')

def recebendoMsg(msg):
    frase = bot.escuta(frase=msg['text'])
    resp = bot.pensa(frase)
    bot.fala(resp)
    #chatID = msg['chat']['id']
    tipoMsg, tipoChat, chatID = telepot.glance(msg)
    telegram.sendMessage(chatID,resp)

telegram.message_loop(recebendoMsg)

while True:
    pass