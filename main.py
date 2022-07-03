import os

import pytz
import telebot
import datetime

from decouple import config
from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.asyncio import AsyncIOScheduler

# local
import admins
import juz
import tools

API_KEY = config('API_KEY')
general_chat_id = config('KK_bot_hatym_bot_test_chat')
SUPER_ADMIN_ID = int(config('SUPER_ADMIN_ID'))

bot = telebot.TeleBot(API_KEY)

deadline = '01.07.2022'


def send_evening_notification():
    message_text = "Today's Updates for Quran Hatim: " + str(deadline) + '\n'
    message_text += juz.show_all()
    bot.send_message(general_chat_id, message_text)


# scheduler = BlockingScheduler(timezone=pytz.timezone('Asia/Almaty'))
# scheduler.add_job(send_evening_notification, trigger='cron', hour=18, minute=27)
# scheduler.start()


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
        bot.send_message(message.chat.id, "Your list is empty")
    else:
        bot.send_message(message.chat.id, "Your list:\n" + my_list)


@bot.message_handler(commands=['set_deadline'])
def set_deadline_command(message):

    if not admins.check_admin(message.from_user.id):
        bot.send_message(message.chat.id, "You are not admin")
        return

    data = tools.extract_arg(message.text)
    date = data[0]
    deadline = datetime.datetime.strptime(date, "%d/%m/%Y").date()
    today = datetime.date.today()
    days = deadline - today

    bot.send_message(message.chat.id, "Successfully set deadline\nDays before deadline: "+str(days)+'\nDeadline : '+str(deadline))


@bot.message_handler(commands=['add'])
def add_to_mylist(message):
    data = tools.extract_arg(message.text)

    if not tools.check_has_arg(data):
        bot.send_message(message.chat.id, "Can not add an empty argument. Please enter a number "
                                          "between [1, 30] after command")
        return

    juz_number = data[0]

    if not juz_number.isdigit():
        bot.send_message(message.chat.id, "Please write a number, you sent wrong parameters. Please enter a number "
                                          "between [1, 30] after command")
        return

    juz_number = int(juz_number)

    if juz_number > 30 or juz_number <= 0:
        bot.send_message(message.chat.id, "No juz found! May be you sent wrong parameters. Please enter a number "
                                          "between [1, 30] after command")
        return

    if juz.check_read(juz_number):
        bot.send_message(message.chat.id, "This juz is already read!")
        return

    if juz.check_mine(juz_number, message.from_user.username):
        bot.send_message(message.chat.id, "This juz is already yours")
        return

    if not juz.check_free(juz_number):
        bot.send_message(message.chat.id, "This juz is taken by other user!")
        return

    juz.add_user(juz_number, message.from_user.username)
    bot.send_message(message.chat.id, "Juz has added to your list\nPlease finish reading till the deadline")


@bot.message_handler(commands=['all'])
def show_all_juz(message):
    message_text = juz.show_all()
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=['done'])
def done_reading_juz(message):
    data = tools.extract_arg(message.text)

    if not tools.check_has_arg(data):
        bot.send_message(message.chat.id, "Can not assign as done. Please enter a number "
                                          "between [1, 30] after command")
        return

    juz_number = data[0]

    if not juz_number.isdigit():
        bot.send_message(message.chat.id, "Please write a number, you sent wrong parameters. Please enter a number "
                                          "between [1, 30] after command")
        return

    juz_number = int(juz_number)

    if juz_number > 30 or juz_number <= 0:
        bot.send_message(message.chat.id, "No juz found!")
        return

    if juz.check_read(juz_number):
        bot.send_message(message.chat.id, "This juz is already read!")
        return

    if not juz.check_mine(juz_number, message.from_user.username):
        bot.send_message(message.chat.id, "This juz is not yours")
        return

    else:
        juz.done_reading(juz_number)
        bot.send_message(message.chat.id, "Congrats keep going! May Allah bless your efforts!")


@bot.message_handler(commands=["drop"])
def drop_user(message):
    data = tools.extract_arg(message.text)

    if not tools.check_has_arg(data):
        bot.send_message(message.chat.id, "Can not drop. Please enter a number between [1, 30] after command")
        return

    juz_number = data[0]

    if not juz_number.isdigit():
        bot.send_message(message.chat.id, "Please write a number, you sent wrong parameters. Please enter a number "
                                          "between [1, 30] after command")
        return

    juz_number = int(juz_number)

    if juz_number > 30 or juz_number <= 0:
        bot.send_message(message.chat.id, "No juz found!")
        return

    if not juz.check_mine(juz_number, message.from_user.username):
        bot.send_message(message.chat.id, "You can't drop this juz cause it is not yours")
        return

    if juz.check_read(juz_number):
        bot.send_message(message.chat.id, "You can't drop the juz you have already read!")
        return

    juz.drop_user(juz_number)

    bot.send_message(SUPER_ADMIN_ID, str(message.from_user.username) + ' has dropped ' + str(juz_number) + ' juz')
    bot.send_message(message.chat.id, "Successfully dropped the juz")


@bot.message_handler(commands=['set_main_chat'])
def set_main_chat(message):
    if not message.from_user.id == SUPER_ADMIN_ID:
        bot.send_message(message.chat.id, "You are not allowed to call this command")
        return

    general_chat_id = message.chat.id
    bot.send_message(message.chat.id, "Successfully set this chat as a general chat!")


@bot.message_handler(commands=['super_admin_status'])
def super_admin_status_command(message):
    if admins.check_super_admin(message.from_user.id):
        bot.send_message(message.chat.id, "Yes you are super admin")
    else:
        bot.send_message(message.chat.id, "No you are not super admin")


@bot.message_handler(commands=['check_chat'])
def check_chat_command(message):
    if not admins.check_admin(message.from_user.id):
        bot.send_message(message.chat.id, "You are not allowed to call this command")
        return

    bot.send_message(general_chat_id, "This is a general chat")


@bot.message_handler(commands=['request_to_become_admin'])
def request_to_admin_command(message):
    if admins.exists_in_black_list(message.from_user.id):
        bot.send_message(message.chat.id, "You are in black list. Contact SuperAdmin")
        return

    if admins.exists_in_admin_list(message.from_user.id):
        bot.send_message(message.chat.id, "You are already an admin")
        return

    if admins.exists_in_waiting_list(message.from_user.id):
        bot.send_message(message.chat.id, "You have already sent the request. "
                                          "Wait till Super Admin answers or Contact him yourself")
        return

    bot.send_message(SUPER_ADMIN_ID,
                     "User " + str(message.from_user.username) + " with id: '" + str(message.from_user.id) + \
                     "' wants to become admin use /approve command to approve " \
                     "the user or /add_to_black_list if you want to add the user " \
                     "to black list")


@bot.message_handler(commands=['approve_admin'])
def approve_user(message):
    data = tools.extract_arg(message.text)
    user_id = data[0]

    if not admins.check_super_admin(message.from_user.id):
        bot.send_message(message.chat.id, "You are not allowed to call this command")
        return

    if admins.check_admin(user_id):
        bot.send_message(message.chat.id, "This user is already an admin")
        return

    admins.approve_admin(user_id)
    bot.send_message(message.chat.id, "Admin approved")
    bot.send_message(user_id, "Hello, SuperAdmin approved you so from now you are an admin. Chat for admins: "
                              "https://t.me/+UtEqHFZ0KoIzNGQy")


@bot.message_handler(commands=['remove'])
def remove_admin(message):
    data = tools.extract_arg(message.text)
    user_id = data[0]

    if not admins.check_super_admin(message.from_user.id):
        bot.send_message(message.chat.id, "You are not allowed for this command")
        return

    if admins.check_super_admin(user_id):
        bot.send_message(message.chat.id, "You cant remove Super Admin")
        return

    if not admins.exists_in_admin_list(user_id):
        bot.send_message(message.chat.id, "This is user is not Admin")
        return

    admins.remove_admin(user_id)
    bot.send_message(message.chat.id, "Successfully removed user from admin list")


@bot.message_handler(commands=['admins'])
def admins_list_command(message):
    if not admins.check_super_admin(message.from_user.id):
        bot.send_message(message.chat.id, "You are not Super Admin")
        return

    bot.send_message(message.chat.id, admins.all_admins())


@bot.message_handler(commands=['admin_status'])
def check_if_admin_command(message):
    if admins.check_admin(message.from_user.id):
        bot.send_message(message.chat.id, "You are admin")
    else:
        bot.send_message(message.chat.id, "You are not admin")


@bot.message_handler(commands=['waiting_list'])
def show_waiting_list_command(message):
    if not admins.check_super_admin(message.from_user.id):
        bot.send_message(message.chat.id, "You are not allowed to call this command")
        return

    bot.send_message(message.chat.id, admins.show_waiting_list())


@bot.message_handler(commands=['black_list'])
def show_black_list(message):
    if not admins.check_super_admin(message.from_user.id):
        bot.send_message(message.chat.id, "You are not allowed to call this command")
        return

    bot.send_message(message.chat.id, admins.show_black_list())


bot.polling()
