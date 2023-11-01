# -*- coding: utf-8 -*-
"""
init MongoDB
"""

from pymongo.mongo_client import MongoClient

from exts.config_base import ConfigBase


class MongoConfig(ConfigBase):
    KEYS = ["host", "port", "username", "password", "uri"]

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = "27017",
        username: str = None,
        password: str = None,
        uri: str = None,
    ) -> None:
        """init setting

        :param str host: mongodb host
        :param int port: service port
        :param str username: authenticate username
        :param str password: authenticate password
        :param str uri: mongodb uri
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.uri = uri

    def build_uri(self):
        if not self.uri:
            if self.password and self.username:
                self.uri = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}?authSource=admin"
            else:
                self.uri = f"mongodb://{self.host}:{self.port}"

    def init_ext(self) -> MongoClient:
        self.build_uri()

        client = MongoClient(self.uri)
        return client


def main():
    client = MongoConfig().init_ext()
    names = client.list_database_names()
    print(names)


if __name__ == "__main__":
    main()
