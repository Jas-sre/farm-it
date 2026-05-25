import os
import mysql.connector

DB_CONFIG = {
    'host': os.getenv('FARMIT_DB_HOST', 'localhost'),
    'user': os.getenv('FARMIT_DB_USER', 'root'),
    'password': os.getenv('FARMIT_DB_PASSWORD', ''),
    'database': os.getenv('FARMIT_DB_NAME', 'farmit')
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_all(query, values=()):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, values)
    result = cursor.fetchall()
    conn.close()
    return result


def execute_query(query, values=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    conn.close()
