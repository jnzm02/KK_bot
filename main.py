import os
import telebot

from decouple import config

# local
import juz
import tools

API_KEY = config('API_KEY')

bot = telebot.TeleBot(API_KEY)


# deadline = date


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Hello, I am a bot which monitor the process of Quran Hatim!')


@bot.message_handler(commands=['free_juz'])
def show_free_juz_command(message):
    free_juz_list = juz.free_juz_list()

    bot.send_message(message.chat.id, "The list of free juz:\n" + free_juz_list)


@bot.message_handler(commands=['my_list'])
def get_my_list_command(message):
    my_list = juz.get_my_list(message.from_user.username)
    if my_list == "":
        message_text = "Your list is empty"
    else:
        message_text = "Your list:\n" + my_list

    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=['add'])
def add_to_mylist(message):
    juz_number = tools.extract_arg(message.text)[0]

    if not juz_number.isdigit():
        bot.send_message(message.chat.id, "Please write a number, you sent wrong parameters")
        return

    juz_number = int(juz_number)

    if juz_number > 30 or juz_number <= 0:
        bot.send_message(message.chat.id, "No juz found! May be you sent wrong parameters")
        return

    # if juz_number == "":
    #
    #     bot.send_message(message.chat.id, "Which juz you want to read?")
    #
    #     @bot.message_handler(content_types=['text'])
    #     def assigning_juz_for_user(new_message):

    # TODO: asks which juz user wants to take
    # TODO: then user sends message which we take as juz_number, then work with this text
    # bot.send_message(message.chat.id, "YES")

    # if free_juz.free_juz_dict[juz_number] is None:
    juz.add_user(juz_number, message.from_user.username)
    message_text = "Juz has added to your list\nPlease finish reading till the deadline"
    # else:
    # message_text = "This juz is already taken!"

    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=['all'])
def show_all_juz(message):
    message_text = juz.show_all()
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=['done'])
def done_reading_juz(message):
    juz_number = int(tools.extract_arg(message.text)[0])
    if juz_number > 30:
        bot.send_message(message.chat.id, "No juz found!")
        return

    if juz.check_read(juz_number):
        bot.send_message(message.chat.id, "This juz is already read!")
        return

    elif not juz.check_if_mine(juz_number, message.from_user.username):
        bot.send_message(message.chat.id, "This juz is not yours")
        return

    else:
        juz.done_reading(juz_number)
        bot.send_message(message.chat.id, "Congrats keep going! May Allah bless your efforts!")


bot.polling()
