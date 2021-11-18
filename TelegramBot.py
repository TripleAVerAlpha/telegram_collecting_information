import telebot


class BotError(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class Bot:
    def __init__(self, token=None, id=-1, file=None):
        if token is None:
            if file is None:
                raise BotError("Не указан Токен бота")
            else:
                try:
                    with open(file, "r") as read_file:
                        line = read_file.read().split("\n")
                    token = line[0]
                    if len(line) > 1:
                        id = int(line[1])
                except FileNotFoundError as e:
                    raise BotError("Ошибка открытия файла: " + str(e))
        if token == "":
            raise BotError("Токен пустой")

        self.user_id = id
        self.bot = telebot.TeleBot(token)
        self.registration_message_reader(self.get_message)

    def registration_message_reader(self, func, content_types=['text']):
        self.bot.message_handlers = []
        self.bot.add_message_handler({'function': func, 'filters': {'content_types': content_types}})

    def get_message(self, message):
        work = True
        if self.user_id != -1:
            if self.user_id != message.from_user.id:
                print(f"Письмо от незарегистрированного пользователя: {message.from_user.id}")
                work = False

        if work:
            self.send_message(message.text)

    def send_message(self, text, id=-1, message=None):
        if message is None:
            if id == -1:
                if self.user_id == -1:
                    raise BotError("Ошибка отправки сообщения, не указан ID")
                else:
                    id = self.user_id
        else:
            id = message.from_user.id

        self.bot.send_message(id, text)

    def start(self):
        self.bot.polling()
