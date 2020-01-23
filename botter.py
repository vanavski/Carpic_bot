# -*- coding: utf-8 -*-

import telebot
import requests
import cv2
import numpy as np

# TELEBOT

TELEBOT_TOKEN = 'TOKEN'
API_TOKEN = 'TOKEN'

# Указываем к какому боту будем обращаться
bot = telebot.TeleBot(TELEBOT_TOKEN)

def get_gray_pic(message):
    photo = cv2.imread('no-bg.png')
    gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('gray.jpg', gray)
    edged = cv2.Canny(gray, 10, 250)
    cv2.imwrite('edged.jpg', cv2.bitwise_not(edged))
    gray_pic = open('gray.jpg', 'rb')
    edged_pic = open('edged.jpg', 'rb')
    bot.send_photo(message.chat.id, gray_pic)
    bot.send_photo(message.chat.id, edged_pic)

# Настраиваем, что будет делать бот при пересылке ему картинки
@bot.message_handler(content_types=['photo'])
def photo(message):
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    # получает html картинки
    downloaded_file = bot.download_file(file_info.file_path)

    # записывает картинку на компухтер
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
        bot.send_message(message.from_user.id, "Сохранил")

        # отправляем картинку в апишку и записываем оттуда готовый вариант на компухтер к файлу .py
        setWithoutBG()
        # считываем готовую картинку
        img = open('no-bg.png', 'rb')
        # отправляем боту
        bot.send_photo(message.chat.id, img)
        get_gray_pic(message)

# Использование API https://www.remove.bg/
# 50 бесплатных картинок на пользователя. В крайнем случае создать нового пользователя на сайте)0
def setWithoutBG():
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(r'D:\Python\OPEN CV\image.jpg', 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': API_TOKEN},
    )
    if response.status_code == requests.codes.ok:
        # записываем файл с именем no-bg.png в папку, где находится .py файл
        with open('no-bg.png', 'wb') as new_file:
            new_file.write(response.content)
    else:
        print("Error:", response.status_code, response.text)

# Что делает бот, если написать ему сообщение
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

# Запускает бота
bot.polling(none_stop=True, interval=0)