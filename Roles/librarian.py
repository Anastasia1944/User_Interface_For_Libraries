import PySimpleGUI as sg
import queries_to_db
import datetime

sg.theme('Reddit')


def add_visitor():
    layout = [[sg.Text(size=(50, 1))],
              [sg.Text('Name:', size=(15, 1)), sg.Input(key='name')],
              [sg.Text('Surname:', size=(15, 1)), sg.Input(key='surname')],
              [sg.Text('Login:', size=(15, 1)), sg.Input(key='login')],
              [sg.Text('Phone number:', size=(15, 1)), sg.Input(key='phone_number')],
              [sg.Text('Passport number:', size=(15, 1)), sg.Input(key='passport_number')],
              [sg.Text(size=(50, 1), key='out')],
              [sg.Button('Add'), sg.Button('Exit'), sg.Button('Back')]]

    window = sg.Window('Add visitor', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Add':
            password = queries_to_db.add_visitor(values['name'], values['surname'],
                                                 values['login'], values['phone_number'], values['passport_number'])
            if password:
                window['out'].update('Visitor added. Password: ' + password)
            else:
                window['out'].update('Visitor not added')
        if event == 'Back':
            window.close()
            menu()

    window.close()


def exclude_visitor():
    visitors = queries_to_db.select_visitors()
    vis = []
    for v in visitors:
        vis.append(f'{v[0]}. {v[1]} {v[2]} - {v[3]}')

    layout = [[sg.Text(size=(50, 1))],
              [sg.InputCombo(vis, size=(35, 5), key='visitor')],
              [sg.Text(size=(50, 1), key='out')],
              [sg.Button('Exclude'), sg.Button('Exit'), sg.Button('Back')]]

    window = sg.Window('Exclude visitor', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Back':
            window.close()
            menu()
        if event == 'Exclude':
            if not queries_to_db.delete_visitor(values['visitor'].split('.')[0]):
                window['out'].update('Visitor excluded')
            else:
                window['out'].update('Visitor not excluded')

    window.close()


def give_document():
    visitors = queries_to_db.select_visitors()
    vis = []
    for v in visitors:
        vis.append(f'{v[0]}. {v[1]} {v[2]} - {v[3]}')

    documents = queries_to_db.list_of_documents()

    layout = [[sg.Text(size=(50, 1))],
              [sg.Text('Select visitor', size=(15, 1)), sg.InputCombo(vis, size=(50, 5), key='visitor')],
              [sg.Text('Select document:', size=(15, 1)), sg.Listbox(documents, size=(50, 20), key='doc')],
              [sg.Text(size=(50, 1), key='out')],
              [sg.Button('Provide'), sg.Button('Exit'), sg.Button('Back')]]

    window = sg.Window('Provide document', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Back':
            window.close()
            menu()
        if event == 'Provide':
            if queries_to_db.give_doc_to_visitor(values['visitor'].split('.')[0], values['doc'][0].split('.')[0]):
                window['out'].update('Document provided')
            else:
                window['out'].update('Document not provided')

    window.close()


def take_document():
    visitors = queries_to_db.select_visitors()
    vis = []
    for v in visitors:
        vis.append(f'{v[0]}. {v[1]} {v[2]} - {v[3]}')

    layout = [[sg.Text(size=(50, 1))],
              [sg.Text('Select visitor', size=(15, 1)), sg.InputCombo(vis, size=(50, 5), key='visitor'),
               sg.Button('Output')],
              [sg.Text('Select document:', size=(15, 1)), sg.Listbox('', size=(50, 20), key='doc')],
              [sg.Text(size=(50, 1), key='out')],
              [sg.Button('Return'), sg.Button('Exit'), sg.Button('Back')]]

    window = sg.Window('Return document', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Back':
            window.close()
            menu()
        if event == 'Return':
            vis_id = values['visitor'].split('.')[0]
            if values['doc'] == '':
                window['out'].update('Choose document')
            elif queries_to_db.return_doc_from_visitor(vis_id, values['doc'][0].split('.')[0]):

                window['out'].update('Document returned')
            else:
                window['out'].update('Document not returned')
        if event == 'Output':
            vis_id = values['visitor'].split('.')[0]
            documents = queries_to_db.view_visitor_in_hand_documents(vis_id)
            doc = []
            for d in documents:
                doc.append(f"{d[0]}. {d[1]} - {d[2]}")
            window['doc'].update(doc)

    window.close()


def expired_documents():
    docs = queries_to_db.expired_documents()
    layout = [[sg.Text('id', size=(5, 1)), sg.Text('name', size=(20, 1)), sg.Text('surname', size=(20, 1)),
               sg.Text('date_give', size=(10, 1)), sg.Text('title', size=(20, 1)), sg.Text('author', size=(20, 1))]]
    for num, d in enumerate(docs):
        if num % 2 != 0:
            layout.append([sg.Text(d[0], size=(5, 1)), sg.Text(d[1], size=(20, 1)), sg.Text(d[2], size=(20, 1)),
                           sg.Text(d[3].strftime("%d/%m/%Y"), size=(10, 1)), sg.Text(d[4], size=(20, 1)),
                           sg.Text(d[5], size=(20, 1))])
        else:
            layout.append([sg.Text(d[0], size=(5, 1), background_color='light grey'),
                           sg.Text(d[1], size=(20, 1), background_color='light grey'),
                           sg.Text(d[2], size=(20, 1), background_color='light grey'),
                           sg.Text(d[3].strftime("%d/%m/%Y"), size=(10, 1), background_color='light grey'),
                           sg.Text(d[4], size=(20, 1), background_color='light grey'),
                           sg.Text(d[5], size=(20, 1), background_color='light grey')])

    layout.append([sg.Button('Back'), sg.Button('Exit')])

    window = sg.Window('Menu of librarian', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Back':
            window.close()
            menu()

    window.close()


def menu():
    layout = [[sg.Button('Back'), sg.Button('Exit')],
              [sg.Button('Add visitor', size=(20, 5)), sg.Button('Exclude visitor', size=(20, 5))],
              [sg.Button('Give document', size=(20, 5)), sg.Button('Take document', size=(20, 5))],
              [sg.Button('Expired documents', size=(20, 5))]]

    window = sg.Window('Menu of librarian', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        else:
            window.close()
            if event == 'Back':
                window.close()
                return True
            if event == 'Add visitor':
                add_visitor()
            elif event == 'Exclude visitor':
                exclude_visitor()
            elif event == 'Give document':
                give_document()
            elif event == 'Take document':
                take_document()
            elif event == 'Expired documents':
                expired_documents()

    window.close()
