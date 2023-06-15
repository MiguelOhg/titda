from database.connection import database

table_name = 'its_goals'


def run_migrations():
    cursor = database.cnx.cursor()
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS `{}` (
           `id` bigint NOT NULL AUTO_INCREMENT,
           `name` varchar(100) DEFAULT NULL,
           `description` varchar(255) DEFAULT NULL,
           `goal_id` bigint NOT NULL, 
            PRIMARY KEY (`id`),
            FOREIGN KEY (`goal_id`) REFERENCES its_goals(`id`)
       ) ENGINE=InnoDB
       '''.format(table_name))
    database.cnx.commit()


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


def get_one(goal_id):
    query = "select * from {} where id = {}".format(table_name, goal_id)
    json = []
    cursor = database.cnx.cursor()
    cursor.execute(query)
    rv = cursor.fetchall()
    row_headers = [x[0] for x in cursor.description]
    for result in rv:
        json.append(dict(zip(row_headers, result)))
    cursor.close()
    return json


def save(name, description, goal_id):
    query = "INSERT INTO {} (name, description, goal_id) VALUES (%s, %s, %s)".format(table_name)
    values = [name, description, goal_id]
    cursor = database.cnx.cursor()
    cursor.execute(query, values)
    database.cnx.commit()
    cursor.close()
    return cursor.lastrowid


def update(name, description, goal_id):
    query = "UPDATE {} SET name = %s, description = %s WHERE id = %s".format(table_name)
    values = [name, description, goal_id]
    cursor = database.cnx.cursor()
    cursor.execute(query, values)
    database.cnx.commit()
    cursor.close()
    return cursor.rowcount


def delete(goal_id):
    query = "DELETE FROM {} WHERE id = %s".format(table_name)
    values = [goal_id]
    cursor = database.cnx.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    cursor.execute(query, values)
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    database.cnx.commit()
    cursor.close()
    return cursor.rowcount
