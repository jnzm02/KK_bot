import tools
import dbhelper


def start_command() -> str:
    return "Ассаламу Алейкум, Командаға сәлем! Бұл бот Құран оқу процесін бақылау үшін жасалған 📖 "


def completed_hatym() -> str:
    return "Congrats, we have finished reading our hatym. Thanks for everyone who engaged in this. May Allah bless " \
           "your efforts 😇 "


# The list of free juz:
# 1 2 3 4 5 7 8 9 10 13 14 15 16 18 19 20 21 24 28
def free_juz_list() -> str:
    return "The list of free juzs:\n" + tools.show_free_juz_list(dbhelper.free_juz())


def juz_successfully_added_to_your_list() -> str:
    return "Juz has been added to your list\nPlease finish reading till the deadline"


def juz_is_not_yours() -> str:
    return "This juz is not yours"


def warning_add_my_juz() -> str:
    return "This juz is already yours"


def warning_add_others_juz() -> str:
    return "This juz is already taken!"


def juz_is_read() -> str:
    return "This juz is already read!"


def done_reading() -> str:
    return "Congrats keep going! May Allah bless your efforts!  😇"


def warning_drop_others_juz() -> str:
    return "You can't drop this juz because it is not yours"


def warning_drop_read_juz() -> str:
    return "You can't drop the juz you have already read!"


def success_drop_juz() -> str:
    return "Successfully dropped the juz ✅"


def not_allowed_to_call() -> str:
    return "You are not allowed to call this command, please contact with admins!"


def message_after_read_quran_button() -> str:
    return "Choose which action you want to perform"


def message_after_deadline_button() -> str:
    return "Choose which action you want to perform"


def message_after_add_juz_button() -> str:
    return "Choose which action you want to perform"


def message_after_drop_juz_button() -> str:
    return "Choose which juz you want to drop"


def warning_drop_empty_list() -> str:
    return "Your list is empty, firstly you should add the juz to your list"


def message_after_done_juz_button() -> str:
    return "Choose which juz you have finished reading"


def warning_done_empty_list() -> str:
    return "Your list is empty, firstly you should add the juz to your list"
