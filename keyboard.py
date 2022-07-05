from telebot.types import ReplyKeyboardMarkup, KeyboardButton


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
