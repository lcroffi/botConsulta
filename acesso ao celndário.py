from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

scopes = 'http://www.googleapi.com/auth/calender.readonly'
client_secret_file = 'calender.json'
aplicativo = 'Google Calendar API Python Quickstart'

def get_credencial():
    home_dir = os.path.expanduser('~')
    credencial_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credencial_dir):
        os.makedirs(credencial_dir)
    credencial_path = os.path.join(credencial_dir, 'calendar-python-quickstart.json')


    store = Storage(credencial_path)
    credencial = store.get()
    if not credencial or credencial.invalid:
        flow = client.flow_from_clientsecrets(client_secret_file, scopes)
        flow.user_agent = aplicativo
        if flags:
            credencial = tools.run_flow(flow, store, flags)
        else:
            credencial = tools.run(flow, store)
        print('Armazenando credencial para: ' + credencial_path)
    return credencial


def main():
    credencial = get_credencial()
    http = credencial.authorize(httplib2.Http())
    servico = dscovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print('obtendo os proximos eventos')
    resultado = service.events().list(calendarId = 'primary', timeMin = now, maxResultao=10, singleEvents=True,
                                      orderBy='startTime').execute()
    evento = resultado.get('items', [])

    if not evento:
        print('não há eventos')
    for k in evento:
        start = k['start'].get('dateTime', k['start'].get('date'))
        print(start, k['summary'])

if __name__ == '__main__':
    main()
