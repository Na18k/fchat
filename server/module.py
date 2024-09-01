import sqlite3
import os
import random
import string

class Commands:
    def verify_command(self, msg):
        # If the message starts with "/", it is considered a command
        if msg[0] == "/":
            return True

        # If the message starts with "/|/", it is considered a system command
        if msg[0:3] == "/|/":
            return True

        return False

def generate_user_id():
    """
    Generates a unique wallet ID with uppercase letters and numbers.
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def create_database():
    if not os.path.exists('database'):
        os.makedirs('database')
    
    conn = sqlite3.connect('./database/users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id_hash TEXT PRIMARY KEY,
            nickname TEXT UNIQUE,
            password_hash TEXT,
            wallet_id TEXT UNIQUE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coins (
            wallet_id TEXT PRIMARY KEY,
            balance INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

create_database()

def register_user(nickname, id_hash, password_hash):
    conn = sqlite3.connect('./database/users.db')
    cursor = conn.cursor()
    
    wallet_id = generate_user_id()  # Generate wallet ID

    try:
        cursor.execute('INSERT INTO users (id_hash, nickname, password_hash, wallet_id) VALUES (?, ?, ?, ?)',
                       (id_hash, nickname, password_hash, wallet_id))
        cursor.execute('INSERT INTO coins (wallet_id, balance) VALUES (?, 0)', (wallet_id,))
        conn.commit()
        print(f'User registered successfully! ID: {id_hash}')
        return True
    except sqlite3.IntegrityError:
        print('Nickname already exists. Choose another.')
        return False
    
    conn.close()






def login_user(id_hash, password_hash):
    conn = sqlite3.connect('./database/users.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE id_hash = ? AND password_hash = ?', (id_hash, password_hash))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        # Apenas indica que o login foi bem-sucedido sem expor o nome
        print('Login successful.')
        return user[1]  # Retorna o nickname para o cliente
    else:
        print('Login failed.')
        return False


def get_nickname_by_id(id_hash):
    conn = sqlite3.connect('./database/users.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT nickname FROM users WHERE id_hash = ?', (id_hash,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    else:
        return None





def transfer_coins(sender_wallet, receiver_wallet, amount):
    conn = sqlite3.connect('./database/users.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT balance FROM coins WHERE wallet_id = ?', (sender_wallet,))
    sender_balance = cursor.fetchone()
    
    if not sender_balance or sender_balance[0] < amount:
        print('Insufficient funds.')
        conn.close()
        return False
    
    cursor.execute('UPDATE coins SET balance = balance - ? WHERE wallet_id = ?', (amount, sender_wallet))
    cursor.execute('UPDATE coins SET balance = balance + ? WHERE wallet_id = ?', (amount, receiver_wallet))
    conn.commit()
    conn.close()
    
    print(f'Transfer of {amount} coins completed successfully!')
    return True
