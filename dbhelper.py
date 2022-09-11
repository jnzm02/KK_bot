import sqlite3
import psycopg2
from decouple import config

# local
import tools

connection = psycopg2.connect(database=config('DB_DATABASE'),
                              user=config('DB_USER'),
                              password=config('DB_PASSWORD'),
                              host=config('DB_HOST'),
                              port="5432")

cursor = connection.cursor()


def add_juz(juz_number, user):
    cursor.execute("UPDATE juz SET user_id = '{}', username = '{}' WHERE juz_number = {}".format(user.id, user.username, juz_number))
    connection.commit()


def remove_admin(user_id):
    cursor.execute("DELETE FROM admins WHERE user_id = {}".format(user_id))
    connection.commit()


def all_admins() -> list:
    cursor.execute("SELECT * FROM accounts WHERE admin_status = True")
    admin_list = []
    admins = cursor.fetchall()
    for admin in admins:
        admin_list.append(admin[1])
    return admin_list


def done_reading(juz_number):
    cursor.execute("UPDATE juz SET is_done = True WHERE juz_number={}".format(juz_number))
    connection.commit()


def drop_user(juz_number):
    cursor.execute("UPDATE juz SET user_id='-1', username='NULL_USER' WHERE juz_number={}".format(juz_number))
    connection.commit()


def show_all():
    cursor.execute("SELECT * FROM juz ORDER BY juz_number")
    return cursor.fetchall()


def done_juz(juz_number):
    cursor.execute("UPDATE juz SET is_done = TRUE where juz_number = {}".format(juz_number))
    connection.commit()


def clean_all():
    cursor.execute("UPDATE juz SET is_done = FALSE, user_id='-1', username='NULL_USER'")
    connection.commit()


def check_read(juz_number) -> bool:
    cursor.execute("SELECT * FROM juz WHERE juz_number={}".format(juz_number))
    if cursor.description is None:
        return False
    data = cursor.fetchall()
    return data[0][2]


def set_deadline(day, month, year):
    cursor.execute("UPDATE deadline SET day={}, month={}, year={}".format(day, month, year))
    connection.commit()


def check_mine(juz_number, user) -> bool:
    cursor.execute("SELECT * FROM juz WHERE juz_number={} and user_id='{}'".format(juz_number, user.id))
    if cursor.description is None:
        return False
    data = cursor.fetchall()
    return len(data) > 0


def check_free(juz_number) -> bool:
    cursor.execute("SELECT * FROM juz WHERE juz_number={} and username = 'NULL_USER'".format(juz_number))
    if cursor.description is None:
        return False
    data = cursor.fetchall()
    return len(data) > 0


def get_deadline() -> list:
    cursor.execute("SELECT * from deadline")
    deadline = cursor.fetchall()
    return [deadline[0][0], deadline[0][1], deadline[0][2]]


def add_new_user(user):
    username = user.username
    if str(username) == 'None':
        if user.first_name is None or user.last_name is None:
            username = "Unknown User"
        else:
            username = user.first_name+' '+user.last_name
    cursor.execute(
        "INSERT INTO accounts VALUES ('{user_id}', '{username}', false) ON conflict (user_id) "
        "DO UPDATE SET username = '{username}'".format(user_id=user.id, username=username))
    connection.commit()


def check_admin(user):
    cursor.execute("SELECT * FROM accounts WHERE user_id = '{}' and admin_status = true".format(user.id))
    return len(cursor.fetchall()) > 0


def clean_all_juz():
    cursor.execute("UPDATE juz SET user_id = '-1', username='NULL_USER', is_done = False")
    connection.commit()


def set_default_deadline():
    cursor.execute("UPDATE deadline SET day=1, month=1, year=2022")
    connection.commit()


def free_juz():
    cursor.execute("SELECT * FROM juz where user_id = '-1' and is_done = False")
    return tools.get_juz(sorted(cursor.fetchall()))


def users_list():
    cursor.execute("SELECT * FROM accounts WHERE user_id != '-1'")
    return cursor.fetchall()


def get_progress():
    cursor.execute("SELECT * FROM progress")
    return cursor.fetchall()


def take_late_people():
    cursor.execute("SELECT * FROM juz WHERE is_done = FALSE")
    return cursor.fetchall()


def add_text(text, juz_number):
    cursor.commit('UPDATE juz SET ')

    cursor.execute("INSERT INTO progress VALUES ('{}')".format(text))
    connection.commit()


def clear_progress():
    cursor.execute("DELETE FROM progress")
    connection.commit()


def generate_my_list(user):
    cursor.execute("SELECT * FROM juz where user_id='{}'".format(user.id))
    return tools.get_juz(sorted(cursor.fetchall()))


def get_general_chat_id():
    cursor.execute("SELECT * FROM general_chat")
    return cursor.fetchall()[0][0]


def set_general_chat(chat_id):
    cursor.execute("UPDATE general_chat SET general_chat_id = '{}'".format(chat_id))
    connection.commit()


def completed_hatym():
    cursor.execute("UPDATE hatym_counter SET haym_number=hatym_number+1")
    connection.commit()


def get_hatym_number():
    cursor.execute("SELECT * FROM hatym_counter")
    return cursor.fetchall()[0][0]


def get_juz_data(juz_number):
    cursor.execute("SELECT * FROM juz WHERE juz_number={}".format(juz_number))
    return cursor.fetchall()[0]


def get_not_finished_users():
    cursor.execute("SELECT * FROM juz WHERE is_done = False")
    users_list = []
    user_data = cursor.fetchall()
    for user in user_data:
        if user[3] != 'NULL_USER':
            if user[3] != 'None':
                if str('@'+user[3]) not in users_list:
                    users_list.append('@'+user[3])

    return users_list


def user_id_list() -> list:
    cursor.execute("SELECT * FROM accounts WHERE username != 'justadlet'")
    data = cursor.fetchall()
    users_list = []
    for user in data:
        users_list.append(user[0])

    return users_list


def set_admin(user_id):
    cursor.execute("UPDATE accounts SET admin_status = True WHERE user_id = '{}'".format(user_id))
    connection.commit()


def number_of_users() -> int:
    cursor.execute("SELECT COUNT(*) FROM accounts")
    data = cursor.fetchall()
    return data[0]
