import redis

redis_client_local = redis.StrictRedis(host='localhost', port=6379, db=1)

def load_from_redis(key):
    return redis_client_local.get(key)