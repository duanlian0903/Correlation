# tested
import smtplib
import win32com.client as wincl
import api.entire_project_parameter as aepp


def send_email(subject, content):  # tested
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('lian.program.email@gmail.com', 'test0002')
        server.sendmail('lian.program.email@gmail.com', 'duanlian.cn@gmail.com', 'Subject: ' + str(subject) + '\n\n' + str(content))
    except:
        show_exception_message('Having error for sending email')


def speak_message(text):  # tested
    try:
        speak = wincl.Dispatch('SAPI.SpVoice')
        speak.Speak(text)
    except:
        show_exception_message('Having error for speaking')


def show_exception_message(exception_message):  # tested
    if aepp.whether_show_exception_message():
        print(exception_message)
