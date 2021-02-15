import logging
import json
import azure.functions as func

from support import db

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)-8s]: %(message)s')

def load_channels(datastr):
    insert_channel_stmt = """
        INSERT INTO sl_channels (id, name, description, archived_at)
          (SELECT ?, ?, ?, getdate()
           WHERE NOT EXISTS (SELECT id FROM sl_channels WHERE sl_channels.id = ?))
    """

    update_channel_stmt = """
        UPDATE sl_channels SET
            name = ?,
            description = ?
         WHERE id = ?
    """

    with db.get_conn() as conn:
        data = json.loads(datastr)
        for channel in data['inserts']:
            #logging.info(f'Inserting channel: {channel}')
            with conn.cursor() as cursor:
                cursor.execute(insert_channel_stmt, 
                    channel['id'],
                    channel['name'],
                    channel['description'],
                    channel['id']
                )

        for channel in data['updates']:
            with conn.cursor() as cursor:
                cursor.execute(update_channel_stmt,
                    channel['name'],
                    channel['description'],
                    channel['id']
                )

def main(event: func.EventGridEvent, data):
    try:
        logging.info(f'loading data file {data.name}')
        load_channels(b''.join(data.readlines()))
    except Exception as e:
        logging.error(f'Unable to load channels. {e}')

