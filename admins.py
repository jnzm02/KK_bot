from decouple import config

# local
import tools

admins = []
waiting_list = []
black_list = []

SUPER_ADMIN_ID = config('SUPER_ADMIN_ID')

admins.append(SUPER_ADMIN_ID)


def check_super_admin(user_id):
    return str(user_id) == str(SUPER_ADMIN_ID)


def exists_in_admin_list(user_id):
    for user in admins:
        if user == user_id:
            return True
    return False


def exists_in_waiting_list(user_id):
    for user in waiting_list:
        if user == user_id:
            return True
    return False


def exists_in_black_list(user_id):
    for user in black_list:
        if user == user_id:
            return True
    return False


def approve_admin(user_id):
    admins.append(user_id)


def remove_admin(user_id):
    admins.remove(user_id)


def all_admins():
    my_list = []
    for admin in admins:
        my_list.append(admin)

    return tools.show_list(my_list)


def check_admin(user_id):
    for admin in admins:
        if str(admin) == str(user_id):
            return True

    return False
