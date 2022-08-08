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
        admin_list.append(admin[0])
    return admin_list


def done_reading(juz_number):
    cursor.execute("UPDATE juz SET is_done = True WHERE juz_number={}".format(juz_number))
    connection.commit()


def drop_user(juz_number):
    cursor.execute("UPDATE juz SET user_id='-1', username='NULL_USER' WHERE juz_number={}".format(juz_number))
    connection.commit()


def show_all():
    cursor.execute("SELECT * FROM juz")
    return sorted(cursor.fetchall())


def done_juz(juz_number):
    cursor.execute("UPDATE juz SET is_done = TRUE where juz_number = {}".format(juz_number))
    connection.commit()


def clean_all():
    cursor.execute("UPDATE juz SET is_done = FALSE, user_id='-1', username='NULL_USER'")
    connection.commit()


def check_read(juz_number) -> bool:
    cursor.execute("SELECT * FROM juz WHERE juz_number={} and is_done = True".format(juz_number))
    return len(cursor.fetchall()) > 0  # return true if the juz already read


def set_deadline(day, month, year):
    cursor.execute("UPDATE deadline SET day={}, month={}, year={}".format(day, month, year))
    connection.commit()


def check_mine(juz_number, user) -> bool:
    cursor.execute("SELECT * FROM juz WHERE juz_number={} and user_id='{}'".format(juz_number, user.id))
    return len(cursor.fetchall()) > 0


def check_free(juz_number) -> bool:
    cursor.execute("SELECT * FROM juz WHERE juz_number={} and username = 'NULL_USER'".format(juz_number))
    return len(cursor.fetchall()) > 0


def get_deadline() -> list:
    cursor.execute("SELECT * from deadline")
    deadline = cursor.fetchall()
    return [deadline[0][0], deadline[0][1], deadline[0][2]]


def add_new_user(user):
    cursor.execute(
        "INSERT INTO accounts VALUES ('{}', '{}', false) "
        "ON conflict (user_id) DO NOTHING;".format(user.id, user.username))
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
    cursor.execute("SELECT * FROM juz where is_done = False")
    return tools.get_juz(sorted(cursor.fetchall()))


def generate_my_list(user):
    cursor.execute("SELECT * FROM juz where user_id='{}'".format(user.id))
    return tools.get_juz(sorted(cursor.fetchall()))
