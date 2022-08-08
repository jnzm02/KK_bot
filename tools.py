import dbhelper


def extract_arg(arg):
    return arg.split()[1:]


def check_has_arg(arg):
    return not len(arg) == 0


def show_list(my_list):
    if len(my_list) == 0:
        return "List is empty"
    the_list = ""
    for item in my_list:
        the_list += str(item) + '\n'
    return the_list


def split_callback_data(data):
    words = data.split('.')
    return words


def get_juz(cursor) -> list:
    temp_list = []
    for juz in cursor:
        if juz[2]:
            temp_list.append(str(juz[0])+'✅')
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
            my_list.append("◦ "+str(juz[0]) + ": " + user+'✅')
        else:
            my_list.append("◦ "+str(juz[0]) + ": " + user)
    return show_list(my_list)
