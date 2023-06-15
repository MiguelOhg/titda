from database.connection import database

table_name = 'its_perceptions'


def insert_all():
    query = "INSERT IGNORE INTO its_perceptions (input) " \
        "SELECT CONCAT(mdl_vpl_submissions.vpl,'-', mdl_vpl_submissions.userid,'-',mdl_vpl_submissions.id)" \
        "FROM mdl_vpl_submissions"

    cursor = database.cnx.cursor()
    cursor.execute(query)
    database.cnx.commit()
    cursor.close()
    return cursor.rowcount


def get_all():
    query = "select * from {} where status = 'charged'".format(table_name)
    json = []
    cursor = database.cnx.cursor()
    cursor.execute(query)
    rv = cursor.fetchall()
    row_headers = [x[0] for x in cursor.description]
    for result in rv:
        json.append(dict(zip(row_headers, result)))
    cursor.close()
    return json


def get_one(_id):
    query = "select * from {} where id = {}".format(table_name, _id)
    json = []
    cursor = database.cnx.cursor()
    cursor.execute(query)
    rv = cursor.fetchall()
    row_headers = [x[0] for x in cursor.description]
    for result in rv:
        json.append(dict(zip(row_headers, result)))
    cursor.close()
    return json


def save(input):
    query = "INSERT INTO {} (input, status) VALUES (%s, 'charged')".format(table_name)
    values = input
    cursor = database.cnx.cursor()
    cursor.execute(query, values)
    database.cnx.commit()
    cursor.close()
    return cursor.rowcount


def update(input, status, perception_id):
    query = "UPDATE {} SET input = %s, status = %s WHERE id = %s".format(table_name)
    values = [input, status, perception_id]
    cursor = database.cnx.cursor()
    cursor.execute(query, values)
    database.cnx.commit()
    cursor.close()
    return cursor.rowcount


def delete(_id):
    query = "DELETE FROM {} WHERE id = ?".format(table_name, _id)
    cursor = database.cnx.cursor()
    cursor.execute(query)
    database.cnx.commit()
    cursor.close()
    return cursor.rowcount
