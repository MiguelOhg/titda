from database.connection import database

table_name: str = 'its_plans'


def get_exercises():
    query = 'select mdl_vpl.* from mdl_vpl LEFT JOIN its_plans ON mdl_vpl.id = its_plans.exercise_id ' \
            'WHERE  shortdescription LIKE "%titda%" AND its_plans.id IS NULL'
    json = []
    cursor = database.cnx.cursor()
    cursor.execute(query)
    rv = cursor.fetchall()
    row_headers = [x[0] for x in cursor.description]
    for result in rv:
        json.append(dict(zip(row_headers, result)))
    cursor.close()
    return json


def get_one(plan_id):
    cursor = database.cnx.cursor()
    query = "select * from {} WHERE id = {}".format(table_name, plan_id)

    cursor.execute(query)
    print("Fetching single row")
    record = cursor.fetchone()
    print(record)

    print("Fetching next row")
    record = cursor.fetchone()
    print(record)

    cursor.close()
    return record


def get_one_by_attr(attr, value):
    query = "select * from {} WHERE {} = {} LIMIT 1".format(table_name, attr, value)
    json = []
    cursor = database.cnx.cursor()
    cursor.execute(query)
    rv = cursor.fetchall()
    row_headers = [x[0] for x in cursor.description]
    for result in rv:
        json.append(dict(zip(row_headers, result)))
    cursor.close()
    return json


def get_all():
    query = "select * from {}".format(table_name)
    json = []
    cursor = database.cnx.cursor()
    cursor.execute(query)
    rv = cursor.fetchall()
    row_headers = [x[0] for x in cursor.description]
    for result in rv:
        json.append(dict(zip(row_headers, result)))
    cursor.close()
    return json


def save(name, level, description, exercise_id):
    query = "INSERT INTO {} (name, level, description, exercise_id) VALUES (%s, %s, %s, %s)".format(table_name)
    values = [name, level, description, exercise_id]
    cursor = database.cnx.cursor()
    cursor.execute(query, values)
    database.cnx.commit()
    cursor.close()
    return cursor.rowcount


def update_plan(plan_id, goal_id, column):
    query = "UPDATE {} SET {}=%s WHERE id=%s".format(table_name, column)
    values = [goal_id, plan_id]
    cursor = database.cnx.cursor()
    cursor.execute(query, values)
    database.cnx.commit()
    cursor.close()
    return cursor.rowcount


def update(name, description, plan_id):
    query = "UPDATE {} SET name = %s, description = %s WHERE id = %s".format(table_name)
    values = [name, description, plan_id]
    cursor = database.cnx.cursor()
    cursor.execute(query, values)
    database.cnx.commit()
    cursor.close()
    return cursor.rowcount


def delete(plan_id):
    query = "DELETE FROM {} WHERE id = %s".format(table_name)
    values = [plan_id]
    cursor = database.cnx.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    cursor.execute(query, values)
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    database.cnx.commit()
    cursor.close()
    return cursor.rowcount
