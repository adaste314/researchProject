import mysql.connector
from mysql.connector import connect, Error
from getpass import getpass

username = input("Enter username: ")
passkey = getpass("Enter password: ")
try:
    with connect(
        host="Serge-HP13",
        user=username,
        password=passkey,
    ) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("CREATE DATABASE data")
            except Error as e:
                print(e)
                pass

        connection = connect(host="Serge-HP13", user=username, password=passkey, database='data')
        with connection.cursor() as cursor:
            try:
                cursor.execute("""CREATE TABLE posts(
                    link LONGBLOB,
                    words LONGBLOB
                    )""")
            except Error as e:
                print(e)
                pass

            try:
                cursor.execute("""CREATE TABLE words(
                    word VARCHAR(45),
                    weighting DECIMAL(65, 30)
                    )""")
            except Error as e:
                print(e)
                pass

            connection.commit()

except Error as e:
    print(e)