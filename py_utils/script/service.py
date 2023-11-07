# -*- coding: utf-8 -*-
"""
服务脚本
"""
from typing import Optional
from abc import ABCMeta, abstractmethod

from pymongo import MongoClient
from redis import Redis
from logging import Logger

from py_utils.exts.ext_loader import ExtLoader
from py_utils.exts.log_config import LogConfig


class Service(metaclass=ABCMeta):
    def __init__(self, config_path: str = "config.cfg"):
        self.ext_loader = ExtLoader(config_path=config_path)
        self.ext_loader.load_exts()

        self.mongo: Optional[MongoClient] = self.ext_loader.exts.get("mongo")
        self.redis: Optional[Redis] = self.ext_loader.exts.get("redis")
        self.log: Logger = (
            self.ext_loader.exts.get("log") or LogConfig(debug=True).init_ext()
        )

    @classmethod
    def run_forever(cls, config_path: str = "config.cfg"):
        _service = cls(config_path)
        _service.log.info("program start:")
        while True:
            _service.main()

    @classmethod
    def run(cls, config_path: str = "config.cfg"):
        _service = cls(config_path)
        _service.log.info("program start:")
        _service.main()

    @abstractmethod
    def main(self):
        pass


def main():
    Service.run_forever()


if __name__ == "__main__":
    main()
