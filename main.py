import telebot
import datetime
from decouple import config

# local
import deadline
import tools
import keyboard
import dbhelper
import messages
import juz

API_KEY = config('API_KEY')
bot = telebot.TeleBot(API_KEY)


SUPER_ADMIN_ID = int(config('SUPER_ADMIN_ID'))


@bot.message_handler(commands=['start'])
def start_command(message):
    dbhelper.add_new_user(message.from_user)
    # dbhelper.upd_new_user(message.from_user.id, message.from_user.username)
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, messages.start_command(), reply_markup=keyboard.start_keyboard())


@bot.message_handler(commands=['number_of_users'])
def get_number_of_users(message):
    if not dbhelper.check_admin(message.from_user.id):
        return

    bot.send_message(message.chat.id, "Current number of users is: " + str(dbhelper.number_of_users()))


@bot.message_handler(commands=['completed_hatm'])
def completed_hatm_command(message):
    if not dbhelper.check_admin(message.from_user.id):
        return

    dbhelper.completed_hatym()
    dbhelper.clean_all()
    dbhelper.set_default_deadline()
    bot.send_message(dbhelper.get_general_chat_id(), messages.completed_hatym())


@bot.message_handler(commands=['clear_all'])
def clean_all(message):
    if not dbhelper.check_admin(message.from_user.id):
        return

    dbhelper.clean_all()
    bot.send_message(message.chat.id, "Clean all juz")


@bot.message_handler(commands=['free_juz'])
def show_free_juz_command(message):
    if message.chat.type != 'private' and not dbhelper.check_admin(message.from_user.id):
        return

    bot.send_message(message.chat.id, messages.free_juz_list(), parse_mode='Markdown')


@bot.message_handler(commands=['my_list'])
def my_list_command(message):
    if message.chat.type != 'private' and not dbhelper.check_admin(message.from_user.id):
        return

    my_list = dbhelper.generate_my_list(message.from_user)
    if len(my_list) > 0:
        bot.send_message(message.chat.id, "Your list:\n" + tools.show_list(my_list))
    else:
        bot.send_message(message.chat.id, "Your list is empty")


@bot.message_handler(commands=['set_deadline'])
def set_deadline_command(message):
    if not dbhelper.check_admin(message.from_user.id):
        return

    data = tools.extract_arg(message.text)

    if len(data) < 3:
        bot.send_message(message.chat.id, 'Please Enter 3 fields for day month and year respectively')
        return

    day, month, year = data[0], data[1], data[2]
    if not deadline.check_date(day, month, year):
        bot.send_message(message.chat.id, "You entered incorrect date, Please enter a correct one")

    dbhelper.set_deadline(day, month, year)

    if deadline.till_deadline() < 0:
        bot.send_message(message.chat.id, "This date is already past, please choose an another date")
        dbhelper.set_default_deadline()
        return

    bot.send_message(message.chat.id,
                     "Successfully set deadline\nDays before deadline: " + str(deadline.till_deadline()) +
                     '\nDeadline : ' + str(deadline.get_deadline()), reply_markup=keyboard.deadline_keyboard())


@bot.message_handler(commands=['users_list'])
def users_list_command(message):
    if not dbhelper.check_admin(message.from_user.id):
        bot.send_message(message.chat.id, messages.not_allowed_to_call())
        return

    message_text = tools.generate_users_list(dbhelper.users_list())
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=['progress', 'show_progress'])
def show_progress_command(message):
    if not dbhelper.check_admin(message.from_user.id):
        bot.send_message(message.chat.id, messages.not_allowed_to_call())
        return

    progress = dbhelper.get_progress()
    if len(progress) < 1:
        bot.send_message(message.chat.id, "The progress is empty")
        return

    message_text = tools.generate_progress(progress)

    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=['send_progress'])
def send_progress_command(message):
    if not dbhelper.check_admin(message.from_user.id):
        bot.send_message(message.chat.id, messages.not_allowed_to_call())
        return

    progress = dbhelper.get_progress()
    # dbhelper.clear_progress()
    bot.send_message(dbhelper.get_general_chat_id(), progress)
    bot.send_message(message.chat.id, "All the progress was sent to the general chat and was cleared from database")


@bot.message_handler(commands=['clear_progress'])
def clear_progress(message):
    if str(SUPER_ADMIN_ID) != str(message.from_user.id):
        return

    progress = dbhelper.get_progress()
    dbhelper.clear_progress()
    if len(progress) < 1:
        bot.send_message(message.chat.id, "progress is empty!")
        return

    bot.send_message(message.chat.id, "Successfully deleted all progress from database")


@bot.message_handler(commands=['extend_deadline'])
def extend_deadline_command(message):
    if not dbhelper.check_admin(message.from_user.id):
        return

    data = tools.extract_arg(message.text)

    if not tools.check_has_arg(data):
        bot.send_message(message.chat.id, "Can't extend deadline with empty number of days. Please, Enter a number of "
                                          "days so that we can extend the deadline")
        return

    number_of_days = data[0]

    if not number_of_days.isdigit():
        bot.send_message(message.chat.id, "Please Enter a number after command, seems you sent invalid argument")
        return

    number_of_days = int(number_of_days)
    deadline.extend_deadline(number_of_days)
    bot.send_message(message.chat.id, "Deadline extended for " + str(number_of_days) + " days\n" +
                     "New deadline is " + str(deadline.get_deadline()))


@bot.message_handler(commands=['remove_deadline'])
def remove_deadline_command(message):
    if not dbhelper.check_admin(message.from_user.id):
        return

    dbhelper.set_default_deadline()
    bot.send_message(message.chat.id, "Successfully removed deadline")


@bot.message_handler(commands=['deadline_past'])
def deadline_past_command(message):
    if not dbhelper.check_admin(message.from_user.id):
        return

    users_list = dbhelper.take_late_people()
    if len(users_list) < 1:
        bot.send_message(message.chat.id, "Congrats!!! All readers ended their juzs!")
        return

    message_text = "LATE USERS LIST FOR THIS HATYM:\n"
    for user in users_list:
        message_text += user
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=['check_deadline'])
def check_deadline_command(message):
    if message.chat.type != 'private' and not dbhelper.check_admin(message.from_user.id):
        return

    if not deadline.check_deadline():
        bot.send_message(message.chat.id, "The deadline does not exist")
        return

    bot.send_message(message.chat.id, "The deadline is: " + str(deadline.get_deadline()))


@bot.message_handler(commands=['all'])
def show_all_juz(message):
    if message.chat.type != 'private' and not dbhelper.check_admin(message.from_user.id):
        return

    message_text = tools.show_all()
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=['warn_not_finished'])
def warn_not_finished(message):
    if not dbhelper.check_admin(message.from_user.id):
        return

    data = tools.extract_arg(message.text)
    if len(data) == 0:
        data = ""

    message_text = tools.concatenate_arg(data)
    temp_list = tools.show_list(dbhelper.get_not_finished_users())
    if temp_list == "List is empty":
        bot.send_message(message.chat.id, "Hatym is finished!")
        return

    message_text += temp_list
    bot.send_message(dbhelper.get_general_chat_id(), message_text)


@bot.message_handler(commands=['super_admin_status'])
def super_admin_status_command(message):
    if message.chat.type != 'private':
        return

    if tools.check_super_admin(message.from_user.id, SUPER_ADMIN_ID):
        bot.send_message(message.chat.id, "Yes you are super admin")
    else:
        bot.send_message(message.chat.id, "No you are not super admin")


@bot.message_handler(commands=['set_general_chat'])
def set_general_chat(message):
    if not dbhelper.check_admin(message.from_user.id):
        return

    if message.chat.type != 'group':
        return

    if str(message.from_user.id) != str(SUPER_ADMIN_ID):
        bot.send_message(message.chat.id, "You are not allowed to call this command!")
        return

    dbhelper.set_general_chat(message.chat.id)
    bot.send_message(message.chat.id, "Successfully set main chat" + str(message.chat.title))


@bot.message_handler(commands=['check_chat'])
def check_chat_command(message):
    if message.chat.type != 'group':
        return

    if not dbhelper.check_admin(message.from_user.id):
        return

    if dbhelper.get_general_chat_id() == message.chat.id:
        bot.send_message(message.chat.id, "This is a general chat")
    else:
        bot.send_message(message.chat.id, "This is not a general chat")


@bot.message_handler(commands=['set_admin'])
def set_admin_command(message):
    if not str(message.from_user.id) == str(SUPER_ADMIN_ID):
        bot.send_message(message.chat.id, messages.not_allowed_to_call())
        return

    user_id = tools.extract_arg(message.text)
    dbhelper.set_admin(user_id[0])
    bot.send_message(message.chat.id, "The user was added to the admins list you can check it using command '/admins'")


@bot.message_handler(commands=['admins'])
def admins_list_command(message):
    if not dbhelper.check_admin(message.from_user.id):
        return

    bot.send_message(message.chat.id, tools.show_list(dbhelper.all_admins()))


@bot.message_handler(commands=['status'])
def status_command(message):
    if message.chat.type != 'private' and not dbhelper.check_admin(message.from_user.id):
        return
    message_text = '#hatm' + str(dbhelper.get_hatym_number()) + '\n\n'
    if deadline.check_deadline():
        message_text += str(deadline.get_deadline()) + '\n\n'
    message_text += tools.show_all()
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=['admin_status'])
def check_if_admin_command(message):
    if message.chat.type != 'private':
        return

    if dbhelper.check_admin(message.from_user.id):
        bot.send_message(message.chat.id, "You are admin")
    else:
        bot.send_message(message.chat.id, "You are not admin")


def callback_juz(call, task, action):
    if task == 'add':
        if action.endswith('✅'):
            bot.send_message(call.from_user.id, messages.juz_is_read())
            return

        juz_number = int(action)
        juz_data = dbhelper.get_juz_data(juz_number)
        if juz.check_read(juz_data):
            bot.send_message(call.from_user.id, messages.juz_is_read())
            return

        if juz.check_mine(juz_data, call.from_user):
            bot.send_message(call.from_user.id, messages.warning_add_my_juz())
            return

        if juz.check_free(juz_data):
            bot.send_message(call.from_user.id, messages.warning_add_others_juz())
            return

        dbhelper.add_juz(juz_number, call.from_user)
        # dbhelper.add_text(call.from_user.username + " added juz " + str(juz_number) + '😇')
        bot.send_message(call.from_user.id, messages.juz_successfully_added_to_your_list())

    elif task == 'done':
        if action.endswith('✅'):
            bot.send_message(call.from_user.id, messages.juz_is_read())
            return

        juz_number = int(action)
        dbhelper.done_reading(juz_number)
        # dbhelper.add_text(call.from_user.username + " done reading juz " + action + '🥳')
        bot.send_message(call.from_user.id, messages.done_reading())

    elif task == 'drop':
        if action.endswith('✅'):
            bot.send_message(call.from_user.id, messages.warning_drop_read_juz())
            return

        juz_number = int(action)
        dbhelper.drop_user(juz_number)
        # dbhelper.add_text(call.from_user.username + " dropped juz " + action + '😔')
        bot.send_message(call.from_user.id, messages.success_drop_juz())
        bot.send_message(SUPER_ADMIN_ID, 'The user ' + str(call.from_user.username) + ' dropped the juz ' + action)


def callback_deadline(call, task, action):
    if task == 'extend_deadline':
        if dbhelper.check_admin(call.from_user):
            deadline.extend_deadline(int(action))
            bot.send_message(call.from_user.id, "Deadline is extended for " + action + ' days')
        else:
            bot.send_message(call.from_user.id, messages.not_allowed_to_call())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    words = tools.split_callback_data(call.data)
    field = words[0]
    task = words[1]
    action = words[2]
    if field == 'juz':
        callback_juz(call, task, action)

    if field == 'deadline':
        callback_deadline(call, task, action)


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    if not message.chat.type == 'private' and not dbhelper.check_admin(message.from_user.id):
        return

    # Buttons to Buttons
    if message.text == 'Read Quran📖':
        bot.send_message(message.chat.id, messages.message_after_read_quran_button(),
                         reply_markup=keyboard.read_quran_keyboard())

    elif message.text == 'Deadline⏰':
        bot.send_message(message.chat.id, messages.message_after_deadline_button(),
                         reply_markup=keyboard.deadline_keyboard())

    # Buttons to info

    elif message.text == 'free juzs':
        show_free_juz_command(message)

    elif message.text == 'my list':
        my_list_command(message)

    # Buttons to  InlineKeyboard

    elif message.text == 'add juz':
        bot.send_message(message.chat.id, messages.message_after_add_juz_button(),
                         reply_markup=keyboard.add_juz_keyboard())

    elif message.text == 'drop juz':
        if len(dbhelper.generate_my_list(message.from_user)) > 0:
            bot.send_message(message.chat.id, messages.message_after_drop_juz_button(),
                             reply_markup=keyboard.drop_juz_keyboard(message.from_user))
        else:
            bot.send_message(message.chat.id, messages.warning_drop_empty_list())

    elif message.text == 'done juz':
        if len(dbhelper.generate_my_list(message.from_user)) > 0:
            bot.send_message(message.chat.id, messages.message_after_done_juz_button(),
                             reply_markup=keyboard.done_juz_keyboard(message.from_user))
        else:
            bot.send_message(message.chat.id, messages.warning_done_empty_list())

    elif message.text == 'Show List📕':
        message_text = '#hatm' + str(dbhelper.get_hatym_number()) + '\n\n'
        if deadline.check_deadline():
            message_text += str(deadline.get_deadline()) + '\n\n'
        message_text += tools.show_all_without_done_status()
        bot.send_message(message.chat.id, message_text)

    elif message.text == 'Show Deadline':
        if not deadline.check_deadline():
            bot.send_message(message.chat.id, "You did not set deadline")
        else:
            bot.send_message(message.chat.id, deadline.get_deadline(), reply_markup=keyboard.deadline_keyboard())

    elif message.text == 'Extend Deadline':
        if not dbhelper.check_admin(message.from_user.id):
            if message.chat.type == 'private':
                bot.send_message(message.chat.id, messages.not_allowed_to_call())
            return

        if not deadline.check_deadline():
            bot.send_message(message.chat.id, "You did not set deadline")
        else:
            bot.send_message(message.chat.id, "Extend Deadline",
                             reply_markup=keyboard.extend_deadline_keyboard())

    elif message.text == "◀Back":
        start_command(message)

    elif message.text == 'Set Deadline':
        if not dbhelper.check_admin(message.from_user.id):
            if message.chat.type == 'private':
                bot.send_message(message.chat.id, messages.not_allowed_to_call())
            return

        message_text = 'SUPER admin did not finished this part. You can use /set_deadline command instead. For ' \
                       'example </set_deadline ' + str(datetime.date.today().day) + ' ' + str(
            datetime.date.today().month) + ' ' + str(datetime.date.today().year) + '>'
        bot.send_message(message.chat.id, message_text)

    elif message.text == 'Remove Deadline':
        if not dbhelper.check_admin(message.from_user.id):
            if message.chat.type == 'private':
                bot.send_message(message.chat.id, messages.not_allowed_to_call())
            return

        if not deadline.check_deadline():
            bot.send_message(message.chat.id, "You did not set deadline")
        else:
            dbhelper.set_default_deadline()
            bot.send_message(message.chat.id, "Successfully Removed the Deadline",
                             reply_markup=keyboard.deadline_keyboard())


bot.polling(none_stop=True)
