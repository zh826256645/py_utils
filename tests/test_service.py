# -*- coding: utf-8 -*-
"""
测试 service 脚本
"""
from py_utils.script.service import Service


class TestService(Service):
    _DEFAULT_CONFIG_PATH = "tests/config.ini"

    def main(self):
        print(self.mongo)
        print("Hello World~")

        self.redis.rpush("test1", "11")
        print(self.redis.lrange("test1", 0, -1))

        self.redis.lrem("test1", 1, "11")
        print(self.redis.lrange("test1", 0, -1))

        print(list(self.mongo["test"].list_collections()))


def main():
    TestService.run()


if __name__ == "__main__":
    main()
