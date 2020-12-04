import PySimpleGUI as sg
import queries_to_db

# import common
# from main import main_menu

sg.theme('Reddit')


def add_document():
    layout = [[sg.Text(size=(50, 1))],
              [sg.Text('Name:', size=(10, 1)), sg.Input(key='name')],
              [sg.Text('Author:', size=(10, 1)), sg.Input(key='author')],
              [sg.Text('Genre:', size=(10, 1)), sg.Input(key='genre')],
              [sg.Text(size=(50, 1), key='out')],
              [sg.Button('Add'), sg.Button('Exit'), sg.Button('Back')]]

    window = sg.Window('Add document', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Add':
            if queries_to_db.add_doc(values['name'], values['author'], values['genre']):
                window['out'].update('Document added')
            else:
                window['out'].update('Document not added')
        elif event == 'Back':
            window.close()
            menu()

    window.close()


def write_off_document():
    documents = queries_to_db.list_of_documents()

    layout = [[sg.Text(size=(50, 1))],
              [sg.Text('Documents:', size=(15, 1)), sg.Listbox(documents, size=(50, 20), key='doc')],
              [sg.Text(size=(50, 1), key='out')],
              [sg.Button('Delete'), sg.Button('Exit'), sg.Button('Back')]]

    window = sg.Window('Write off a document', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Back':
            window.close()
            menu()
        if event == 'Delete':
            if queries_to_db.delete_document(values['doc'][0]):
                window['out'].update('Document deleted')
            else:
                window['out'].update('Document not deleted')


def view_workers():
    layout = []
    workers = queries_to_db.select_workers()
    for num, w in enumerate(workers):
        if num % 2 == 0:
            layout.append([sg.Text(w[0], size=(20, 1)), sg.Text(w[1], size=(20, 1)), sg.Text(w[2], size=(20, 1))])
        else:
            layout.append([sg.Text(w[0], size=(20, 1), background_color='light grey'),
                           sg.Text(w[1], size=(20, 1), background_color='light grey'),
                           sg.Text(w[2], size=(20, 1), background_color='light grey')])

    window = sg.Window('View all workers', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break


def menu():
    layout = [[sg.Button('Back'), sg.Button('Exit')],
              [sg.Button('Add document', size=(20, 5)), sg.Button('Write off a document', size=(20, 5))],
              [sg.Button('View all workers', size=(20, 5)), sg.Button('View all documents of visitor', size=(20, 5))],
              [sg.Button('Add worker', size=(20, 5)), sg.Button('Dismiss worker', size=(20, 5))],
              [sg.Button('Add visitor', size=(20, 5)), sg.Button('Exclude visitor', size=(20, 5))],
              [sg.Button('Quarterly report', size=(42, 5))]]

    window = sg.Window('Menu of chief librarian', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Main menu':
            break
        else:
            window.close()
            if event == 'Back':
                window.close()
                return True
            if event == 'Add document':
                add_document()
            elif event == 'Write off a document':
                write_off_document()
            elif event == 'View all workers':
                view_workers()

    window.close()
