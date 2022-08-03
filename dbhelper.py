import sqlite3
import psycopg2
from decouple import config

connection = psycopg2.connect(database=config('DB_DATABASE'),
                              user=config('DB_USER'),
                              password=config('DB_PASSWORD'),
                              host=config('DB_HOST'),
                              port="5432")

cursor = connection.cursor()


def add_juz(juz_number, username):
    cursor.execute("UPDATE juz SET user_id = user_id(username={usename}) WHERE juz_number = {juz_number}".format(user_id=user_id,
                                                                                               juz_number=juz_number))
    cursor.commit()


def drop_juz(juz_number):
    cursor.execute("UPDATE juz SET user_id = -1 WHERE juz_number = {juz_number}".format(juz_number=juz_number))
    cursor.commit()


def done_juz(juz_number):
    cursor.execute("UPDATE juz SET is_done = TRUE where juz_number = {juz_number}".format(juz_number=juz_number))
    cursor.commit()


def clean_all():
    cursor.execute("UPDATE juz SET is_done=FALSE, user_id=-1")
    cursor.commit()


def check_read(juz_number) -> bool:
    cursor.execute("SELECT * FROM juz WHERE juz_number={juz_number}".format(juz_number=juz_number))
    return cursor.is_done  # return true if the juz already read or not

def set_deadline(day, month, year):
    # global cursor
    print("Entrance UPDATE deadline SET day={day}, month={month}, year={year}".format(day=day, month=month, year=year))
    cursor.execute("UPDATE deadline SET day={day}, month={month}, year={year}".format(day=day, month=month, year=year))
    connection.commit()


def get_deadline() -> str:
    cursor.execute("SELECT * from deadline")
    return str(cursor.fetchall())


def get_my_list(username):
    cursor.execute("SELECT * FROM juz WHERE user_id(username={username})".format(username=username))
    for juz in cursor:
        print(juz.juz_number)
