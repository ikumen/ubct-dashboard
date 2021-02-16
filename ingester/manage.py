import os
import fn_load_messages
import fn_load_users, fn_load_channels


def import_data(source, archive, fn):
    for fname in os.listdir(source):
        fpath = f'{source}/{fname}'
        with open(fpath) as file:
            fn(''.join(file.readlines()))
            os.rename(fpath, f'{archive}/{fname}')

import_data(
    source='../production/channels', 
    archive='../production/archive/channels', 
    fn=fn_load_channels.load_channels)

import_data(
    source='../production/users', 
    archive='../production/archive/users', 
    fn=fn_load_users.load_users)

import_data(
    source='../production/messages', 
    archive='../production/archive/messages', 
    fn=fn_load_messages.load_messages)