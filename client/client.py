import threading
import socket
import json
import os
import getpass
from module import msg, entry, MSGSystem, hash_data, generate_user_id

msg("Initializing: config.json")

if os.path.exists('./files/config.json'):
    with open("./files/config.json", "r") as config_file:
        config = json.load(config_file)
else:
    msg(message='File not found: config.json', type_msg="system")

msg("Initializing: langs.json")
if os.path.exists('./files/langs.json'):
    with open("./files/langs.json", "r") as lang_file:
        langs = json.load(lang_file)
else:
    msg(message='File not found: langs.json', type_msg="system")

msg("Configuring system message language...")
lang_system = langs[config['lang']]
msg_system = MSGSystem(config["lang"], langs_db=langs)

msg("Initializing functions...")

def connect_server():
    client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    for server_adr in config["servers"]:
        msg(message=f"{lang_system['trying_to_connect']}: {server_adr}")
        try:
            host = server_adr
            port = config["port_system"]

            client_connection.connect((host, port))
            return client_connection

        except:
            msg(f"--- {lang_system['not_connected']}")

def receiveMessages(client_connection, username):
    while True:
        try:
            server_msg = client_connection.recv(2048).decode('utf-8')
            if server_msg:
                # Exibe as mensagens recebidas com o formato correto
                msg(f'{server_msg}\n')
        except:
            msg('\nFailed to stay connected to the server!\n')
            msg('Press <Enter> to continue...')
            client_connection.close()
            break

def sendMessages(client_connection, username):
    while True:
        try:
            msg_input = entry(f'\n>>> ')
            if msg_input.startswith('/'):
                handle_local_commands(msg_input, client_connection)
            else:
                # Envia as mensagens com o formato adequado
                client_connection.send(f'[{username} (You)]: {msg_input}'.encode('utf-8'))
        except:
            return

def send_server_commands(command, client_connection):
    try:
        client_connection.send(command.encode('utf-8'))
    except: 
        return False

def login_system(client_connection):    

    msg(msg_system.lang_msg["do_you_have_an_account"])
    verification = entry("Yes = y | No = n :")

    msg_system.break_space(100)
    msg_system.separator()

    if verification.lower() == "y":
        while True:
            msg(msg_system.lang_msg["login_account"])
            msg_system.separator()
            msg_system.break_space(2)

            user_token = entry(f"{msg_system.lang_msg['user_token']} >>> ")
            password = getpass.getpass(f"{msg_system.lang_msg['password']} >>> ")

            user_token_hash = hash_data(user_token)
            password_hash = hash_data(password)

            command = f"/|/login {user_token_hash} {password_hash}"
            send_server_commands(command, client_connection)
            
            response = client_connection.recv(2048).decode('utf-8')
            if "successful" in response.lower():
                msg(msg_system.lang_msg["login_success"])
                # Recebe o nickname após o login
                send_server_commands(f"/|/get_nickname {user_token_hash}", client_connection)
                user_nickname = client_connection.recv(2048).decode('utf-8')
                return user_nickname
            else:
                msg(msg_system.lang_msg["login_failed"])
                continue

    elif verification.lower() == "n":
        nickname = entry(f"{msg_system.lang_msg['user']} >>> ")
        password = entry(f"{msg_system.lang_msg['password']} >>> ")

        user_id = generate_user_id()
        user_id_hash = hash_data(user_id)
        password_hash = hash_data(password)

        # Exibe o ID de usuário e espera que o usuário pressione Enter para copiá-lo
        msg(f"{msg_system.lang_msg['id_display']} {user_id}")
        entry(msg_system.lang_msg["waiting_for_copy"])

        # Limpa a tela ou limpa o histórico de mensagens
        os.system('cls' if os.name == 'nt' else 'clear')

        # Envia o comando de registro para o servidor
        command = f"/|/register {nickname} {user_id_hash} {password_hash}"
        send_server_commands(command, client_connection)
        response = client_connection.recv(2048).decode('utf-8')
        
        msg(response)

        # Dá boas-vindas e inicia o chat
        msg(msg_system.lang_msg["welcome"])
        return nickname

def handle_local_commands(command, client_connection):
    """
    Trata comandos locais do cliente antes de enviar ao servidor
    """
    if command.startswith('/pay'):
        client_connection.send(command.encode('utf-8'))
        response = client_connection.recv(2048).decode('utf-8')
        msg(response)
    elif command.startswith('/private') or command.startswith('/msgbox'):
        client_connection.send(command.encode('utf-8'))
        response = client_connection.recv(2048).decode('utf-8')
        msg(response)

    elif command.startswith('/exit'):
        client_connection.close()

    else:
        send_server_commands(command, client_connection)

def main():
    msg_system.break_space()
    msg_system.separator()

    client_connection = connect_server()
    if client_connection:

        msg_system.welcome()
        username = login_system(client_connection)

        if not username:
            msg(msg_system.lang_msg["failed_login"])
            return

        msg_system.break_space(100)
        msg_system.welcome()
        msg(f'\n{msg_system.lang_msg["connected_as"]} {username}')

        thread1 = threading.Thread(target=receiveMessages, args=[client_connection, username])
        thread2 = threading.Thread(target=sendMessages, args=[client_connection, username])

        thread1.start()
        thread2.start()

if __name__ == "__main__":
    msg("Initializing system...")
    main()
