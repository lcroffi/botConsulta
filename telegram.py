import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from chatbot import chatbot

telegram = telepot.Bot('570291084:AAEHYbsvh-EFVVMuzu4YwxUMFEwEoudSAW4')

bot = chatbot('Lucy')

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def recebendoMsg(msg):
    frase = bot.escuta(frase=msg['text'])
    resp = bot.pensa(frase)
    bot.fala(resp)
    #chatID = msg['chat']['id']
    tipoMsg, tipoChat, chatID = telepot.glance(msg)
    if 'consulta' in frase:
            button_list = [
                    InlineKeyboardButton(text="Cardiologista", callback_data='cardio'),
                    InlineKeyboardButton(text="Clínico Geral", callback_data='clinic'),
                    InlineKeyboardButton(text="Dermatologista", callback_data='dermo'),
                    InlineKeyboardButton(text="Endocrinologista", callback_data='endoc'),
                    InlineKeyboardButton(text="Gastroenterologista", callback_data='pneumo'),
                    InlineKeyboardButton(text="Ginecologista", callback_data='gineco'),
                    InlineKeyboardButton(text="Oftalmologista", callback_data='oftalmo'),
                    InlineKeyboardButton(text="Pneumologista", callback_data='pneumo'),
                    InlineKeyboardButton(text="Outro", callback_data='outro')
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=build_menu(button_list, n_cols=2))
            medico = telegram.sendMessage(chatID, 'Temos as seguintes especialidades disponíveis:', reply_markup=reply_markup)
            
    else:
        telegram.sendMessage(chatID,resp)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    
    resp = bot.pensa(query_data)
    bot.fala(resp)
    telegram.answerCallbackQuery(query_id, text='Certo.')

MessageLoop(telegram, {'chat': recebendoMsg,
                  'callback_query': on_callback_query}).run_as_thread()

while True:
    pass
