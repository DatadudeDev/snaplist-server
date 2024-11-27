# lib/utilities/dbAdmin.py

import sqlite3
from sqlite3 import Error
import os

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection established to database.")
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    """ create a table """
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS metrics (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     userRef TEXT NOT NULL,
                     requestType TEXT NOT NULL,
                     imageGenerated TEXT NOT NULL,
                     startTime TEXT NOT NULL,
                     endTime TEXT NOT NULL,
                     runtime FLOAT NOT NULL);''')
        print("Table created successfully.")
    except Error as e:
        print(e)

def insert_metrics(conn, metrics):
    """Insert a new row into the metrics table"""
    sql = ''' INSERT INTO metrics(userRef,requestType,imageGenerated,startTime,endTime,runtime)
              VALUES(?,?,?,?,?,?) '''
    try:
        c = conn.cursor()
        c.execute(sql, metrics)
        conn.commit()
        print("New metric inserted successfully.")
    except Error as e:
        print(e)

def dbAdmin(userRef, requestType, imageGenerated, startTime, endTime, runtime):
    database = "./data/Metrics/performance.db"
    os.makedirs(os.path.dirname(database), exist_ok=True)

    # create a database connection
    conn = create_connection(database)
    with conn:
        create_table(conn)
        metrics = (userRef, requestType, imageGenerated, startTime, endTime, runtime)
        insert_metrics(conn, metrics)

if __name__ == '__main__':
    print("This script is intended to be imported, not run directly.")
