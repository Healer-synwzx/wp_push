import uuid
import time
import math
import redis
from redis import Redis

from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB


class RedisUtil:

    def __init__(self):
        self.redis = Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=REDIS_DB
        )

    def set_scaned_flag(self, unique_id, openid, exp=1800):
        if isinstance(openid, bytes):
            openid = openid.decode()
        if isinstance(unique_id, bytes):
            unique_id = unique_id.decode()
        self.redis.set(f'scaned_{unique_id}', openid, ex=exp)

    def get_scened_flag(self, unique_id):
        if isinstance(unique_id, bytes):
            unique_id = unique_id.decode()
        return self.redis.get(f'scaned_{unique_id}')

    def set_ticket_unique(self, ticket, unique_id, exp=1800):
        if isinstance(ticket, bytes):
            ticket = ticket.decode()
        if isinstance(unique_id, bytes):
            unique_id = unique_id.decode()
        self.redis.set(f'ticket_{ticket}', unique_id, ex=exp)

    def get_ticket_unique(self, ticket):
        if isinstance(ticket, bytes):
            ticket = ticket.decode()
        return self.redis.get(f'ticket_{ticket}')

    def get_access_token(self):
        return self.redis.get("wp_access_token")

    def set_access_token(self, access_token, exp):
        self.redis.set("wp_access_token", access_token, ex=exp)

    def acquire_lock_once(self, lockname):
        identifier = str(uuid.uuid4())
        if self.redis.setnx('lock:' + lockname, identifier):
            return identifier
        return False

    def get_ttl(self, key_name):
        return self.redis.ttl(key_name)

    def get_access_token_ttl(self):
        return self.get_ttl('wp_access_token')

    def lock_access_token_with_timeout(self, acquire_timeout=10, lock_timeout=10):
        return self.acquire_lock_with_timeout('wp_access_token', acquire_timeout=acquire_timeout,
                                              lock_timeout=lock_timeout)

    def release_access_token_lock(self, identifier):
        return self.release_lock("wp_access_token", identifier)

    def acquire_lock_with_timeout(self, lockname, acquire_timeout=10, lock_timeout=10):
        identifier = str(uuid.uuid4())
        lockname = 'lock:' + lockname
        lock_timeout = int(math.ceil(lock_timeout))

        end = time.time() + acquire_timeout
        while time.time() < end:
            if self.redis.setnx(lockname, identifier):
                self.redis.expire(lockname, lock_timeout)
                return identifier
            elif not self.redis.ttl(lockname):
                self.redis.expire(lockname, lock_timeout)

            time.sleep(.001)
        return False

    def release_lock(self, lockname, identifier):
        pipe = self.redis.pipeline(True)
        lockname = 'lock:' + lockname

        while True:
            try:
                pipe.watch(lockname)
                if pipe.get(lockname) == identifier:
                    pipe.multi()
                    pipe.delete(lockname)
                    pipe.execute()
                    return True
                pipe.unwatch()
                break
            except redis.exceptions.WatchError:
                pass
        return False


redis_client = RedisUtil()
