import MySQLdb

def conn():
    return MySQLdb.connect("127.0.0.1", "root", "root", "blogs")

def execute_sql_query(query):
    db = conn()
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result
