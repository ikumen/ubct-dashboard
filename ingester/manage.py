import fn_load_messages
import fn_load_users, fn_load_channels

# TODO cli
# with open('../tests/data/users.json') as file:
#     fn_load_users.load_users(''.join(file.readlines()))

# with open('../tests/data/channels.json') as file:
#     fn_load_channels.load_channels(''.join(file.readlines()))

with open('../tests/data/newmessages.json') as file:
    fn_load_messages.load_newmessages(''.join(file.readlines()))    