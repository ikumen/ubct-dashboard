import logging
import json
import azure.functions as func

from support import db

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)-8s]: %(message)s')


insert_emoji_stmt = """
    INSERT INTO sl_emojis (id, url)
        (SELECT ?, ? WHERE NOT EXISTS (
            SELECT 1 FROM sl_emojis
            WHERE sl_emojis.id = ?
                AND sl_emojis.url = ?
        ))
"""

insert_files_stmt = """
    INSERT INTO sl_files (message_id, channel_id, url)
        (SELECT ?,?,? WHERE NOT EXISTS (
            SELECT 1 FROM sl_files
            WHERE sl_files.message_id = ?
                AND sl_files.channel_id = ?
                AND url = ?
        ))
"""

insert_reaction_stmt = """
    INSERT INTO sl_reactions (message_id, channel_id, user_id, emoji_id)
        (SELECT ?,?,?, ? WHERE NOT EXISTS (
            SELECT 1 FROM sl_reactions
            WHERE sl_reactions.message_id = ?
                AND sl_reactions.channel_id = ?
                AND sl_reactions.user_id = ?
                AND sl_reactions.emoji_id = ?
        ))
"""

insert_msg_stmt = """
    INSERT INTO sl_messages (id, channel_id, thread_id, user_id, content)
        (SELECT ?, ?, ?, ?, ? 
        WHERE NOT EXISTS (
            SELECT 1 FROM sl_messages 
            WHERE sl_messages.id = ? AND sl_messages.channel_id = ?))
"""

update_msg_stmt = """
    UPDATE sl_messages SET
        content = ?
     WHERE id = ?
"""

def _set_file_data(msg, file_data):
    for furl in msg.get('files', []):
        file_data.append((
            msg['id'], 
            msg['channel'], 
            furl, 
            msg['id'], 
            msg['channel'], 
            furl
        ))
    return file_data

def _set_react_data(msg, emoji_data, user_data):
    for emoji_id, emoji in msg.get('reactions', {}).items():
        emoji_data.append((
            emoji_id, 
            emoji['url'], 
            emoji_id, 
            emoji['url']
        ))

        for user in emoji.get('users',[]):
            user_data.append((
                msg['id'], 
                msg['channel'], 
                user, 
                emoji_id, 
                msg['id'], 
                msg['channel'], 
                user, 
                emoji_id
            ))
    return emoji_data, user_data


def load_messages(datastr):
    with db.get_conn() as conn:
        data = json.loads(datastr)
        with conn.cursor() as cursor:
            cursor.fast_executemany = True
            msg_data = []
            file_data = []
            react_emoji_data = []
            react_user_data = []
            i = len(data['inserts'])
            for msg in data['inserts']:
                #logging.info(f'Inserting channel: {channel}')
                logging.info(f"insert msg: {msg['id']}, {msg['channel']}")
                msg_data.append((
                    msg['id'], 
                    msg['channel'], 
                    msg['thread'], 
                    msg['user'], 
                    msg['content'], 
                    msg['id'], 
                    msg['channel']                    
                ))
                _set_file_data(msg, file_data)
                _set_react_data(msg, react_emoji_data, react_user_data)

                if len(msg_data) == 100 or i == 1:                
                    cursor.executemany(insert_msg_stmt, msg_data)
                    if file_data:
                        cursor.executemany(insert_files_stmt, file_data)
                    if react_emoji_data:
                        cursor.executemany(insert_emoji_stmt, react_emoji_data)
                    if react_user_data:
                        cursor.executemany(insert_reaction_stmt, react_user_data)
                    msg_data = []
                    file_data = []
                    react_emoji_data = []
                    react_user_data = []
                i -= 1
                
            msg_data = []
            file_data = []
            react_emoji_data = []
            react_user_data = []
            i = len(data['updates'])
            for msg in data['updates']: 
                logging.info(f"update msg: {msg['id']}, {msg['channel']}")
                msg_data.append((
                    msg['content'], 
                    msg['id']
                ))
                _set_file_data(msg, file_data)
                _set_react_data(msg, react_emoji_data, react_user_data)
                if len(msg_data) == 100 or i == 1:          
                    cursor.executemany(update_msg_stmt, msg_data)
                    if file_data:
                        cursor.executemany(insert_files_stmt, file_data)
                    if react_emoji_data:
                        cursor.executemany(insert_emoji_stmt, react_emoji_data)
                    if react_user_data:
                        cursor.executemany(insert_reaction_stmt, react_user_data)
                    msg_data = []
                    file_data = []
                    react_emoji_data = []
                    react_user_data = []
                i -= 1



def main(event: func.EventGridEvent, data):
    try:
        logging.info(f'loading data file {data.name}')
        load_messages(b''.join(data.readlines()))
    except Exception as e:
        logging.error(f'Unable to load channels. {e}')

