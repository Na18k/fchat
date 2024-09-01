
def msg(message, type_msg="", lang=None):
    # Para fácil manutenção!
    # Caso o sistema no futuro mude
    if type_msg == '':
        print(message)

    elif type_msg == "system":
        print(f'[{lang["system_lang"]}]: {message}')

    elif type_msg == "system" and lang == None:
        # Se não for caregado a linguagem
        print(f'[SYSTEM]: {message}')

class MSGSystem:
    def __init__(self, lang, langs_db):
        self.lang_msg = langs_db[lang]

    def welcome(self):
        msg("Welcome message:")
        msg(f"""
            +---------------------------------------------------------+
            |                                                         |
            |  __        __   _                            _          |
            |  \ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___    |
            |   \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \   |
            |    \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) |  |
            |     \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/   |
            |                                                         |
            |    _____ ____ _           _                             |
            |   |  ___/ ___| |__   __ _| |_                           |
            |   | |_ | |   | '_ \ / _` | __|                          |
            |   |  _|| |___| | | | (_| | |_                           |
            |   |_|   \____|_| |_|\__,_|\__|                          |
            |                                                         |
            +---------------------------------------------------------+

            {self.lang_msg["help_command_info"]}
        """)
