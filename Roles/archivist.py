import PySimpleGUI as sg
import queries_to_db

sg.theme('Reddit')


def search_document_in_archive(login):
    layout = [[sg.Text('Name:', size=(15, 1)), sg.Input(size=(30, 20), key='name')],
              [sg.Text('Author:', size=(15, 1)), sg.Input(size=(30, 20), key='author')],
              [sg.Listbox('', size=(70, 20), key='out')],
              [sg.Button('Search'), sg.Button('Exit'), sg.Button('Back')]]

    window = sg.Window('Search document with name or author in archive', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Search':
            documents = queries_to_db.select_docs_in_archive(values['name'], values['author'])
            docs = []
            for doc in documents:
                docs.append(f"{doc[0]}. {doc[1]} - {doc[2]} - {doc[3]}")
            window['out'].update(docs)
        if event == 'Back':
            window.close()
            menu(login)

    window.close()


def add_document_to_archive(login):
    statuses = queries_to_db.get_statuses()
    st = []
    for s in statuses:
        st.append(f"{s[0]}. {s[1]}")
    layout = [[sg.Text(size=(50, 1))],
              [sg.Text('Title:', size=(10, 1)), sg.Input(key='name')],
              [sg.Text('Author:', size=(10, 1)), sg.Input(key='author')],
              [sg.Text('Status:', size=(10, 1)), sg.InputCombo(st, size=(20, 5), key='status')],
              [sg.Text(size=(50, 1), key='out')],
              [sg.Button('Add'), sg.Button('Exit'), sg.Button('Back')]]

    window = sg.Window('Add document', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Add':
            if queries_to_db.add_doc_to_archive(values['name'], values['author'],
                                                values['status'].split('.')[0], login):
                window['out'].update('Document added')
            else:
                window['out'].update('Document not added')
        elif event == 'Back':
            window.close()
            menu(login)

    window.close()


def create_archive_copy(login):
    documents = queries_to_db.list_of_archive_documents()
    layout = [[sg.Text(size=(50, 1))],
              [sg.Text('Documents:', size=(15, 1)), sg.Listbox(documents, size=(50, 20), key='doc')],
              [sg.Text(size=(50, 1), key='out')],
              [sg.Button('Copy'), sg.Button('Exit'), sg.Button('Back')]]

    window = sg.Window('Copy a document in archive', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Back':
            window.close()
            menu(login)
        if event == 'Copy':
            if queries_to_db.copy_doc_in_archive(values['doc'][0].split('.')[0], login):
                window['out'].update('Document copied')
            else:
                window['out'].update('Document not copied')

    window.close()


def exception_from_archive(login):
    documents = queries_to_db.list_of_archive_documents()
    layout = [[sg.Text(size=(50, 1))],
              [sg.Text('Documents:', size=(15, 1)), sg.Listbox(documents, size=(50, 20), key='doc')],
              [sg.Text(size=(50, 1), key='out')],
              [sg.Button('Delete'), sg.Button('Exit'), sg.Button('Back')]]

    window = sg.Window('Delete a document from archive', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Back':
            window.close()
            menu(login)
        if event == 'Delete':
            if queries_to_db.delete_document_from_archive(values['doc'][0].split('.')[0]):
                window['out'].update('Document deleted')
            else:
                window['out'].update('Document not deleted')

    window.close()


def change_status(login):
    documents = queries_to_db.list_of_archive_documents()
    statuses = queries_to_db.get_statuses()
    st = []
    for s in statuses:
        st.append(f"{s[0]}. {s[1]}")
    layout = [[sg.Text(size=(50, 1))],
              [sg.Text('Documents:', size=(15, 1)), sg.Listbox(documents, size=(50, 20), key='doc')],
              [sg.Text('Change status to:', size=(15, 1)), sg.InputCombo(st, size=(20, 5), key='status')],
              [sg.Text(size=(50, 1), key='out')],
              [sg.Button('Change'), sg.Button('Exit'), sg.Button('Back')]]

    window = sg.Window('Change status of document in archive', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Back':
            window.close()
            menu(login)
        if event == 'Change':
            if queries_to_db.change_status_of_doc(values['doc'][0].split('.')[0], values['status'][0].split('.')[0]):
                window['out'].update('Status changed')
            else:
                window['out'].update('Status not changed')


def menu(login):
    layout = [[sg.Button('Back'), sg.Button('Exit')],
              [sg.Button('Search document in archive', size=(20, 5)),
               sg.Button('Add document to archive', size=(20, 5))],
              [sg.Button('Create archive copy', size=(20, 5)), sg.Button('Exception from archive', size=(20, 5))],
              [sg.Button('Change status of document in archive', size=(20, 5))]]

    window = sg.Window('Menu of archivist', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Main menu':
            break
        else:
            window.close()
            if event == 'Back':
                window.close()
                return True
            if event == 'Search document in archive':
                search_document_in_archive(login)
            elif event == 'Add document to archive':
                add_document_to_archive(login)
            elif event == 'Create archive copy':
                create_archive_copy(login)
            elif event == 'Exception from archive':
                exception_from_archive(login)
            elif event == 'Change status of document in archive':
                change_status(login)

    window.close()
