from database.connection import database


def run_trigger():
    cursor = database.cnx.cursor()
    cursor.execute("DROP TRIGGER IF EXISTS onchange_trigger")
    query_str = ('''
        CREATE TRIGGER onchange_trigger AFTER INSERT ON mdl_vpl_submissions FOR EACH ROW
        BEGIN
            DECLARE username_ VARCHAR(100);
            SELECT username INTO username_ FROM mld_user WHERE id = NEW.userid;
            IF username != 'admin' THEN
                INSERT INTO its_perceptions (input, status) 
                VALUES (CONCAT(NEW.vpl,'-',NEW.userid,'-',NEW.id), 'charged');
            END IF;
        END
    ''')
    cursor.execute(query_str)
    database.cnx.commit()


