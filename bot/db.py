import sqlite3

class Database:
    def __init__(self, db_file):
        print("ok")

    def user_exists(self, user_id):
        self.connection = sqlite3.connect('base.db')
        self.cursor = self.connection.cursor()
        try:
            with self.connection:
                resault = self.cursor.execute("SELECT * from users WHERE user_id = ?", (user_id,)).fetchmany(1)
                return bool(len(resault))

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        
    def read_sqlite_table(records):
        try:
            sqlite_connection = sqlite3.connect('base.db')
            cursor = sqlite_connection.cursor()
            # print("Подключен к SQLite")

            sqlite_select_query = """SELECT * from users"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            # print("Всего строк:  ", len(records))
            # print("Вывод каждой строки")
            for row in records:
                x = row[2]
                
            cursor.close()

            return x

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    def update_sqlite_table(self, user_id, city):
        try:
            sqlite_connection = sqlite3.connect('base.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")

            sql_update_query = """Update users set city = ? where user_id = ?"""
            data = (city, user_id)
            cursor.execute(sql_update_query, data)
            sqlite_connection.commit()
            print("Запись успешно обновлена")
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    def read_push(records):
            try:
                sqlite_connection = sqlite3.connect('base.db')
                cursor = sqlite_connection.cursor()
                # print("Подключен к SQLite")

                sqlite_select_query = """SELECT * from users"""
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                # print("Всего строк:  ", len(records))
                # print("Вывод каждой строки")
                for row in records:
                    x = row[3]
                    
                cursor.close()
                print(x)
                return x

            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)
            finally:
                if sqlite_connection:
                    sqlite_connection.close()

    def update_bool(self, user_id, push):
        try:
            sqlite_connection = sqlite3.connect('base.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")

            sql_update_query = """Update users set push = ? where user_id = ?"""
            data = (push, user_id)
            cursor.execute(sql_update_query, data)
            sqlite_connection.commit()
            print("Запись успешно обновлена")
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")
    
    def read_isru(records):
            try:
                sqlite_connection = sqlite3.connect('base.db')
                cursor = sqlite_connection.cursor()
                # print("Подключен к SQLite")

                sqlite_select_query = """SELECT * from users"""
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                # print("Всего строк:  ", len(records))
                # print("Вывод каждой строки")
                for row in records:
                    x = row[4]
                    print(x)
                    
                cursor.close()
                
                return x

            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)
            finally:
                if sqlite_connection:
                    sqlite_connection.close()

    def add_isru(self, user_id, isru):
        try:
            sqlite_connection = sqlite3.connect("base.db")
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")

            sqlite_insert_with_param = """INSERT INTO users
                                (user_id, isru)
                                VALUES
                                (?, ?);"""

            data_tuple = (user_id, isru)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqlite_connection.commit()

            print("Запись успешно вставлена ​​в таблицу sqlitedb_developers ", cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")
    
    def update_sqlite_table2(self, city, user_id):
        try:
            sqlite_connection = sqlite3.connect('base.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")

            sql_update_query = """Update users set city = ? where user_id = ?"""
            data = (city, user_id)
            cursor.execute(sql_update_query, data)
            sqlite_connection.commit()
            print("Запись успешно обновлена")
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    def update_isru(self, user_id, isru):
        try:
            sqlite_connection = sqlite3.connect('base.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")

            sql_update_query = """Update users set isru = ? where user_id = ?"""
            data = (isru, user_id)
            cursor.execute(sql_update_query, data)
            sqlite_connection.commit()
            print("Запись успешно обновлена")
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")
    




