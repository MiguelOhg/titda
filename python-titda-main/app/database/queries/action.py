from database.connection import database

table_name = 'its_actions'


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


def get_one(action_id):
    query = "select * from {} where id = {}".format(table_name, action_id)
    json = []
    cursor = database.cnx.cursor()
    cursor.execute(query)
    rv = cursor.fetchall()
    row_headers = [x[0] for x in cursor.description]
    for result in rv:
        json.append(dict(zip(row_headers, result)))
    cursor.close()
    return json


def save(name, description, type, value, plan_id, procedural_memory_id):
    query = f"INSERT INTO {table_name} (name, description, type, value, plan_id, procedural_memory_id) VALUES " \
            f"(%s, %s, %s, %s, %s, %s)"
    values = [name, description, type, value, plan_id, procedural_memory_id]
    cursor = database.cnx.cursor()
    cursor.execute(query, values)
    database.cnx.commit()
    cursor.close()
    return cursor.rowcount


def update(name, description, type, value, action_id):
    query = "UPDATE {} SET name = %s, description = %s, type = %s, value = %s WHERE id = %s".format(table_name)
    values = [name, description, type, value, action_id]
    cursor = database.cnx.cursor()
    cursor.execute(query, values)
    database.cnx.commit()
    cursor.close()
    return cursor.rowcount


def delete(action_id):
    query = "DELETE FROM {} WHERE id = %s".format(table_name)
    values = [action_id]
    cursor = database.cnx.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    cursor.execute(query, values)
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    database.cnx.commit()
    cursor.close()
    return cursor.rowcount
