from telebot.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

import dbhelper


def start_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(
        KeyboardButton("Read Quran"),
        KeyboardButton("Deadline"),
        KeyboardButton('Show List')
    )

    return keyboard


def start_user_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(
        KeyboardButton("Read Quran"),
        KeyboardButton("Show Deadline"),
        KeyboardButton("Show List"),
    )


def read_quran_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(
        KeyboardButton("free juz"),
        KeyboardButton("my list"),
        KeyboardButton("add juz"),
        KeyboardButton("done juz"),
        KeyboardButton("drop juz"),
        KeyboardButton("◀Back"),
    )

    return keyboard


def deadline_keyboard():
    temp_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    temp_keyboard.add(
        KeyboardButton('Set Deadline'),
        KeyboardButton('Extend Deadline'),
        KeyboardButton('Remove Deadline'),
        KeyboardButton('Show Deadline'),
        KeyboardButton("◀Back")
    )
    return temp_keyboard


def extend_deadline_keyboard():
    temp_keyboard = InlineKeyboardMarkup(row_width=2)
    temp_keyboard.add(
        InlineKeyboardButton('1 day', callback_data='deadline.extend_deadline.1'),
        InlineKeyboardButton('2 days', callback_data='deadline.extend_deadline.2'),
        InlineKeyboardButton('1 week', callback_data='deadline.extend_deadline.7'),
        InlineKeyboardButton('2 weeks', callback_data='deadline.extend_deadline.14'),
    )
    return temp_keyboard


def add_juz_keyboard():
    return generate_juz_keyboard(dbhelper.free_juz(), 'add')


def drop_juz_keyboard(username):
    return generate_juz_keyboard(dbhelper.generate_my_list(username), 'drop')


def done_juz_keyboard(username):
    return generate_juz_keyboard(dbhelper.generate_my_list(username), 'done')


def generate_juz_keyboard(my_list, task):
    temp_keyboard = InlineKeyboardMarkup(row_width=3)
    for number in range(len(my_list)):
        if number % 3 == 2:
            temp_keyboard.add(
                InlineKeyboardButton(my_list[number-2],
                                     callback_data='juz'+'.'+task+'.'+my_list[number-2]),
                InlineKeyboardButton(my_list[number-1],
                                     callback_data='juz'+'.'+task+'.'+my_list[number-1]),
                InlineKeyboardButton(my_list[number],
                                     callback_data='juz'+'.'+task+'.'+my_list[number]),
            )
    if len(my_list) % 3 == 2:
        temp_keyboard.add(
            InlineKeyboardButton(my_list[len(my_list)-2],
                                 callback_data='juz'+'.'+task+'.'+my_list[len(my_list)-2]),
            InlineKeyboardButton(my_list[len(my_list)-1],
                                 callback_data='juz'+'.'+task+'.'+my_list[len(my_list)-1])
        )
    if len(my_list) % 3 == 1:
        temp_keyboard.add(
            InlineKeyboardButton(my_list[len(my_list)-1],
                                 callback_data='juz'+'.'+task+'.'+my_list[len(my_list)-1])
        )

    return temp_keyboard
