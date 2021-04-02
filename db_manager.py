import bcrypt
from psycopg2.extras import RealDictCursor
import db_common
import datetime


def get_submission_time():
    time = datetime.datetime.now()
    return time.strftime('%Y-%m-%d %H:%M:%S')


@db_common.connection_handler
def check_username_exists(cursor: RealDictCursor, username: str):
    query = """
        SELECT * FROM users
        WHERE username = %(username)s;
         """
    cursor.execute(query, {
        'username': username
    })
    return cursor.fetchone()


@db_common.connection_handler
def register_user(cursor: RealDictCursor, username: str, seen_password: str, submission_time: int):
    if check_username_exists(username):
        return False
    query = """
    INSERT INTO users (username, password, submission_time)
    VALUES (%(username)s, %(password)s, %(submission_time)s)
           """
    return cursor.execute(query, {
        'username': username,
        'password': encrypt_password(seen_password),
        'submission_time': submission_time
    })


def encrypt_password(password):
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pass.decode('utf-8')


@db_common.connection_handler
def get_user_details(cursor: RealDictCursor, username):
    query = """
    SELECT * FROM users
    WHERE username = %(username)s;
    """
    cursor.execute(query, {'username': username})
    cursor.fetchone()


@db_common.connection_handler
def check_user(cursor: RealDictCursor, username: str):
    query = """
        SELECT id, password
        FROM users
        WHERE username ILIKE %(username)s;
    """
    cursor.execute(query, {'username': username})
    return cursor.fetchone()


def verify_password(text_password, hashed_pass):
    return bcrypt.checkpw(text_password.encode('utf-8'), hashed_pass.encode('utf-8'))
