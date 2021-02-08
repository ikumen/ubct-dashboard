import fn_load_users, fn_load_channels

# TODO cli
with open('../tests/data/users.json') as file:
    fn_load_users.load_users(file)

with open('../tests/data/channels.json') as file:
    fn_load_channels.load_channels(file)