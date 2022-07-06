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
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(
        KeyboardButton('Set Deadline'),
        KeyboardButton('Extend Deadline'),
        KeyboardButton('Remove Deadline'),
        KeyboardButton('Show Deadline'),
    )

    return keyboard


def add_juz_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=3)
    for number in juz.free_juz():
        keyboard.add(
                InlineKeyboardButton(number, callback_data='cb_free_juz_'+number),
        )

    return keyboard
