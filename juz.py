def check_read(juz_data) -> bool:
    return juz_data[2]


def check_mine(juz_data, user) -> bool:
    return str(user.id) == str(juz_data[1])


def check_free(juz_data) -> bool:
    return juz_data == '-1'
