from sql_connection import Sql
from tkinter import *


# create a window
window = Tk()
window.geometry('600x400+200+100')
window.title("Добро пожаловать в приложение PythonRu")
lbl = Label(window, text="Привет")
lbl.grid(column=0, row=0)
window.mainloop()

# Create connection to Database "test"
sql = Sql('test')
cursor = sql.cnxn.cursor()

# Example of db query
cursor.execute("SELECT * FROM Staff")
row = cursor.fetchall()
print(row)