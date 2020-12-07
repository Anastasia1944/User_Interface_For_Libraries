import PySimpleGUI as sg
import queries_to_db


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

    window.close()


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

    layout.append([sg.Button('Exit'), sg.Button('Back')])

    window = sg.Window('View all workers', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Back':
            window.close()
            menu()

    window.close()


def view_docs_of_visitor():
    visitors = queries_to_db.select_visitors()
    vis = []
    for v in visitors:
        vis.append(f'{v[0]}. {v[1]} {v[2]} - {v[3]}')

    layout = [[sg.InputCombo(vis, size=(35, 5), key='visitor'),
               sg.Listbox('', size=(35, 20), key='docs')],
              [sg.Button('View'), sg.Button('Exit'), sg.Button('Back')]]
    window = sg.Window('View documents of visitor', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Back':
            window.close()
            menu()
        if event == 'View':
            docs = queries_to_db.select_docs_of_visitor(values['visitor'][0])
            window['docs'].update(docs)

    window.close()


def add_worker():
    positions = queries_to_db.select_positions()
    layout = [[sg.Text(size=(50, 1))],
              [sg.Text('Position:', size=(15, 1)), sg.InputCombo(positions, size=(40, 5), key='position')],
              [sg.Text('Name:', size=(15, 1)), sg.Input(key='name')],
              [sg.Text('Surname:', size=(15, 1)), sg.Input(key='surname')],
              [sg.Text('Login:', size=(15, 1)), sg.Input(key='login')],
              [sg.Text('Phone number:', size=(15, 1)), sg.Input(key='phone_number')],
              [sg.Text(size=(50, 1), key='out')],
              [sg.Button('Add'), sg.Button('Exit'), sg.Button('Back')]]

    window = sg.Window('Add worker', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Add':
            password = queries_to_db.add_worker(values['position'], values['name'], values['surname'],
                                        values['login'], values['phone_number'])
            if password:
                window['out'].update('Worker added. Password: ' + password)
            else:
                window['out'].update('Worker not added')
        if event == 'Back':
            window.close()
            menu()

    window.close()


def dismiss_worker():
    workers = queries_to_db.select_workers()
    work = []
    for w in workers:
        work.append(f'{w[3]}. {w[0]} {w[1]} - {w[2]}')
    layout = [[sg.Text(size=(50, 1))],
              [sg.InputCombo(work, size=(35, 5), key='worker')],
              [sg.Text(size=(50, 1), key='out')],
              [sg.Button('Dismiss'), sg.Button('Exit'), sg.Button('Back')]]

    window = sg.Window('Dismiss worker', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Back':
            window.close()
            menu()
        if event == 'Dismiss':
            if not queries_to_db.delete_worker(values['worker'].split('.')[0]):
                window['out'].update('Worker dismissed')
            else:
                window['out'].update('Worker not dismissed')


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


def quarterly_report():
    report = queries_to_db.quarterly_report()
    rep = []
    layout = [[sg.Text('id', size=(7, 1)), sg.Text('name', size=(20, 1)), sg.Text('quantity', size=(15, 1))]]
    for num, r in enumerate(report):
        if num % 2 != 0:
            layout.append([sg.Text(r[0], size=(7, 1)), sg.Text(r[1], size=(20, 1)), sg.Text(r[2], size=(15, 1))])
        else:
            layout.append([sg.Text(r[0], size=(7, 1), background_color='light grey'),
                           sg.Text(r[1], size=(20, 1), background_color='light grey'),
                           sg.Text(r[2], size=(15, 1), background_color='light grey')])

    layout.append([sg.Button('Exit'), sg.Button('Back')])

    window = sg.Window('Quarterly report', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Back':
            window.close()
            menu()


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
            elif event == 'View all documents of visitor':
                view_docs_of_visitor()
            elif event == 'Add worker':
                add_worker()
            elif event == 'Dismiss worker':
                dismiss_worker()
            elif event == 'Add visitor':
                add_visitor()
            elif event == 'Exclude visitor':
                exclude_visitor()
            elif event == 'Quarterly report':
                quarterly_report()

    window.close()
