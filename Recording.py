import json
import random
import subprocess
import soundfile as sf
from TelegramBot import Bot
import pandas as pd
import os

param_file = "Data/param.json"


def get_message(message):
    global manifest, param
    if "+" in message.text:
        text = message.text.replace('+ ', '')
        manifest = manifest.append({"Текст": text}, ignore_index=True)
        manifest.to_csv("Data/manifest.csv")
        bot.send_message(f"Добавляю: {text}")

    if "Запись" in message.text:
        param["record"] = True
        bot.send_message(f"Запись включина", ["Конец"])
        nextString()

    if "Конец" in message.text:
        param["record"] = False
        bot.send_message(f"Запись выключина", ["Запись", "Статистика"])

    if "Пропустить" in message.text:
        nextString()

    if "Статистика" in message.text:
        print(manifest)
        d = 0
        for i in manifest["Файл"].dropna(axis=0).index:
            if manifest.loc[i, "Длительность"] == 0:
                audio, sample_rate = sf.read(manifest.loc[i, "Файл"] + ".wav")
                manifest.loc[i, "Длительность"] = len(audio) / sample_rate
            d += manifest.loc[i, "Длительность"]
        text = ""
        stat = manifest.groupby("Текст").count()
        for i in stat.index:
            text += f"{i} -  {stat.loc[i, 'Файл']}\n"

        h = d // 3600
        m = d % 3600 // 60
        s = d % 3600 % 60
        text += f"Всего: {h} часов {m} минут {s} секунд"
        bot.send_message(text)


def record(message):
    global manifest, param
    if param["record"]:
        src_filename = f"Data/Запись {len(manifest)}.ogg"
        dest_filename = f"Data/WAV/Запись {len(manifest)}.wav"
        bot.get_voice(message, src_filename)
        outfile = open("out.txt", "w+")
        process = subprocess.run(['ffmpeg', "-i", src_filename, dest_filename], stderr=outfile)
        if process.returncode != 0:
            raise Exception("Something went wrong")
        else:
            row = {"Текст": param["record_text"], "Файл": dest_filename.replace(".wav", ""), "Длительность": 0}
            manifest = manifest.append(row, ignore_index=True)
            manifest.to_csv("Data/manifest.csv")
            nextString()
        os.remove(src_filename)


def nextString():
    global param
    stat = manifest.groupby("Текст").count().index
    text = stat[random.randint(0, len(stat)-1)]
    param["record_text"] = text
    bot.send_message(text, ["Удалить пр запись", "Пропустить", "Конец"])


if os.path.exists(param_file):
    with open(param_file, "r") as f:
        param = json.load(f)
else:
    param = {
        "record": False,
        "record_text": ""
    }
if os.path.exists("Data/manifest.csv"):
    manifest = pd.read_csv("Data/manifest.csv", index_col=0)
else:
    manifest = pd.DataFrame(columns=["Текст", "Файл"])
print(manifest)

bot = Bot(file="Data/setting")
bot.send_message("Начинаю работу", ["Запись", "Статистика"])
bot.del_message_reader()
bot.registration_message_reader(record, content_types=["voice"])
bot.registration_message_reader(get_message, content_types=["text"])
bot.start()
