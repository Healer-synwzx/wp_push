import time
from werobot.client import Client
from werobot.robot import WeRoBot
from werobot.utils import cached_property

from redis_util import redis_client
from config import logger


class RewriteAccessTokenClient(Client):

    def get_access_token(self):
        token_ttl = redis_client.get_access_token_ttl()
        if token_ttl < 60:
            identifier = redis_client.acquire_lock_with_timeout("wp_access_token", acquire_timeout=10, lock_timeout=10)
            try:
                if identifier:
                    if redis_client.get_access_token_ttl() < 60:
                        json = self.grant_token()
                        access_token = json["access_token"]
                        expire = json["expires_in"]
                        redis_client.set_access_token(access_token, expire)
            finally:
                redis_client.release_access_token_lock(identifier)

        return redis_client.get_access_token()


class Robot(WeRoBot):

    @cached_property
    def client(self):
        logger.info("use RewriteAccessTokenClient")
        return RewriteAccessTokenClient(self.config)

