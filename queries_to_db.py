from sql_connection import Sql
import random

# Create connection to Database "test"
sql = Sql('Library')
cursor = sql.cnxn.cursor()


def entry(log, pas):
    if log and pas:
        cursor.execute(f"EXEC Account_Position '{log}', '{pas}'")
        position = cursor.fetchall()[0][0]
        return position
    return []


def add_doc(name, author, genre):
    if name and author and genre:
        cursor.execute(f"INSERT Document(name, author, genre, date_added, is_present) "
                       f"VALUES ('{name}', '{author}', '{genre}', GETDATE(), 1)")
        cursor.commit()
        cursor.execute(
            f"SELECT document_id FROM Document WHERE name='{name}' AND author='{author}' AND genre='{genre}'")
        return cursor.fetchall()[0][0]
    return False


def list_of_documents():
    cursor.execute(f"SELECT name, author, genre, CONVERT(NVARCHAR, date_added, 1) FROM Document")
    documents = cursor.fetchall()
    docs = []
    for doc in documents:
        docs.append(f"{doc[0]} - {doc[1]} - {doc[2]} - {doc[3]}")
    docs.sort()
    return docs


def delete_document(document):
    document = document.split(' - ')
    cursor.execute(f"DELETE FROM Document WHERE name='{document[0]}' AND author='{document[1]}' "
                   f"AND genre='{document[2]}'")
    cursor.commit()
    cursor.execute(f"SELECT document_id FROM Document WHERE name='{document[0]}' AND author='{document[1]}' "
                   f"AND genre='{document[2]}'")
    if not cursor.fetchall()[0][0]:
        return True
    else:
        return False


def select_workers():
    cursor.execute(f"SELECT * FROM Workers_positions")
    workers = cursor.fetchall()
    return workers


def select_visitors():
    cursor.execute(f"SELECT visitor_id, name, surname, phone_number FROM Visitor")
    visitors = cursor.fetchall()
    return visitors


def select_docs_of_visitor(visitor_id):
    cursor.execute(f"SELECT document_name, CONVERT(NVARCHAR, date, 1) FROM Visitors_and_books "
                   f"WHERE visitor_id={visitor_id}")
    docs = cursor.fetchall()
    documents = [' '.join(doc) for doc in docs]
    return documents


def select_positions():
    cursor.execute(f"SELECT position_id, position_name FROM Position")
    pos = cursor.fetchall()
    positions = [str(p[0]) + '. ' + p[1] for p in pos]
    return positions


def add_account(login):
    password = password_generation()
    cursor.execute(f"INSERT Account(login, password) VALUES ('{login}', '{password}')")
    cursor.commit()
    cursor.execute(f"SELECT account_id FROM Account WHERE login='{login}' AND password='{password}'")
    account_id = cursor.fetchone()[0]
    return account_id


def add_worker(position, name, surname, login, phone_number):
    if name and position and surname and login and phone_number:
        account_id = add_account(login)
        cursor.execute(f"INSERT Worker(position_id, name, surname, phone_number, account_id) "
                       f"VALUES ({int(position[0])}, '{name}', '{surname}', '{phone_number}', '{account_id}')")
        cursor.commit()
        cursor.execute(f"SELECT worker_id FROM Worker WHERE name='{name}' AND phone_number='{phone_number}'")
        return cursor.fetchone()
    return False


def password_generation():
    chars = '+_=-!@#$%^&*<>()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password = ''
    for i in range(10):
        password += random.choice(chars)
    return password


def delete_worker(worker_id):
    if worker_id:
        cursor.execute(f"DELETE FROM Worker WHERE worker_id={worker_id}")
        cursor.commit()
        cursor.execute(f"SELECT name FROM Worker WHERE worker_id={worker_id}")
        return cursor.fetchone()
    return False


def add_visitor(name, surname, login, phone_number, passport_number):
    if name and passport_number and surname and login and phone_number:
        account_id = add_account(login)
        cursor.execute(f"INSERT Visitor(name, surname, phone_number, passport_number, account_id) "
                       f"VALUES ('{name}', '{surname}', '{phone_number}', '{passport_number}', '{account_id}')")
        cursor.commit()
        cursor.execute(f"SELECT visitor_id FROM Visitor WHERE name='{name}' AND phone_number='{phone_number}'")
        return cursor.fetchone()
    return False


def delete_visitor(visitor_id):
    if visitor_id:
        cursor.execute(f"DELETE FROM Visitor WHERE visitor_id={visitor_id}")
        cursor.commit()
        cursor.execute(f"SELECT name FROM Visitor WHERE visitor_id={visitor_id}")
        return cursor.fetchone()
    return False


def quarterly_report():
    cursor.execute(f"EXEC quarterly_report")
    return cursor.fetchall()


def select_docs_on_name_or_author(name, author):
    if name and author:
        str = f"name='{name}' AND author='{author}'"
    elif name:
        str = f"name='{name}'"
    elif author:
        str = f"author='{author}'"
    else:
        return False

    cursor.execute(f"SELECT document_id, name, author, genre, CONVERT(NVARCHAR, date_added, 1), is_present "
                   f"FROM Document WHERE {str}")
    docs = cursor.fetchall()
    return docs


def id_from_login(login):
    cursor.execute(f"SELECT visitor_id FROM Visitor JOIN Account ON Visitor.account_id=Account.account_id "
                   f"WHERE login='{login}'")
    return cursor.fetchone()[0]


def view_visitor_documents(login):
    visitor_id = id_from_login(login)
    cursor.execute(f"SELECT document_name, CONVERT(NVARCHAR, date, 1) FROM Visitors_and_books WHERE visitor_id='{visitor_id}'")
    return cursor.fetchall()


def submit_request(login, name, author):
    visitor_id = id_from_login(login)
    if name and author:
        cursor.execute(f"INSERT Request(visitor_id, title, author, date) "
                       f"VALUES ({visitor_id}, '{name}', '{author}', GETDATE())")
        cursor.commit()
        cursor.execute(f"SELECT request_id FROM Request "
                       f"WHERE visitor_id={visitor_id} AND title='{name}' AND author='{author}'")
        return cursor.fetchall()
    return False


