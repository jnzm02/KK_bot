from telebot.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

import juz


def start_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(
        KeyboardButton("Read Quran"),
        KeyboardButton("Deadline"),
        KeyboardButton('Show List')
    )

    return keyboard


def read_quran_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(
        KeyboardButton("free juz"),
        KeyboardButton("my list"),
        KeyboardButton("add juz"),
        KeyboardButton("done juz"),
        KeyboardButton("drop juz"),
    )

    return keyboard


def deadline_keyboard():
    temp_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    temp_keyboard.add(
        KeyboardButton('Set Deadline'),
        KeyboardButton('Extend Deadline'),
        KeyboardButton('Remove Deadline'),
        KeyboardButton('Show Deadline'),
    )

    return temp_keyboard


def add_juz_keyboard():
    return generate_juz_keyboard(juz.free_juz())


def drop_juz_keyboard(user_id):
    return generate_juz_keyboard(juz.get_my_list(user_id))


def done_juz_keyboard(user_id):
    return generate_juz_keyboard(juz.get_my_list(user_id))


def generate_juz_keyboard(my_list):
    temp_keyboard = InlineKeyboardMarkup(row_width=3)
    for number in range(len(my_list)):
        if number % 3 == 2:
            temp_keyboard.add(
                InlineKeyboardButton(my_list[number - 2], callback_data='cb_free_juz_' + my_list[number - 2]),
                InlineKeyboardButton(my_list[number - 1], callback_data='cb_free_juz_' + my_list[number - 1]),
                InlineKeyboardButton(my_list[number], callback_data='cb_free_juz_' + my_list[number]),
            )
    if len(my_list) % 3 == 2:
        temp_keyboard.add(
            InlineKeyboardButton(my_list[len(my_list) - 2], callback_data='cb_free_juz_' + my_list[len(my_list) - 2]),
            InlineKeyboardButton(my_list[len(my_list) - 1], callback_data='cb_free_juz_' + my_list[len(my_list) - 1])
        )
    if len(my_list) % 3 == 1:
        temp_keyboard.add(
            InlineKeyboardButton(my_list[len(my_list) - 1], callback_data='cb_free_juz_' + my_list[len(my_list) - 1])
        )

    return temp_keyboard
