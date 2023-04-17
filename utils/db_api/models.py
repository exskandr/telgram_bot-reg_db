# import sqlite3
#
# # Створення таблиці з використанням змінних для підстановки даних
# create_table_query = '''
# CREATE TABLE IF NOT EXISTS users (
#     user_id INTEGER,
#     username TEXT,
#     first_name TEXT,
#     last_name TEXT,
#     f_i_o TEXT,
#     phone_number TEXT,
#     passport TEXT PRIMARY KEY,
#     number_of_people INTEGER,
#     status TEXT
# );
# '''
#
# # Виконання запиту на створення таблиці та збереження змін у базі даних
# with sqlite3.connect('pin_users.db') as conn:
#     cursor = conn.cursor()
#     cursor.execute(create_table_query)
#     conn.commit()
#     cursor.close()
#     conn.close()
#
#
