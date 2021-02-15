import logging
import json
import azure.functions as func

from support import db

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)-8s]: %(message)s')

def load_users(datastr):
    insert_user_stmt = """
        INSERT INTO sl_users (id, name, full_name, description, avatar_id, tz_offset, archived_at)
            (SELECT ?, ?, ?, ?, ?, ?, getdate()
         WHERE NOT EXISTS (SELECT id FROM sl_users WHERE sl_users.id = ?))
    """
    
    update_user_stmt = """
        UPDATE sl_users SET
            name = ?,
            full_name = ?,
            description = ?,
            tz_offset = ?
         WHERE id = ?
    """
    
    with db.get_conn() as conn:
        data = json.loads(datastr)
        for user in data['inserts']:
            #logging.info(f'Inserting user: {user}')
            with conn.cursor() as cursor:
                cursor.execute(insert_user_stmt, 
                    user['id'],
                    user['name'],
                    user['fullName'],
                    user['title'],
                    user['avatarId'],
                    user['offset'],
                    user['id'])

        for user in data['updates']:
            with conn.cursor() as cursor:
                cursor.execute(update_user_stmt,
                    user['name'],
                    user['fullName'],
                    user['title'],
                    user['offset'],
                    user['id'])


def main(event: func.EventGridEvent, data):
    try:
        logging.info(f'loading data file {data.name}')
        load_users(b''.join(data.readlines()))
    except Exception as e:
        logging.error(f'Unable to load users. {e}')