import telebot
from telebot import types
import random
import os
from dotenv import load_dotenv

from telebot.apihelper import ApiTelegramException

from db import checkGroupExists, addToDB, close_db, checkUserExists, checkOrganizerByUserID, getGroupNameByUserID, getNamesByGroup, getNameIdByName, addWishListByUserID, getWishListByName, deleteRecordsByGroupName, checkUserExistsInGroup, getOrganizerGroup

load_dotenv()
token = os.getenv('token')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "ХО ХО ХО  🎅🏼️ ")
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button1 = types.KeyboardButton('Створити групу➕')
    button2 = types.KeyboardButton('Приєднатися до групи🙋🏼')
    button3 = types.KeyboardButton('Додати свій список побажань💌')
    button4 = types.KeyboardButton('Розприділити🎁')
    keyboard.add(button1, button2, button3, button4)
    explanation_text = """Цей бот - це особливий помічник Санта Клауса 🎅🏼️.
     Він допомагає вам організувати розподіл подарунків з вашими друзями. 
     Якщо ви обираєте опцію 'Створити групу➕', бот допоможе вам створити групу з назвою,
     і кожний учасник може приєднатися до неї, обираючи 'Приєднатися до групи🙋🏼'.
    Лише тоді, коли всі учасники доєднаються, організатор кнопкою 'Розприділити🎁' 
    надішлеться кожному учаснику імена людей, кому ви даритимете. Це створює чарівну атмосферу обміну подарунками.
     Нехай Різдво буде незабутнім! 🎄"""
    bot.reply_to(message, explanation_text, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Додати свій список побажань💌')
def add_user_handler(message):
    if checkUserExists(message.from_user.id):
        bot.send_message(message.chat.id, "Напишіть одним повідомленням список подарунків, які б ви хотіли отримали🎁:")
        bot.register_next_step_handler(message, get_wish_list)
    else:
        bot.send_message(message.chat.id, "Для початку приєднайтеся до групи😉")


def get_wish_list(message):
    chat_id = message.chat.id
    wish_list = message.text
    addWishListByUserID(message.from_user.id, wish_list)
    bot.send_message(chat_id, "Список побажань складений🎁")


@bot.message_handler(func=lambda message: message.text == 'Приєднатися до групи🙋🏼')
def add_user_handler(message):
    bot.send_message(message.chat.id, "Будь ласка, введіть своє ім'я:")
    bot.register_next_step_handler(message, get_user_name)


def get_user_name(message):
    chat_id = message.chat.id
    user_name = message.text

    bot.send_message(chat_id, "Тепер введіть назву групи, до якої ви хочете доєднатися:")
    bot.register_next_step_handler(message, add_to_group_step, user_name)


def add_to_group_step(message, user_name):
    chat_id = message.chat.id
    user_id = message.from_user.id
    group_name = message.text

    add_to_group(chat_id, group_name, user_name, user_id)


def add_to_group(chat_id, group_name, user_name, user_id):

    if checkGroupExists(group_name):
        if checkUserExistsInGroup(user_id, group_name):
            bot.send_message(chat_id, "Ви вже долучилися до групи✅")
        else:
            addToDB(group_name, user_name, user_id, False)
            bot.send_message(chat_id, "Ви успішно долучилися до групи🎉 Коли всі доєднаються до групи, вам прийде повідомлення з ім`ям людини, якій ви маєте підготувати подарунок🤫")
    else:
        bot.send_message(chat_id, "Такої групи не існує, зверніться до організатора❗️ Якщо організатора немає, і ви хочете створити групу нажміть на відповідну кнопку😉")


def create_group(message, chat_id, group_name, user_name, user_id):

    if not checkGroupExists(group_name):
        addToDB(group_name, user_name, user_id, True)
        bot.send_message(chat_id, f"Групу з назвою '{group_name}' створено успішно! Тепер інші можуть приєднатися до неї.")
    else:
        bot.send_message(chat_id, f"Група з назвою '{group_name}' вже існує. Будь ласка, виберіть іншу назву групи.")
        bot.register_next_step_handler(message, create_group_step, user_name)



@bot.message_handler(func=lambda message: message.text == 'Створити групу➕')
def create_group_handler(message):
    bot.send_message(message.chat.id, "Будь ласка, введіть своє ім'я:")
    bot.register_next_step_handler(message, get_user_name_create)


def get_user_name_create(message):
    chat_id = message.chat.id
    user_name = message.text

    bot.send_message(chat_id, "Тепер введіть назву групи:")
    bot.register_next_step_handler(message, create_group_step, user_name)


def create_group_step(message, user_name):
    chat_id = message.chat.id
    user_id = message.from_user.id
    group_name = message.text

    create_group(message, chat_id, group_name, user_name, user_id)  # Викликаємо функцію для створення групи


@bot.message_handler(func=lambda message: message.text == 'Розприділити🎁')
def add_user_handler(message):
    user_id = message.from_user.id
    if checkUserExists(user_id):
        if checkOrganizerByUserID(user_id):
            split(getGroupNameByUserID(user_id))
        else:
            bot.send_message(message.chat.id, "Ви не є організатором, тільки організатор може вас розприділити❗️")
    else:
        bot.send_message(message.chat.id, "Ви не є організатором, для початку створіть групу❗️")


def split(group_name):
    names = getNamesByGroup(group_name)
    random.shuffle(names)
    msgs = []
    for i in range(len(names)):
        gives = getNameIdByName(names[i], group_name)
        receiver = names[(i + 1) % len(names)]
        wish_list = getWishListByName(receiver, group_name)
        send = "Вітаю🎄 ти дариш: " + receiver + "\nСписок побажань:" + wish_list
        try:
            msgs.append(bot.send_message(gives, send))
        except ApiTelegramException:
            bot.send_message(getOrganizerGroup(group_name), f"{names[i]} заблокував бота, ви не можете продовжити!")
            for msg in msgs:
                bot.delete_message(msg.chat.id, msg.id)
            return
    deleteRecordsByGroupName(group_name)


try:
    bot.infinity_polling()
except KeyboardInterrupt:
    close_db()
    exit()
