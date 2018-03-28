import os
from sqlalchemy import create_engine
import psycopg2

DATABASE_URL = os.environ["DATABASE_URL"]

def update_sql_query(no_of_words, sql, name):
    """
    Args:
    no_of_words: no of words in name
    sql: sql query for the request (needs three "%s"'s)
    """
    if no_of_words == 1:
        col_name = "firstname"
        sql = sql % (col_name, col_name, "'"+name+"'")

    elif no_of_words == 2:
        col_name = "name"
        sql = sql % (col_name, col_name, "'"+name+"'")

    return sql


def run_query(command, type):
    # connect to db
    # db = psycopg2.connect(DATABASE_URL, sslmode='require')
    db = create_engine(DATABASE_URL)
    c = db.connect()
    # c = db.cursor()

    # parse name from command
    no_of_words = len(command.split(" ")[1:])
    name = command.split(" ", 1)[1]

    if name:
        if type == "who":
            sql = """
                SELECT %s, committee, committeeRole, company, dayjob, tag
                FROM volunteer_info
                WHERE %s=%s
                """
            updated_sql = update_sql_query(no_of_words, sql, name)
        elif type == "get":
            sql = """
                SELECT %s, email, phone, gender
                FROM volunteer_info
                WHERE %s=%s
                """
            updated_sql = update_sql_query(no_of_words, sql, name)

        query = c.execute(updated_sql)
        results = query.fetchall()
        return results
    else:
        print("Not so smart, eh? Check your spelling and come again!")