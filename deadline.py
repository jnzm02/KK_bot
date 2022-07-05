import datetime

deadline = datetime.datetime(2022, 1, 1, 20, 0, 0)
default_deadline = datetime.datetime(2022, 1, 1, 20, 0, 0)


def set_deadline(day, month, year):
    print(day, month, year)
    deadline.replace(year=int(year), month=int(month), day=int(day))


def get_deadline():
    return deadline


def check_new_deadline():
    if deadline < datetime.datetime.today() or deadline == default_deadline:
        return False

    return True


def remove_deadline():
    global deadline
    deadline = default_deadline


def extend_deadline(days):
    global deadline
    deadline = deadline + datetime.timedelta(days=days)


def today():
    return datetime.date.today()
