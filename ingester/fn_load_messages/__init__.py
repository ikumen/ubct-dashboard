import logging
import json
import azure.functions as func

from support import db

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)-8s]: %(message)s')

def load_newmessages(data):
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
    with db.get_conn() as conn:
        for msg in json.loads(data):
            #logging.info(f'Inserting channel: {channel}')
            with conn.cursor() as cursor:
                logging.info(f"insert msg: {msg['id']}, {msg['channel']}")
                cursor.execute(insert_msg_stmt, 
                    msg['id'],
                    msg['channel'],
                    msg['thread'],
                    msg['user'],
                    msg['content'],
                    msg['id'],
                    msg['channel']
                )
                for f in msg.get('files', []):
                    logging.info(f"insert file: {msg['id']}, {msg['channel']}, {f}")
                    cursor.execute(insert_files_stmt,
                        msg['id'],
                        msg['channel'],
                        f,
                        msg['id'],
                        msg['channel'],
                        f
                    )
                for emoji_id, emoji in msg.get('reactions', {}).items():
                    logging.info(f"insert emoji: {emoji_id}, {emoji['url']}")
                    cursor.execute(insert_emoji_stmt,
                        emoji_id,
                        emoji['url'],
                        emoji_id,
                        emoji['url']
                    )

                    for user in emoji.get('users',[]):
                        logging.info(f"insert reaction: {msg['id']}, {msg['channel']}, {user}, {emoji_id}")
                        cursor.execute(insert_reaction_stmt,
                            msg['id'],
                            msg['channel'],
                            user,
                            emoji_id,
                            msg['id'],
                            msg['channel'],
                            user,
                            emoji_id
                        )


def main(event: func.EventGridEvent, data):
    try:
        logging.info(f'loading data file {data.name}')
        load_newmessages(b''.join(data.readlines()))
    except Exception as e:
        logging.error(f'Unable to load channels. {e}')

