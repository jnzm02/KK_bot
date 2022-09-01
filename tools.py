import dbhelper


def extract_arg(arg):
    return arg.split()[1:]


def check_has_arg(arg) -> bool:
    return not len(arg) == 0


def concatenate_arg(arg) -> str:
    message_text = ""
    for word in arg:
        message_text += word
        message_text += ' '
    message_text += '\n'

    return message_text


def show_free_juz_list(temp_list) -> str:
    if len(temp_list) == 0:
        return "List is empty"
    the_list = "*"  # star char makes text bold in telegram
    for juz_number in temp_list:
        the_list += str(juz_number) + ' '
    return the_list + '*'


def show_list(temp_list) -> str:
    if len(temp_list) == 0:
        return "List is empty"
    the_list = ""
    for item in temp_list:
        the_list += str(item) + '\n'
    return the_list


def split_callback_data(data):
    words = data.split('.')
    return words


def get_juz(cursor) -> list:
    temp_list = []
    for juz in cursor:
        if juz[2]:
            temp_list.append(str(juz[0]) + '✅')
        else:
            temp_list.append(str(juz[0]))

    return temp_list


def show_all():
    db_juz = dbhelper.show_all()
    sorted(db_juz)
    my_list = []
    for juz in db_juz:
        user = juz[3]
        if juz[3] == 'NULL_USER':
            user = ''
        if juz[2]:
            my_list.append("◦ " + str(juz[0]) + ": " + user + ' ✅')
        else:
            if str(user) != "":
                my_list.append("◦ " + str(juz[0]) + ": " + user + ' ⏳')
            else:
                my_list.append("◦ " + str(juz[0]) + ": " + user)
    return show_list(my_list)


def check_super_admin(user_id, super_admin_id) -> bool:
    return str(user_id) == str(super_admin_id)
