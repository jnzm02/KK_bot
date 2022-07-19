import tools

juz_dict = {}

for juz in range(1, 31):
    juz_dict[juz] = ["", False]


def make_empty():
    for is_free in juz_dict.values():
        is_free = ["", False]


def show_all():
    my_list = []
    for juz_number, is_free in juz_dict.items():
        if is_free[1]:
            my_list.append(str(str(juz_number) + ": " + str(is_free[0]) + '✅'))
        else:
            my_list.append(str(str(juz_number) + ": " + str(is_free[0])))

    return tools.show_list(my_list)


def free_juz_list():
    my_list = []
    for juz_number, is_free in juz_dict.items():
        if len(is_free[0]) == 0:
            if not is_free[1]:
                my_list.append(str(juz_number))

    return tools.show_list(my_list)


def generate_my_list(username):
    my_list = []
    for juz_number, name in juz_dict.items():
        if name[0] == username:
            if name[1]:
                my_list.append(str(juz_number) + '✅')
            else:
                my_list.append(str(juz_number))
    return my_list


def get_my_list(username):
    return tools.show_list(generate_my_list(username))


def done_reading(juz_number):
    juz_dict[juz_number][1] = True


def check_read(juz_number):
    if juz_dict[juz_number][1]:
        return True
    else:
        return False


def check_mine(juz_number, username):
    return juz_dict[juz_number][0] == username


def add_user(juz_number, username):
    juz_dict[juz_number][0] = str(username)


def drop_user(juz_number):
    juz_dict[juz_number] = ["", False]


def check_free(juz_number):
    return juz_dict[juz_number][0] == ""


def free_juz():
    my_list = []
    for juz_number, is_free in juz_dict.items():
        if len(is_free[0]) == 0:
            if not is_free[1]:
                my_list.append(str(juz_number))

    return my_list


def clean_all():
    for juz_number in range(1, 31):
        juz_dict[juz_number] = ["", False]


def generate_user_id_list():
    my_list = []
    for juz_number, is_free in juz_dict.items():
        if is_free[1]:
            my_list.append(is_free[0])
    print(my_list)
    return list(dict.fromkeys(my_list))
