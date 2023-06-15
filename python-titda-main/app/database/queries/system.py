from database.connection import database

table_name = 'mdl_course_modules_completion'
table_name_mld_vpl = 'mdl_vpl'
table_name_revision = 'its_revisions'
table_name_responses = 'its_responses'


def save(coursemoduleid, userid, completionstate, timemodified):
    query_verify = "SELECT id FROM {} WHERE coursemoduleid=%s and userid=%s LIMIT 0, 1".format(
        table_name)
    values = [coursemoduleid, userid]
    cursor = database.cnx.cursor(buffered=True)
    cursor.execute(query_verify, values)

    if cursor.rowcount:
        query = "UPDATE {} SET completionstate=%s, timemodified=%s WHERE userid=%s and coursemoduleid=%s ".format(
            table_name)
        values = [completionstate, timemodified, userid, coursemoduleid]
        cursor.execute(query, values)
        database.cnx.commit()
        cursor.close()
    else:
        query = "INSERT INTO {} (coursemoduleid, userid, completionstate, timemodified) VALUES (%s, %s, %s, %s)".format(
            table_name)
        values = [coursemoduleid, userid, completionstate, timemodified]
        cursor.execute(query, values)
        database.cnx.commit()
        cursor.close()
    return cursor.rowcount


def save_response(exercise_id, user_id, archive_id):
    query_verify = "SELECT id FROM {} WHERE exercise_id=%s and user_id=%s and archive_id=%s LIMIT 0,1".format(
        table_name_responses)
    values = [exercise_id, user_id, archive_id]
    cursor = database.cnx.cursor(buffered=True)
    cursor.execute(query_verify, values)

    if not cursor.rowcount:
        query = "INSERT INTO {} (exercise_id, user_id, archive_id) VALUES (%s, %s, %s)".format(
            table_name_responses)
        values = [exercise_id, user_id, archive_id]
        cursor = database.cnx.cursor()
        cursor.execute(query, values)
        database.cnx.commit()
        cursor.close()

    return cursor.lastrowid


def update_response(response_id, status, log):
    query = "UPDATE {} SET status=%s, log=%s WHERE id=%s".format(
        table_name_responses)
    values = [status, log, response_id]
    cursor = database.cnx.cursor()
    cursor.execute(query, values)
    database.cnx.commit()
    cursor.close()


def save_revision(response_id, action_id, procedural_memory_id, value, response_from_its):
    query_verify = "SELECT id FROM {} WHERE response_id=%s and action_id=%s and procedural_memory_id=%s LIMIT 0, 1"\
        .format(table_name_revision)
    values = [response_id, action_id, procedural_memory_id]
    cursor = database.cnx.cursor(buffered=True)
    cursor.execute(query_verify, values)

    if cursor.rowcount:
        query = f"UPDATE {table_name_revision} SET value=%s, response_from_its=%s " \
                f"WHERE response_id=%s and action_id=%s and procedural_memory_id=%s"
        values = [value, response_from_its, response_id, action_id, procedural_memory_id]
        cursor = database.cnx.cursor()
        cursor.execute(query, values)
        database.cnx.commit()
        cursor.close()
    else:
        query = "INSERT IGNORE INTO {} (response_id, action_id, procedural_memory_id, value, response_from_its) " \
                "VALUES (%s, %s, %s, %s, %s)".format(table_name_revision)
        values = [response_id, action_id, procedural_memory_id, value, response_from_its]
        cursor = database.cnx.cursor()
        cursor.execute(query, values)
        database.cnx.commit()
        cursor.close()
    return cursor.rowcount


def get_responses():
    query = "SELECT mdl_user.username, mdl_vpl.name, COUNT(DISTINCT its_responses.id) AS attempts," \
            " SUM(IF(its_responses.status = 'fail', 1, 0)) as errors" \
            " FROM its_responses " \
            " INNER JOIN mdl_user ON mdl_user.id = its_responses.user_id" \
            " INNER JOIN mdl_vpl ON mdl_vpl.id = its_responses.exercise_id" \
            " INNER JOIN mdl_course_modules_completion ON mdl_course_modules_completion.userid = its_responses.user_id" \
            " GROUP BY mdl_user.username, mdl_vpl.name"
    json = []
    cursor = database.cnx.cursor()
    cursor.execute(query)
    rv = cursor.fetchall()
    row_headers = [x[0] for x in cursor.description]
    for result in rv:
        json.append(dict(zip(row_headers, result)))
    cursor.close()
    return json


def get_responses_student(id):
    query = "SELECT its_responses.exercise_id, mdl_user.username, mdl_vpl.name, " \
            " COUNT(DISTINCT its_responses.id) as attempts," \
            " (SELECT COUNT(DISTINCT id) FROM its_revisions WHERE response_id = its_responses.id AND " \
            " its_revisions.response_from_its != 'done')  AS errors" \
            " FROM its_responses " \
            " INNER JOIN mdl_user ON mdl_user.id = its_responses.user_id" \
            " INNER JOIN mdl_vpl ON mdl_vpl.id = its_responses.exercise_id" \
            " WHERE mdl_user.id = %s " \
            " GROUP BY its_responses.id, its_responses.exercise_id, mdl_user.username, mdl_vpl.name " \
            " ORDER BY its_responses.exercise_id DESC"
    values = [id]
    json = []
    cursor = database.cnx.cursor()
    cursor.execute(query, values)
    rv = cursor.fetchall()
    row_headers = [x[0] for x in cursor.description]
    for result in rv:
        json.append(dict(zip(row_headers, result)))
    cursor.close()
    return json


def get_responses_extended_student(exercise_id, id):
    query = "SELECT its_actions.name, its_revisions.response_from_its" \
            " FROM its_actions " \
            " INNER JOIN its_revisions ON its_revisions.action_id = its_actions.id" \
            " INNER JOIN its_responses ON its_responses.id = its_revisions.response_id" \
            " WHERE its_responses.exercise_id = %s AND its_responses.user_id = %s" \
            " GROUP BY its_actions.name, its_revisions.response_from_its"
    values = [exercise_id, id]
    json = []
    cursor = database.cnx.cursor()
    cursor.execute(query, values)
    rv = cursor.fetchall()
    row_headers = [x[0] for x in cursor.description]
    for result in rv:
        json.append(dict(zip(row_headers, result)))
    cursor.close()
    return json


def get_course_id(vpl, user):
    query = "SELECT mdl_course_modules.id " \
            " FROM mdl_course_modules " \
            " INNER JOIN mdl_vpl_submissions ON mdl_vpl_submissions.vpl = mdl_course_modules.instance" \
            " WHERE mdl_course_modules.module = 25 AND mdl_vpl_submissions.vpl = %s " \
            " AND mdl_vpl_submissions.userid = %s LIMIT 0,1"
    values = [vpl, user]
    json = []
    cursor = database.cnx.cursor()
    cursor.execute(query, values)
    rv = cursor.fetchall()
    row_headers = [x[0] for x in cursor.description]
    for result in rv:
        json.append(dict(zip(row_headers, result)))
    cursor.close()
    return json
