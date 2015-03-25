import sqlite3


def main():
    db = sqlite3.connect("data.mydb");

    #Prueba de creacion de tabla
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS test(id INTEGER PRIMARY KEY, points INTEGER)''')

    #Prueba de insertado de datos
    cursor.execute('''INSERT INTO highscores(points) VALUES(?)''', (10,))
    cursor.execute('''INSERT INTO highscores(points) VALUES(?)''', (0,))
    cursor.execute('''INSERT INTO highscores(points) VALUES(?)''', (25,))

    #Prueba de sacado del mayor valor
    cursor.execute('''SELECT MAX(points) from highscores''')
    hs = cursor.fetchone()
    print hs[0]
    #Imprime correctamente el valor 25

    #Prueba de limpieza de datos
    cursor.execute('''DELETE FROM highscores ''')

    #Borrado de la tabla de prueba
    cursor.execute('''DROP TABLE test''')


if __name__ == '__main__':
    main()