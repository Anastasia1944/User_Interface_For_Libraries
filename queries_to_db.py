from sql_connection import Sql

# Create connection to Database "test"
sql = Sql('Library')
cursor = sql.cnxn.cursor()


def entry(log, pas):
    cursor.execute(f"EXEC Account_Position '{log}', '{pas}'")
    position = cursor.fetchall()[0][0]
    return position



