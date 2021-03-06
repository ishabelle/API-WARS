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


# @db_common.connection_handler
# def vote_planet_by_planet_name(cursor: RealDictCursor, new_data: dict, user):
#     query = '''
#         INSERT INTO planet_votes (planet_id, planet_name, user_id, submission_time)
#         VALUES (%(planet_id)s, %(planet_name)s, %(user_id)s, now())
#     '''
#     cursor.execute(query, {'planet_id': new_data['planet_id'],
#                            'planet_name': new_data['planet_name'],
#                            'user_id': new_data['user_id']
#                            'user': user
#                            })


@db_common.connection_handler
def vote_planet_by_planet_name(cursor: RealDictCursor, planet_id, planet_name, user_id, submission_time):
    query = '''
        INSERT INTO planet_votes (planet_id, planet_name, user_id, submission_time) 
        VALUES (%(planet_id)s, %(planet_name)s, %(user_id)s, %(submission_time)s) 
    '''
    cursor.execute(query, {'planet_id': planet_id,
                           'planet_name': planet_name,
                           'user_id': user_id,
                           'submission_time': submission_time
                           })


@db_common.connection_handler
def get_vote_statistics(cursor: RealDictCursor):
    query = """
    SELECT planet_name, COUNT(planet_id) AS recived_votes FROM planet_votes
    GROUP BY planet_name
    """
    cursor.execute(query)
    return cursor.fetchall()
