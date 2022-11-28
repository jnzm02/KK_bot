

@bot.message_handler(commands=['send_evening_notification'])
def send_evening_notification_command(message):
    if not dbhelper.check_admin(message.from_user):
        return
    message_text = '#hatm' + str(dbhelper.get_hatym_number()) + '\n\n'
    if deadline.check_deadline():
        message_text += str(deadline.get_deadline()) + '\n\n'
    bot.send_message(dbhelper.get_general_chat_id(), message_text + tools.show_all())



@bot.message_handler(commands=['assign'])
def assign_juz(message):
    if not dbhelper.check_admin(message.from_user.id):
        return

    data = tools.extract_arg(message.text)

    try:
        user_id = data[0]
        juz_number = data[1]
        status = data[2]

        if not tools.valid_number(juz_number):
            return

        username = dbhelper.get_username(user_id)

        if status == 'add':
            dbhelper.add_juz_with_username(juz_number, user_id, username)

    except TypeError:
        bot.send_message(message.chat.id, "Error!")


#
# @bot.message_handler(commands=['add'])
# def add_to_mylist(message):
#     if message.chat.type != 'private' and not dbhelper.check_admin(message.from_user.id):
#         return
#
#     data = tools.extract_arg(message.text)
#
#     if not tools.check_has_arg(data):
#         bot.send_message(message.chat.id, "Can not add an empty argument. Please enter a number "
#                                           "between [1, 30] after command")
#         return
#
#     juz_number = data[0]
#
#     if not juz_number.isdigit():
#         bot.send_message(message.chat.id, "Please write a number, you sent wrong parameters. Please enter a number "
#                                           "between [1, 30] after command")
#         return
#
#     juz_number = int(juz_number)
#
#     if juz_number > 30 or juz_number <= 0:
#         bot.send_message(message.chat.id, "No juz found! May be you sent wrong parameters. Please enter a number "
#                                           "between [1, 30] after command")
#         return
#
#     juz_data = dbhelper.get_juz_data(juz_number)
#
#     if juz.check_read(juz_data):
#         bot.send_message(message.chat.id, messages.juz_is_read())
#         return
#
#     if juz.check_mine(juz_data, message.from_user):
#         bot.send_message(message.chat.id, messages.warning_add_my_juz())
#         return
#
#     if not juz.check_free(juz_data):
#         bot.send_message(message.chat.id, messages.warning_add_others_juz())
#         return
#
#     dbhelper.add_juz(juz_number, message.from_user)
#     bot.send_message(message.chat.id, messages.juz_successfully_added_to_your_list())



# @bot.message_handler(commands=['done'])
# def done_reading_juz(message):
#     if message.chat.type != 'private' and not dbhelper.check_admin(message.from_user.id):
#         return
#
#     data = tools.extract_arg(message.text)
#
#     if not tools.check_has_arg(data):
#         bot.send_message(message.chat.id, "Can not assign as done. Please enter a number "
#                                           "between [1, 30] after the command")
#         return
#
#     juz_number = data[0]
#
#     if not juz_number.isdigit():
#         bot.send_message(message.chat.id, "Please write a number, you sent wrong parameters. Please enter a number "
#                                           "between [1, 30] after the command")
#         return
#
#     juz_number = int(juz_number)
#     juz_data = dbhelper.get_juz_data(juz_number)
#     if juz_number > 30 or juz_number <= 0:
#         bot.send_message(message.chat.id, "No juz found!")
#         return
#
#     if juz.check_read(juz_data):
#         bot.send_message(message.chat.id, messages.juz_is_read())
#         return
#
#     if not juz.check_mine(juz_data, message.from_user):
#         bot.send_message(message.chat.id, messages.juz_is_not_yours())
#         return
#
#     else:
#         dbhelper.done_reading(juz_number)
#         bot.send_message(message.chat.id, messages.done_reading())


@bot.message_handler(commands=['warn_everyone'])
def warn_everyone_command(message):
    if str(SUPER_ADMIN_ID) != str(message.from_user.id):
        return

    message_text = tools.concatenate_arg(tools.extract_arg(message.text))
    if message_text == " ":
        bot.send_message(message.chat.id, "List is empty!")
        return
    user_id_list = dbhelper.user_id_list()
    bot.send_message(message.chat.id, str(user_id_list))


# @bot.message_handler(commands=["drop"])
# def drop_user(message):
#     if message.chat.type != 'private' and not dbhelper.check_admin(message.from_user.id):
#         return
#
#     data = tools.extract_arg(message.text)
#
#     if not tools.check_has_arg(data):
#         bot.send_message(message.chat.id, "Can not drop. Please enter a number between [1, 30] after command")
#         return
#
#     juz_number = data[0]
#
#     if not juz_number.isdigit():
#         bot.send_message(message.chat.id, "Please write a number, you sent wrong parameters. Please enter a number "
#                                           "between [1, 30] after command")
#         return
#
#     juz_number = int(juz_number)
#     juz_data = dbhelper.get_juz_data(juz_number)
#
#     if juz_number > 30 or juz_number <= 0:
#         bot.send_message(message.chat.id, "No juz found!")
#         return
#
#     if not juz.check_mine(juz_data, message.from_user):
#         bot.send_message(message.chat.id, messages.warning_drop_others_juz())
#         return
#
#     if juz.check_read(juz_data):
#         bot.send_message(message.chat.id, messages.warning_drop_read_juz())
#         return
#
#     dbhelper.drop_user(juz_number)
#
#     bot.send_message(SUPER_ADMIN_ID, str(message.from_user.username) + ' has dropped ' + str(juz_number) + ' juz')
#     bot.send_message(message.chat.id, messages.success_drop_juz())

