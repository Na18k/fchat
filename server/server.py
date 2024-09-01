import threading
import socket
from module import Commands, register_user, login_user, transfer_coins, get_nickname_by_id

clients = []

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('localhost', 1223))
        server.listen()
        print("Server started and listening...")
    except Exception as e:
        return print(f'\nUnable to start server! Error: {e}\n')

    while True:
        client, addr = server.accept()
        clients.append(client)
        print(f'Connection established with {addr}')

        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()


def messagesTreatment(client):
    command_handler = Commands()

    while True:
        try:
            msg = client.recv(2048).decode('utf-8')

            # Check if the message is a command
            if command_handler.verify_command(msg):
                handle_command(msg, client)
            else:
                broadcast(msg, client)

        except Exception as e:
            print(f"Error handling message: {e}")
            deleteClient(client)
            break


def handle_command(msg, client):
    """
    Função para tratar comandos específicos recebidos do cliente.
    """
    parts = msg.split()
    if msg.startswith("/|/login"):
        id_hash = parts[1]
        password_hash = parts[2]
        if login_user(id_hash, password_hash):
            response = "Login successful."
        else:
            response = "Login failed."
        client.send(response.encode('utf-8'))
    elif msg.startswith("/|/register"):
        nickname = parts[1]
        id_hash = parts[2]  # Usado diretamente, sem geração no servidor
        password_hash = parts[3]
        if register_user(nickname, id_hash, password_hash):  # Passa o id_hash diretamente
            response = "Registration successful."
        else:
            response = "Registration failed."
        client.send(response.encode('utf-8'))
    elif msg.startswith("/pay"):
        sender_wallet = parts[1]
        receiver_wallet = parts[2]
        amount = int(parts[3])
        if transfer_coins(sender_wallet, receiver_wallet, amount):
            response = f"Transfer of {amount} coins to {receiver_wallet} completed."
        else:
            response = "Transfer failed."
        client.send(response.encode('utf-8'))

    elif msg.startswith("/|/get_nickname"):
        id_hash = parts[1]
        nickname = get_nickname_by_id(id_hash)
        if nickname:
            response = nickname
        else:
            response = "User not found."
        client.send(response.encode('utf-8'))
    else:
        response = "Command not recognized."
        client.send(response.encode('utf-8'))




def broadcast(msg, client):
    for clientItem in clients:
        # if clientItem != client:
        #     try:
        #         clientItem.send(msg.encode('utf-8'))
        #     except Exception as e:
        #         print(f"Error sending message to a client: {e}")
        #         deleteClient(clientItem)

        try:
            clientItem.send(msg.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message to a client: {e}")
            deleteClient(clientItem)

def deleteClient(client):
    if client in clients:
        clients.remove(client)
        print(f"Client removed: {client}")


if __name__ == "__main__":
    main()
