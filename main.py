import PySimpleGUI as sg
from queries_to_db import entry
from Roles import chief_librarian, visitor, librarian, archivist


def login():

    layout = [[sg.Text(size=(50, 1), key='out')],
              [sg.Text('Login:', size=(10, 1)), sg.Input(key='login')],
              [sg.Text('Password:', size=(10, 1)), sg.Input(key='password', password_char='*')],
              [sg.Text(size=(50, 1), key='out')],
              [sg.Button('Log in'), sg.Button('Exit')]]

    window = sg.Window('Основное меню', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == sg.WIN_CLOSED or event == 'Log in':
            position = entry(values['login'], values['password'])
            if position == []:
                window['out'].update('Неправильный логин или пароль')
            elif position == 'Главный библиотекарь':
                window.close()
                chief_librarian.menu()
  #          elif position == 'Библиотекарь':
 #               librarian.menu()
 #           elif position == 'Посетитель':
  #              visitor.menu()
 #           elif position == 'Архивист':
 #               archivist.menu()

    window.close()


sg.theme('Reddit')
login()

