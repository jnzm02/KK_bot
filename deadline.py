import datetime
import dbhelper


def check_deadline():
    data = dbhelper.get_deadline()
    if data[0] == 1 and data[1] == 1 and data[2] == 2022:
        return False
    return True


def till_deadline():
    date = dbhelper.get_deadline()
    db_deadline = datetime.datetime(date[2], date[1], date[0], 20, 0, 0)
    return (db_deadline - datetime.datetime.today()).days


def get_deadline():
    data = dbhelper.get_deadline()
    db_deadline = datetime.datetime(data[2], data[1], data[0], 20, 0, 0)
    # month_name = str(datetime.datetime.strptime(str(db_deadline.month), "%m"))
    # return '⏰ ' + str(db_deadline.day) + month_name + str(db_deadline.year)
    return '⏰ '+str(db_deadline)


def extend_deadline(days):
    data = dbhelper.get_deadline()
    db_deadline = datetime.datetime(data[2], data[1], data[0], 20, 0, 0)
    new_deadline = db_deadline + datetime.timedelta(days=days)
    dbhelper.set_deadline(new_deadline.day, new_deadline.month, new_deadline.year)


def check_date(day, month, year):
    try:
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        return False
    return True
