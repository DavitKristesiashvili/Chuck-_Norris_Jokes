import sqlite3
from sqlite3 import Error
import requests


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "Chuck_Norris.db"

    sql_create_chuck_jokes = """
                                    CREATE TABLE IF NOT EXISTS jokes ( 
                                    id text NOT NULL, 
                                    categories text NOT NULL, 
                                    icon_url text NOT NULL, 
                                    created_at text NOT NULL, 
                                    updated_at text NOT NULL, 
                                    url text NOT NULL, 
                                    joke text NOT NULL
                                    );
                                   """
    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_chuck_jokes)
    else:
        print("Error!")


def insert_jokes(conn, joke):
    sql_insert_jokes = '''
                           INSERT INTO jokes(id, categories, icon_url, created_at, updated_at, url, joke)
                           VALUES(?,?,?,?,?,?,?)
                           '''

    try:
        c = conn.cursor()
        c.execute(sql_insert_jokes, joke)
        conn.commit()

        return True

    except Error as e:
        print(e)


def main_insert():
    database = r"Chuck_Norris.db"

    conn = create_connection(database)
    with conn:
        for i in range(100):
            url = "https://api.chucknorris.io/jokes/random"
            response = requests.get(url).json()
            cat = response["categories"]
            cre_at = response["created_at"]
            icon_url = response["icon_url"]
            id = response["id"]
            upd_at = response["updated_at"]
            url = response["url"]
            joke = response["value"]
            insert_jokes(conn, (id, str(cat), icon_url, cre_at, upd_at, url, joke))


def select_jokes(conn):
    sql_select_jokes = """
                        SELECT * from jokes WHERE LENGTH(joke) > 10 
                        """

    try:
        c = conn.cursor()
        c.execute(sql_select_jokes)
        conn.commit()

        return True

    except Error as e:
        print(e)


def main_select():
    database = r"Chuck_Norris.db"

    conn = create_connection(database)
    with conn:
        select_jokes(conn)



if __name__ == '__main__':
    main_select()
