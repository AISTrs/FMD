import os

import pandas as pd
import psycopg2


def get_connection():
    conn = psycopg2.connect(
        dbname=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT')
    )

    return conn


def get_transaction_category(cur):
    table_query = "Select * from transaction_category;"
    cur.execute(table_query)
    data = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    df = pd.DataFrame(data, columns=columns)
    return df


def validate_batch_number(cur, table, batch_id):
    table_query = f"Select count(*) from {table} where batch_id = {batch_id};"
    cur.execute(table_query)
    result = cur.fetchall()
    if result[0][0] > 0:
        raise SystemExit("Error: Batch number exists! Please try other batch number.")


def get_fiscal_id(cur, semester):
    table_query = f"Select id, semester from fiscal_term where semester='{semester}';"
    cur.execute(table_query)
    result = cur.fetchall()
    if result:
        return result[0][0]

    raise SystemExit("Error: Invalid semester data! Please try with a valid semester.")


def get_max_batch_number(cur, table):
    table_query = f"Select max(batch_id) from {table};"
    cur.execute(table_query)
    result = cur.fetchall()

    return result[0][0] if result[0][0] is not None else 0
