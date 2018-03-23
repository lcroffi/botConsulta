import json

class chatbot():
    def __init__(self, nome):
        try:
            memoria = open(nome+'.json','r')
        except FileNotFoundError:
            memoria = open(nome+'.json','w')
            memoria.write('[["Larissa","Letícia", "Jéssica"], {"oi": "Olá, com quem estou falando?","tchau":"tchau", "sair":"Até logo", "/start":"Bom dia, eu sou a secretária Lucy. No que posso ajudá-lo?"}]')
            memoria.close()
            memoria = open(nome+'.json','r')
        self.nome = nome
        self.conhecidos, self.frases = json.load(memoria)
        memoria.close()
        self.historico = [None, ]

    def escuta(self,frase=None):
        frase = str(frase)
        frase = frase.lower()
        return frase

    def pensa(self,frase):
        if frase in self.frases:
            return self.frases[frase]
        if frase == 'aprende':
            return 'Digite a frase: '
            
        #Responde frases que dependem do histórico
        ultimaFrase = self.historico[-1]
        if ultimaFrase == 'Olá, com quem estou falando?':
            nome = self.pegaNome(frase)
            frase = self.respondeNome(nome)
            return frase
        if ultimaFrase == 'Digite a frase: ':
            self.chave = frase
            return 'Digite a resposta: '
        if ultimaFrase == 'Digite a resposta: ':
            resp = frase
            self.frases[self.chave] = resp
            self.gravaMemoria()
            return 'Aprendido'
        try:
            resp = str(eval(frase))
            return resp
        except:
            pass
        return 'Não entendi'
            
    def pegaNome(self,nome):
        nome = nome.title()
        return nome

    def respondeNome(self,nome):
        if nome in self.conhecidos:
            frase = 'Olá outra vez, '
        else:
            frase = 'Muito prazer, '
            self.conhecidos.append(nome)
            self.gravaMemoria()            
        return frase+nome
    
    def gravaMemoria(self):
        memoria = open(self.nome+'.json','w')
        json.dump([self.conhecidos, self.frases],memoria)
        memoria.close()