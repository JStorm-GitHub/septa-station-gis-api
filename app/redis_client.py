### This is a redis client instance that allows cross-instance compatibility

import redis

r = redis.Redis(host="redis", port=6379, decode_responses=True)
