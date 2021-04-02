from psycopg2.extras import RealDictCursor
import db_common


@db_common.connection_handler
def check_exists_username(cursor: RealDictCursor, username):
    query = """
    SELECT * FROM users
    WHERE username = %(username)s;
    """
    cursor.execute(query, {"username": username})
    return cursor.fetchone()


@db_common.connection_handler
def add_user(cursor: RealDictCursor, new_user):
    if check_exists_username(new_user["username"]):
        return False
    else:
        query = """
        INSERT INTO users (username, password, submission_time)
        VALUES (%s, %s, now());
        """
        cursor.execute(query, (new_user["username"], new_user["password"]))


@db_common.connection_handler
def get_user_details(cursor: RealDictCursor, username):
    query = """
    SELECT * FROM users
    WHERE username = %(username)s;
    """
    cursor.execute(query, {'username': username})
    cursor.fetchone()
