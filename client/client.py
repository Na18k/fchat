# +---------------------------------------------------------------------------------------+
# |                                                                                       |
# |   _____ ____ _           _      __  _____                 ____ _           _    __    |
# |  |  ___/ ___| |__   __ _| |_   / / |  ___| __ ___  ___   / ___| |__   __ _| |_  \ \   |
# |  | |_ | |   | '_ \ / _` | __| | |  | |_ | '__/ _ \/ _ \ | |   | '_ \ / _` | __|  | |  |
# |  |  _|| |___| | | | (_| | |_  | |  |  _|| | |  __/  __/ | |___| | | | (_| | |_   | |  |
# |  |_|   \____|_| |_|\__,_|\__| | |  |_|  |_|  \___|\___|  \____|_| |_|\__,_|\__|  | |  |
# |                                \_\                                              /_/   |
# |                                                                                       |
# +---------------------------------------------------------------------------------------+
#   Developed by: Kainan Henrique
#   Created in: 01/09/2024 [dd/mm/YY]
#   Release: 0.0.1
#   License: MIT
# 
#   Contributions:
#       - 
# 

# +----------------------------------------+
# |                                        |
# |   ___                            _     |
# |  |_ _|_ __ ___  _ __   ___  _ __| |_   |
# |   | || '_ ` _ \| '_ \ / _ \| '__| __|  |
# |   | || | | | | | |_) | (_) | |  | |_   |
# |  |___|_| |_| |_| .__/ \___/|_|   \__|  |
# |                |_|                     |
# |                                        |
# +----------------------------------------+
import threading
import socket
import json
import os
from module import msg, MSGSystem

# +--------------------------------------------------+
# |                                                  |
# |   _                    _   _____ _ _             |
# |  | |    ___   __ _  __| | |  ___(_) | ___  ___   |
# |  | |   / _ \ / _` |/ _` | | |_  | | |/ _ \/ __|  |
# |  | |__| (_) | (_| | (_| | |  _| | | |  __/\__ \  |
# |  |_____\___/ \__,_|\__,_| |_|   |_|_|\___||___/  |
# |                                                  |
# +--------------------------------------------------+
msg("Initializing: config.json")

if os.path.exists('./files/config.json'):
    with open("./files/config.json", "r") as config_file:
        config = json.load(config_file)
else:
    msg(message='File not found: config.json', type_msg="sytem")

msg("Initializing: langs.json")
if os.path.exists('./files/langs.json'):
    with open("./files/langs.json", "r") as lang_file:
        langs = json.load(lang_file)

else:
    msg(message='File not found: langs.json', type_msg="sytem")


msg("Configuring system message language...")

# Configura as linguagens do sistema
lang_system = lang=langs[config['lang']]
msg_system = MSGSystem(config["lang"], langs_db=langs)


msg("Initializing functions...")
def main():
    msg_system.welcome()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    for server_adr in config["servers"]:
        try:
            host = server_adr
            port = config["port_system"]

            client.connect((host, port))

        except:
            return msg(message='Não foi possívvel se conectar ao servidor!', type_msg="sytem", lang=lang_system)

    username = input('Usuário> ')
    msg('\nConectado')

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    thread1.start()
    thread2.start()


def receiveMessages(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            msg(msg+'\n')
        except:
            msg('\nNão foi possível permanecer conectado no servidor!\n')
            msg('Pressione <Enter> Para continuar...')
            client.close()
            break
            

def sendMessages(client, username):
    while True:
        try:
            msg = input('\n')
            client.send(f'<{username}> {msg}'.encode('utf-8'))
        except:
            return

msg("Initializing system...")
main()