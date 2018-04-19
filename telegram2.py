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
                    KeyboardButton(text="Cardiologista"),
                    KeyboardButton(text="Clínico Geral"),
                    KeyboardButton(text="Dermatologista"),
                    KeyboardButton(text="Endocrinologista"),
                    KeyboardButton(text="Gastroenterologista"),
                    KeyboardButton(text="Ginecologista"),
                    KeyboardButton(text="Oftalmologista"),
                    KeyboardButton(text="Pneumologista"),
                    KeyboardButton(text="Outro")
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard=build_menu(button_list, n_cols=2), one_time_keyboard=True)
            msg = telegram.sendMessage(chatID, 'Temos as seguintes especialidades disponíveis:', reply_markup=reply_markup)
            
    else:
        telegram.sendMessage(chatID,resp)

MessageLoop(telegram, {'chat': recebendoMsg}).run_as_thread()

while True:
    pass
