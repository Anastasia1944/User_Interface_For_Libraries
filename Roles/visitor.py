import PySimpleGUI as sg
import queries_to_db


def search_document(login):
    layout = [[sg.Text('Name:', size=(15, 1)), sg.Input(size=(30, 20), key='name')],
              [sg.Text('Author:', size=(15, 1)), sg.Input(size=(30, 20), key='author')],
              [sg.Listbox('', size=(70, 20), key='out')],
              [sg.Button('Search'), sg.Button('Exit'), sg.Button('Back')]]

    window = sg.Window('Search document on name or author', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Search':
            documents = queries_to_db.select_docs_on_name_or_author(values['name'], values['author'])
            docs = []
            for doc in documents:
                if doc[5]:
                    s = 'available'
                else:
                    s = 'not available'
                docs.append(f"{doc[0]}. {doc[1]} - {doc[2]} - {doc[3]} - {doc[4]} ({s})")
            window['out'].update(docs)
        if event == 'Back':
            window.close()
            menu(login)

    window.close()


def view_documents(login):
    documents = queries_to_db.view_visitor_documents(login)
    layout = [[sg.Text('name', size=(25, 1)), sg.Text('date', size=(25, 1))]]
    for num, d in enumerate(documents):
        if num % 2 != 0:
            layout.append([sg.Text(d[0], size=(25, 1)), sg.Text(d[1], size=(25, 1))])
        else:
            layout.append([sg.Text(d[0], size=(25, 1), background_color='light grey'),
                           sg.Text(d[1], size=(25, 1), background_color='light grey')])

    layout.append([sg.Button('Back'), sg.Button('Exit')])

    window = sg.Window('View documents', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Back':
            window.close()
            menu(login)
    window.close()


def app_for_document(login):
    layout = [[sg.Text('Name:', size=(15, 1)), sg.Input(size=(30, 20), key='name')],
              [sg.Text('Author:', size=(15, 1)), sg.Input(size=(30, 20), key='author')],
              [sg.Text(size=(50, 1), key='out')],
              [sg.Button('Submit'), sg.Button('Exit'), sg.Button('Back')]]

    window = sg.Window('Submit a request for a document', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Back':
            window.close()
            menu(login)
        if event == 'Submit':
            if queries_to_db.submit_request(login, values['name'], values['author']):
                window['out'].update('Request added')
            else:
                window['out'].update('Request not added')

    window.close()


def menu(login):
    layout = [[sg.Button('Back'), sg.Button('Exit')],
              [sg.Button('Search document', size=(20, 5)), sg.Button('View documents', size=(20, 5))],
              [sg.Button('Application for document', size=(20, 5))]]

    window = sg.Window('Menu of visitor', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Main menu':
            break
        else:
            window.close()
            if event == 'Back':
                window.close()
                return True
            if event == 'Search document':
                search_document(login)
            if event == 'View documents':
                view_documents(login)
            if event == 'Application for document':
                app_for_document(login)


    window.close()
