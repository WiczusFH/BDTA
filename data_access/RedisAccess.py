import redis

class RedisAccess:
    def __init__(self, host='localhost', port=6379, db=0):
        self.raw_db = redis.Redis(host=host, port=port, db=db, decode_responses=True, charset='utf-8')

    def persist_raw(self, source, date, text):
        key_count = len(self.raw_db.keys(f"{source}:{date}*"))
        self.raw_db.set(f"{source}:{date}:{key_count}",text)

