free_juz_dict = {}

for juz in range(1, 31):
    free_juz_dict[juz] = ["", False]


def make_empty():
    for is_free in free_juz_dict.values():
        is_free[0] = ""


def show_list(my_list):
    first = True
    the_list = ""
    for item in my_list:
        if not first:
            the_list += ', '
        the_list += str(item)
        first = False

    return the_list


def show():
    for juz_number, is_free in free_juz_dict.items():
        print(juz_number, is_free[0])


def show_all():
    my_list = []
    for juz_number, is_free in free_juz_dict.items():
        if is_free[1]:
            my_list.append(str(juz_number)+'✅')
        else:
            my_list.append(str(juz_number))

        return show_list(my_list)


def free_juz_list():
    my_list = []
    for juz_number, is_free in free_juz_dict.items():
        if len(is_free[0]) == 0:
            if is_free[1]:
                print("YES")
                my_list.append(str(str(juz_number)+'done'))
            else:
                print("NO")
                my_list.append(str(juz_number))

    return show_list(my_list)


def get_my_list(username):
    my_list = []
    for juz_number, name in free_juz_dict.items():
        if name[0] == username:
            if name[1]:
                my_list.append(str(juz_number)+'✅')
            else:
                my_list.append(str(juz_number))
    return show_list(my_list)


def done_reading(juz_number):
    free_juz_dict[juz_number][1] = True


def check_read(juz_number):
    if free_juz_dict[juz_number][1]:
        return True
    else:
        return False


def check_if_mine(juz_number, username):
    return free_juz_dict[juz_number][0] == username


def add_user(juz_number, username):
    free_juz_dict[juz_number][0] = str(username)
