import json

class chatbot():
    def __init__(self, nome):
        try:
            memoria = open(nome+'.json','r')
        except FileNotFoundError:
            memoria = open(nome+'.json','w')
            memoria.write('[["Larissa","Letícia", "Jéssica"], {"oi": "Olá, com quem estou falando?","tchau":"Tchau!", "sair":"Até logo!"}, ["Médicos"]]')
            memoria.close()
            memoria = open(nome+'.json','r')
        self.nome = nome
        self.conhecidos, self.frases, self.medicos = json.load(memoria)
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
        if frase == 'cardiologista' or frase == 'clínico geral' or frase == 'dermatologista' or frase == 'endocrinologista' or frase == 'gastroenterologista' or frase == 'ginecologista' or frase == 'oftalmologista' or frase == 'pneumologista':
            return 'Temos um horário às 16h com a Dra. Cláudia, pode ser?'
        if frase == 'outro':
            return 'Qual seria a especialidade que está procurando?'
        if frase == "/start":
            return 'Bom dia, eu sou a secretária Lucy. No que posso ajudá-lo?'
            
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
        if ultimaFrase == 'Qual seria a especialidade que está procurando?':
            medico = frase
            self.medicos.append(medico)
            self.gravaMemoria() 
            return 'Anotado, vamos procurar essa especialidade.'
            
        try:
            resp = str(eval(frase))
            return resp
        except:
            pass
        return 'Posso marcar uma consulta pra você.'

            
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
        json.dump([self.conhecidos, self.frases, self.medicos],memoria)
        memoria.close()
        
    def fala(self,frase):
        print(frase)
        self.historico.append(frase)
