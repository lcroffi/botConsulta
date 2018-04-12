import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
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
                    KeyboardButton(text="Cardiologista", callback_data='cardio'),
                    KeyboardButton(text="Clínico Geral", callback_data='clinic'),
                    KeyboardButton(text="Dermatologista", callback_data='dermo'),
                    KeyboardButton(text="Endocrinologista", callback_data='endoc'),
                    KeyboardButton(text="Gastroenterologista", callback_data='pneumo'),
                    KeyboardButton(text="Ginecologista", callback_data='gineco'),
                    KeyboardButton(text="Oftalmologista", callback_data='oftalmo'),
                    KeyboardButton(text="Pneumologista", callback_data='pneumo'),
                    KeyboardButton(text="Urologista", callback_data='uro')
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard=build_menu(button_list, n_cols=3), one_time_keyboard=True)
            medico = telegram.sendMessage(chatID, 'Qual médico você está procurando?', reply_markup=reply_markup)
            
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
