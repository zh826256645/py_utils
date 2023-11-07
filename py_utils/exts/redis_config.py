# -*- coding: utf-8 -*-
"""
Redis 组件初始化
"""
from typing import Optional

import redis

from py_utils.exts.config_base import ConfigBase


class RedisConfig(ConfigBase):
    KEYS = ["host", "port", "db", "protocol", "username", "password", "url"]

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 6379,
        db: int = 0,
        protocol: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        url: Optional[str] = None,
    ) -> None:
        """init

        :param str host: redis host
        :param int port: port
        :param int db: db num
        :param int protocol: use redis 5.0 version need set "protocol = 3"
        :param username: authenticate username
        :param password: authenticate password
        :param url: redis url
        """
        self.host = host
        self.port = port
        self.db = db
        self.protocol = protocol
        self.username = username
        self.password = password
        self.url = url

    def build_url(self):
        if self.password:
            if not self.username:
                self.username = ""
            self.url = f"redis://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}"
        else:
            self.url = f"redis://{self.host}:{self.port}/{self.db}"

    def init_ext(self) -> redis.Redis:
        self.build_url()

        return redis.Redis.from_url(url=self.url)


def main():
    client = RedisConfig().init_ext()
    print(client.info())


if __name__ == "__main__":
    main()
