from database.connection import database

table_name = 'its_discrepancies'


def get_all(plan_id):
    query = "select * from {} where plan_id = {}".format(table_name, plan_id)
    json = []
    cursor = database.cnx.cursor()
    cursor.execute(query)
    rv = cursor.fetchall()
    row_headers = [x[0] for x in cursor.description]
    for result in rv:
        json.append(dict(zip(row_headers, result)))
    cursor.close()
    return json


def get_one(discrepancy_id):
    query = "select * from {} where id = {}".format(table_name, discrepancy_id)
    json = []
    cursor = database.cnx.cursor()
    cursor.execute(query)
    rv = cursor.fetchall()
    row_headers = [x[0] for x in cursor.description]
    for result in rv:
        json.append(dict(zip(row_headers, result)))
    cursor.close()
    return json


def save(description, discrepancy_id):
    query = "INSERT INTO {} (description, discrepancy_id) VALUES (%s, %s)".format(table_name)
    values = [description, discrepancy_id]
    cursor = database.cnx.cursor()
    cursor.execute(query, values)
    database.cnx.commit()
    cursor.close()
    return cursor.lastrowid


def update(description, discrepancy_id):
    query = "UPDATE {} SET description = %s WHERE id = %s".format(table_name)
    values = [description, discrepancy_id]
    cursor = database.cnx.cursor()
    cursor.execute(query, values)
    database.cnx.commit()
    cursor.close()
    return cursor.rowcount


def delete(discrepancy_id):
    query = "DELETE FROM {} WHERE id = %s".format(table_name)
    values = [discrepancy_id]
    cursor = database.cnx.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    cursor.execute(query, values)
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    database.cnx.commit()
    cursor.close()
    return cursor.rowcount
