import redis
from django.conf import settings

redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=int(settings.REDIS_PORT),
    db=0,
    decode_responses=True, # for string
)
