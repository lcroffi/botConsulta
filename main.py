from Chatbot import Chatbot

Bot = Chatbot('Lucy')
while True:
    frase = Bot.escuta()
    resp = Bot.pensa(frase)
    Bot.fala(resp)
    if resp == 'tchau' or resp == 'sair':
        break