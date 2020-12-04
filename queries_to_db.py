from sql_connection import Sql

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
    print(workers)
    return workers
