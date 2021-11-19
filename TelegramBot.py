import requests
import telebot
from telebot import types


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

        self.token = token
        self.user_id = id
        self.bot = telebot.TeleBot(token)
        self.registration_message_reader(self.get_message)
        self.menu = []

    def del_message_reader(self):
        self.bot.message_handlers = []

    def registration_message_reader(self, func, content_types=['text']):
        self.bot.add_message_handler({'function': func, 'filters': {'content_types': content_types}})
        print(self.bot.message_handlers)

    def get_message(self, message):
        work = True
        if self.user_id != -1:
            if self.user_id != message.from_user.id:
                print(f"Письмо от незарегистрированного пользователя: {message.from_user.id}")
                work = False

        if work:
            self.send_message(message.text)

    def getKeyboard(self, button_=None):
        if button_ is None:
            button_ = self.menu
        # Создание клавиатуры для ответов
        keyboard = types.ReplyKeyboardMarkup()
        try:
            for i in button_:
                keyboard.add(types.KeyboardButton(text=i))
        except TypeError:
            keyboard = types.ReplyKeyboardRemove()
        return keyboard

    def send_message(self, text, button_=None, id=-1, message=None):
        if message is None:
            if id == -1:
                if self.user_id == -1:
                    raise BotError("Ошибка отправки сообщения, не указан ID")
                else:
                    id = self.user_id
        else:
            id = message.from_user.id

        if button_ is None:
            self.bot.send_message(id, text)
        else:
            keybord = self.getKeyboard(button_)
            self.bot.send_message(id, text, reply_markup=keybord)

    def get_voice(self, message, path):
        file_info = self.bot.get_file(message.voice.file_id)
        file_ = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(self.token, file_info.file_path)).content
        with open(path, "wb") as open_file:
            open_file.write(file_)

    def start(self):
        self.bot.polling()
