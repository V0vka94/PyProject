import sqlite3

youngs = {}
items = {}

def create_table():
# Создаем таблицу 
    sql = ('''
    CREATE TABLE IF NOT EXISTS Participants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    birthday TEXT NOT NULL,
    congratulation TEXT NOT NULL)
    ''')
    
def edit_item():
    pass

def insert_item(name, birthday, text):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    sql = "INSERT INTO Participants (name, birthday, congratulation) VALUES (?, ?, ?) "
    global youngs
    cursor.execute(sql, (name, birthday, text))
    connection.commit()
    connection.close()
    print ('Значения добавлены!')
    youngs = {'name':name, 'birthday':birthday, 'text':text}
    print (str(youngs))

def select_items(day, month):
    global youngs, items
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    sql = 'SELECT * FROM Participants WHERE birthday LIKE ?'    
    cursor.execute(sql,(day+'.'+month+'%',))
    res = cursor.fetchall()
    for r in res:
        youngs = {'name': r[1], 'birthday': r[2], 'text': r[3]}
        items = {'id':r[0], 'items':youngs}
        print('id: ', r[0])
        print('Имя: ', r[1])
        print('День рождения: ', r[2])
        print('Текст: ', r[3])
    connection.commit()
    print (str(items))
    print ('Success!')
    connection.close()