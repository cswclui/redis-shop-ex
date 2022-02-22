#sample program for redis py
#Redis-py Doc: https://redis-py.readthedocs.io/en/stable/index.html

import redis
from pprint import pprint 

r = redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True)

#Redis string
r.set("message","hello")
msg = r.get("message")
print(type(msg))
print(msg)

#Redis Set
r.sadd("books","book1")
r.sadd("books","book2")
r.sadd("books","book3")
books = r.smembers("books")
print(type(books))
pprint(books)

#Redis Sorted Set
r.zadd("game_score",{"Peter":100})
r.zadd("game_score",{"Alice":80})
scores = r.zrange("game_score",0,-1, withscores=True)
print(type(scores))
pprint(scores)

#Redis Hash
r.hset("marks", key="Alice", value=30)
r.hset("marks", key="Bob", value=50)
r.hset("marks", key="Carol", value=99)
all_marks=r.hgetall("marks")
print(type(all_marks))
pprint(all_marks)
