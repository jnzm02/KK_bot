import datetime

deadline = datetime.datetime(2022, 1, 1, 20, 0, 0)
default_deadline = datetime.datetime(2022, 1, 1, 20, 0, 0)


def check_deadline():
    return not deadline == datetime.datetime(2022, 1, 1, 20, 0, 0)


def set_deadline(day, month, year):
    global deadline
    new_deadline = datetime.datetime(int(year), int(month), int(day), 20, 0, 0)
    deadline = new_deadline
    del new_deadline


def till_deadline():
    temp = deadline - datetime.datetime.today()
    return temp.days


def get_deadline():
    return '⏰ '+str(deadline)


def clean_all():
    remove_deadline()


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


def check_date(day, month, year):
    try:
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        return False

    return True
