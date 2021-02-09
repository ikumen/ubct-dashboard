import logging
import json
import azure.functions as func

from support import db

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)-8s]: %(message)s')

def load_channels(data):
    insert_user_stmt = """
        INSERT INTO sl_channels (id, name, description, archived_at)
          (SELECT ?, ?, ?, getdate()
           WHERE NOT EXISTS (SELECT id FROM sl_channels WHERE sl_channels.id = ?))
    """
    with db.get_conn() as conn:
        for channel in json.loads(b''.join(data.readlines())):
            #logging.info(f'Inserting channel: {channel}')
            with conn.cursor() as cursor:
                cursor.execute(insert_user_stmt, 
                    channel['id'],
                    channel['name'],
                    channel['description'],
                    channel['id']
                )


def main(event: func.EventGridEvent, data):
    try:
        logging.info(f'loading data file {data.name}')
        load_channels(data)
    except Exception as e:
        logging.error(f'Unable to load channels. {e}')

