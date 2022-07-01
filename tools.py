def extract_arg(arg):
    return arg.split()[1:]


def check_has_arg(arg):
    return not len(arg) == 0


def show_list(my_list):
    if len(my_list) == 0:
        return "List is empty"
    the_list = ""
    for item in my_list:
        the_list += item + '\n'

    return the_list

