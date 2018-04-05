import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from chatbot import chatbot

telegram = telepot.Bot('503578488:AAEmi4K0-arlUIGXzg6WEsnCbaGQiReR-oQ')

bot = chatbot('Lucy')

def recebendoMsg(msg):
    frase = bot.escuta(frase=msg['text'])
    resp = bot.pensa(frase)
    bot.fala(resp)
    #chatID = msg['chat']['id']
    tipoMsg, tipoChat, chatID = telepot.glance(msg)
    if 'consulta' in frase:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Press me', callback_data='press')],
               ])
            telegram.sendMessage(chatID, 'Use inline keyboard', reply_markup=keyboard)
    else:
        telegram.sendMessage(chatID,resp)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    telegram.answerCallbackQuery(query_id, text='Got it')

MessageLoop(telegram, {'chat': recebendoMsg,
                  'callback_query': on_callback_query}).run_as_thread()

while True:
    pass
