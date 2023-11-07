# -*- coding: utf-8 -*-
"""
测试 service 脚本
"""
from py_utils.script.service import Service


class TestService(Service):
    def main(self):
        print(self.mongo)
        print("Hello World~")


def main():
    TestService.run(config_path="tests/config.ini")


if __name__ == "__main__":
    main()
