juz_dict = {}

for juz in range(1, 31):
    juz_dict[juz] = ["", False]


def make_empty():
    for is_free in juz_dict.values():
        is_free = ["", False]


def show_list(my_list):
    # first = True
    # the_list = ""
    # for item in my_list:
    #     if not first:
    #         the_list += ', '
    #     the_list += str(item)
    #     first = False

    the_list = ""
    for item in my_list:
        the_list += item + '\n'

    return the_list


def show_all():
    my_list = []
    for juz_number, is_free in juz_dict.items():
        if is_free[1]:
            my_list.append(str(str(juz_number) + ": " + str(is_free[0]) + '✅'))
        else:
            my_list.append(str(str(juz_number) + ": " + str(is_free[0])))

    return show_list(my_list)


def free_juz_list():
    my_list = []
    for juz_number, is_free in juz_dict.items():
        if len(is_free[0]) == 0:
            if is_free[1]:
                my_list.append(str(str(juz_number) + 'done'))
            else:
                my_list.append(str(juz_number))

    return show_list(my_list)


def get_my_list(username):
    my_list = []
    for juz_number, name in juz_dict.items():
        if name[0] == username:
            if name[1]:
                my_list.append(str(juz_number) + '✅')
            else:
                my_list.append(str(juz_number))
    return show_list(my_list)


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
