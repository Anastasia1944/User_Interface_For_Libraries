import PySimpleGUI as sg
from queries_to_db import entry
from Roles import chief_librarian, visitor, librarian, archivist
# from Roles.chief_librarian import menu
import queries_to_db

sg.theme('Reddit')


def log_in(pos, login):
    if pos == 'Главный библиотекарь':
        if chief_librarian.menu() is None:
            main_menu()
    elif pos == 'Пользователь':
        if visitor.menu(login) is None:
            main_menu()


#             elif position == 'Библиотекарь':
#                  librarian.menu()
#              elif position == 'Посетитель':
#                 visitor.menu()
#              elif position == 'Архивист':
#                  archivist.menu()


def main_menu():
    layout = [[sg.Text(size=(50, 1))],
              [sg.Text('Login:', size=(10, 1)), sg.Input(key='login')],
              [sg.Text('Password:', size=(10, 1)), sg.Input(key='password', password_char='*')],
              [sg.Text(size=(50, 1), key='out')],
              [sg.Button('Log in'), sg.Button('Exit')]]

    window = sg.Window('Main menu', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Log in':
            visitor.menu('EkaterinaPopova')
            position = entry(values['login'], values['password'])
            if not position:
                window['out'].update('Invalid login or password')
            else:
                window.close()
                log_in(position, values['login'])

    window.close()


main_menu()
