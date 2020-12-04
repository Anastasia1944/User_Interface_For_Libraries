import PySimpleGUI as sg

sg.theme('Reddit')


def menu():
    print('ffegegg')
    layout = [[sg.Button('Log in'), sg.Button('Exit')],
              [sg.Button('Log in'), sg.Button('Exit')]]

    window = sg.Window('Меню главного библиотекаря', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

    window.close()
