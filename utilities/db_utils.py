import psycopg2
from flask import request


def create_connection():
    conn = psycopg2.connect(
        host="tam-postgres.postgres.database.azure.com",
        database="postgres",
        # user='postgres',
        user="postgres@tam-postgres",
        password='Tamana@19',
        port=5432)
    return conn


def execute_query(query):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    if request.method == "GET":
        result = cur.fetchall()
        conn.close()
        return result
    conn.close()

