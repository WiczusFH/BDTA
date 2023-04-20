from telethon.errors import ChannelPrivateError
from telethon.sync import TelegramClient as SyncTelegramClient
from data_access.RedisAccess import RedisAccess
from validation_telegram import validate

api_id = 26555779
api_hash = 'eb302d2bbb1767656d7485a6b729b6e2'
phone_number = '+4368110596446'

ra = RedisAccess()
target_year=2022
target_channel="KyivIndependent_official"
db_idx="telegram"
with SyncTelegramClient('anon', api_id, api_hash) as client:
    """Potentially needs to log in"""
    client.start(phone=phone_number)
    try:
        channel = client.get_entity(target_channel)
        """Iterate through messages, validate and reformat text to fit the tokenization process. """
        for message in client.iter_messages(channel):
            if message.date.year == target_year:
                # print(message.date) # slow in python uncomment to see progress.
                if validate(message):
                    ra.persist_raw(db_idx, message.date.strftime('%Y%m%d'), message.text)
            elif message.date.year < target_year:
                break

    except ChannelPrivateError:
        print('The channel is private and you do not have access to it.')

