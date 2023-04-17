import logging
import aiosqlite

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def db_connect():
    conn = await aiosqlite.connect('pin_users.db')
    logging.info("Connected to database")
    return conn


async def db_close(conn):
    await conn.close()
    logging.info("Database connection closed")


async def create_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        f_i_o TEXT,
        phone_number TEXT,
        passport TEXT PRIMARY KEY,
        number_of_people INTEGER,
        status TEXT);
    '''
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(create_table_query)
        await conn.commit()
        logging.info("database created")
    except aiosqlite.Error as error:
        logging.error("Error while connecting to SQLite: %s", error)
    finally:
        await db_close(conn)


async def db_add_user(user_id, username, first_name, last_name, f_i_o, phone_number, passport, num_of_people, status):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(
            'INSERT INTO users '
            '(user_id, username, first_name, last_name, f_i_o, phone_number, passport, number_of_people, status) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (user_id, username, first_name, last_name, f_i_o, phone_number, passport, num_of_people, status))
        await conn.commit()
        logging.info("Data added to database")
    except aiosqlite.Error as error:
        logging.error("Error while connecting to SQLite: %s", error)
    finally:
        await db_close(conn)


async def select_user(passport):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute('SELECT ROWID FROM users WHERE passport = ?', (passport,))
        selectuser = await cursor.fetchone()
        logging.info("Selected user: %s", selectuser)
        return selectuser[0] if selectuser else None
    except aiosqlite.Error as error:
        logging.error("Error while connecting to SQLite: %s", error)
    finally:
        await db_close(conn)


async def select_last_in_line():
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        sqlite_select_query = """SELECT count(*) from users"""
        await cursor.execute(sqlite_select_query)
        total_rows = await cursor.fetchone()
        logging.info("Number of records: %s", total_rows)
        return total_rows[0] if total_rows else None
    except aiosqlite.Error as error:
        logging.error("Error while connecting to SQLite: %s", error)
    finally:
        await db_close(conn)


async def next_in_line():
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        select_last_status_pass = """SELECT ROWID FROM users WHERE status = "PASS" ORDER BY ROWID DESC LIMIT 1"""
        await cursor.execute(select_last_status_pass)
        row = await cursor.fetchone()
        next_row = row[0] + 1  # збільшуємо значення на 1
        await cursor.execute("SELECT f_i_o, ROWID FROM users WHERE ROWID = ? ORDER BY ROWID DESC LIMIT 1", (next_row,))
        total_rows = await cursor.fetchone()
        logging.info("Number of records: %s", total_rows)
        return total_rows if total_rows else None
    except aiosqlite.Error as error:
        logging.error("Error while connecting to SQLite: %s", error)
    finally:
        await db_close(conn)


async def update_status(number):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute('UPDATE Users SET Status="PASS" WHERE ROWID = ?', (number,))
        await conn.commit()
        text = "Status of number in line %s was change", (number,)
        logging.info(text)
        return text if text else "number in line not found"
    except aiosqlite.Error as error:
        logging.error("Error while connecting to SQLite: %s", error)
    finally:
        await db_close(conn)
