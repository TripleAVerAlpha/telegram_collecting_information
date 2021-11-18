from TelegramBot import Bot
import pandas as pd
import os


def get_message(message):
    if "+" in message.text:
        text = message.text.replace('+ ', '')
        b.send_message(f"Добавляю: {text}")


if os.path.exists("model/line.csv"):
    all_data = pd.read_csv("model/line.csv", index_col=0)
else:
    all_data = pd.DataFrame(columns=["Текст", "Файл"])
b = Bot(file="Data/setting")
b.registration_message_reader(get_message)
b.start()
