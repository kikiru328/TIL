### redis container
```bash
docker run -p 6379:6379 --name redis -d --rm redis
```

### python console
```python
>>> import redis
>>> redis_client = redis.Redis(host="127.0.0.1", port=6379, db=0, encoding="UTF-8", decode_responses=True)
# remote dictionary server ## hashmap type

>>> redis_client.set("key", "value")
True
>>> redis_client.get("key")
"value"
>>> redis_client.expire("key", 10)
# 10초만 가지고 있겠다.

```
