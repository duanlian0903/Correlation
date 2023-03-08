# tested
import api.entire_project_parameter as aepp


def show_exception_message(exception_message):  # tested
    if aepp.whether_show_exception_message():
        print(exception_message)
