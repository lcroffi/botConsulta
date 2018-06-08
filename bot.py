#### Google api agenda ####
# pip install --upgrade google-api-python-client
# pip install --upgrade oauth2client
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

# lê os eventos
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('credentials.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('calendario_lucy.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='primary', timeMin=now,
                                      maxResults=10, singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])
    


# cria os eventos

def agendar():
    event = {
      'summary': 'Maria', #nome do paciente
      'location': 'Av. Perseu, 157 - Jardim Satélite',
      'description': 'Endocrinologista' #especialidade,
      'start': {
        'dateTime': '2018-05-28T09:00:00-03:00', #início
        'timeZone': 'America/Sao_Paulo',
      },
      'end': {
        'dateTime': '2018-05-28T17:00:00-03:00', #fim
        'timeZone': 'America/Sao_Paulo',
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created: %s' % (event.get('htmlLink')))




#### BOT ####
# pip install telepot
import telepot
import json
from telepot.namedtuple import ForceReply, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


####### Salvar e carregar memória do bot

def memoriaBot():
    try:
        memoria = open('Lucy.json','r')
    except FileNotFoundError:
        memoria = open('Lucy.json','w')
        memoria.write('[["Larissa","Letícia", "Jéssica"], {"oi": "Olá, com quem estou falando?","tchau":"Tchau!", "sair":"Até logo!"}, ["Médicos"]]')
        memoria.close()
        memoria = open('Lucy.json','r')
    conhecidos, frases, medicos = json.load(memoria)
    memoria.close()
    historico = [None, ]
    return conhecidos, frases, medicos, historico

####### Rodar o bot no Telegram

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
    frase = escuta(frase=msg['text'])
    resp = pensa(frase)
    fala(resp)
    #chatID = msg['chat']['id']
    tipoMsg, tipoChat, chatID = telepot.glance(msg)
    if msg == "/start":
        resp = 'Bom dia, eu sou a secretária Lucy. No que posso ajudá-lo?'
        bot.sendMessage(chatID,resp)
    elif 'endereço' or 'local' in frase:
        resp = 'Av. Perseu, 157 - Jardim Satélite'
        bot.sendMessage(chatID,resp)
    elif 'consulta' in frase:
        inline_keyboard = [
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
        bot.sendMessage(
            chatID,
            'Temos as seguintes especialidades disponíveis:',
            reply_markup = InlineKeyboardMarkup(inline_keyboard=build_menu(inline_keyboard, n_cols=2))
            )
    else:
        bot.sendMessage(chatID,resp)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    chatID = from_id
    option = query_data
    print(chatID)
    bot.answerCallbackQuery(query_id, text="Só um instante")
    print("callback query", query_id, from_id, query_data)
    resposta(chatID, option)

def resposta(chatID, option):
    if option == "cardio":
        bot.sendMessage(
                        chatID,
                        'Cardiologistas:',
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(text="Dr. Expedito Leitão", callback_data='eleitao')],
                                [InlineKeyboardButton(text="Dr. Sebastião Faria", callback_data='sfaria')]
                            ]
                        )
                    )
    elif option == "clinic":
        bot.sendMessage(
                        chatID,
                        'Clínico Geral:',
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(text="Dra. Rosa Castro", callback_data='rcastro')],
                                [InlineKeyboardButton(text="Dr. Luís Gabriel", callback_data='lgabri')]
                            ]
                        )
                    )
    elif option == "dermo":
        bot.sendMessage(
                        chatID,
                        'Dermatologista:',
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(text="Dra. Maria do Rosário Reis", callback_data='mreis')],
                                [InlineKeyboardButton(text="Dr. Renato Gomes", callback_data='rgomes')]
                            ]
                        )
                    )
    elif option == "endoc":
        bot.sendMessage(
                        chatID,
                        'Dermatologista:',
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(text="Dra. Edwiges Mota", callback_data='emota')],
                                [InlineKeyboardButton(text="Dr. Reinaldo Godoi", callback_data='rgodoi')]
                            ]
                        )
                    )
    elif option == "pneumo":
        bot.sendMessage(
                        chatID,
                        'Gastroenterologista:',
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(text="Dra. Laura Silva", callback_data='lsilva')],
                                [InlineKeyboardButton(text="Dra. Amanda Saldanha", callback_data='asal')]
                            ]
                        )
                    )
    elif option == "gineco":
        bot.sendMessage(
                        chatID,
                        'Ginecologista:',
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(text="Dra. Solange Maciel", callback_data='smac')],
                                [InlineKeyboardButton(text="Dr. Armando Oliveira", callback_data='aoliv')]
                            ]
                        )
                    )
    elif option == "oftalmo":
        bot.sendMessage(
                        chatID,
                        'Oftalmologista:',
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(text="Dra. Maíra Fernandes", callback_data='mfer')],
                                [InlineKeyboardButton(text="Dra. Nicole Almeida", callback_data='nalm')]
                            ]
                        )
                    )
    elif option == "pneumo":
        bot.sendMessage(
                        chatID,
                        'Pneumologista:',
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(text="Dr. Nilton Dias", callback_data='ndias')],
                                [InlineKeyboardButton(text="Dr. Maurício Correa", callback_data='mcorrea')]
                            ]
                        )
                    )
    elif option == "eleitao":
        bot.sendMessage (
                        chatID,
                        'Dr. Expedito Leitão:',
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(text="10:00 - 10:30", callback_data='ndias')],
                                [InlineKeyboardButton(text="10:30 - 11:00", callback_data='mcorrea')]
                                [InlineKeyboardButton(text="11:00 - 11:30", callback_data='mcorrea')]
                                [InlineKeyboardButton(text="14:30 - 15:00", callback_data='mcorrea')]
                                [InlineKeyboardButton(text="15:00 - 15:30", callback_data='mcorrea')]
                            ]
                        )
                    )
                
    elif option == "outro":
        frase = 'Qual seria a especialidade que está procurando?'
        fala(frase)
        bot.sendMessage(chatID,frase)
        

####### Ações de interação do bot para deixá-lo mais humano

def escuta(frase=None):
        frase = str(frase)
        frase = frase.lower()
        return frase


def pensa(frase):
    if frase in frases:
        return frases[frase]
    if frase == 'aprende':
            return 'Digite a frase: '
   
    #Responde frases que dependem do histórico
    ultimaFrase = historico[-1]
    if ultimaFrase == 'Olá, com quem estou falando?':
        nome = pegaNome(frase)
        frase = respondeNome(nome)
        return frase
    if ultimaFrase == 'Digite a frase: ':
        chave = frase
        return 'Digite a resposta: '
    if ultimaFrase == 'Digite a resposta: ':
        resp = frase
        frases[chave] = resp
        gravaMemoria()
        return 'Aprendido'
    if ultimaFrase == 'Qual seria a especialidade que está procurando?':
        medico = frase
        medicos.append(medico)
        gravaMemoria() 
        return 'Anotado, vamos procurar essa especialidade para você.'
            
    try:
        resp = str(eval(frase))
        return resp
    except:
        pass
    return 'Posso marcar uma consulta pra você.'

            
def pegaNome(nome):
    nome = nome.title()
    return nome

def respondeNome(nome):
        if nome in conhecidos:
            frase = 'Olá outra vez, '
        else:
            frase = 'Muito prazer, '
            conhecidos.append(nome)
            gravaMemoria()            
        return frase+nome
    
def gravaMemoria():
    memoria = open('Lucy.json','w')
    json.dump([conhecidos, frases, medicos],memoria)
    memoria.close()
        
def fala(frase):
    print(frase)
    historico.append(frase)

####### Main

conhecidos, frases, medicos, historico = memoriaBot()
load = open("token.json")
token = json.loads(load.read())
bot = telepot.Bot(token[0])

bot.message_loop({'chat': recebendoMsg,
                  'callback_query': on_callback_query,})

while True:
    pass
