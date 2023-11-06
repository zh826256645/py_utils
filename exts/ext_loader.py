# -*- coding: utf-8 -*-
"""
从配置文件注册组件
"""
from typing import Optional
from configparser import ConfigParser

from exts.config_base import ConfigBase
from exts.mongo_config import MongoConfig
from exts.redis_config import RedisConfig
from exts.log_config import LogConfig


class Exts(dict):
    """组件中心"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class ExtLoader:
    def __init__(
        self, config_path: str = "config.cfg", name_ext_config: Optional[dict] = None
    ) -> None:
        self.config_path = config_path
        self.exts = Exts()

        self.config: Optional[ConfigParser] = None
        self.load_config()

        self._name_ext_config = {
            "mongo": MongoConfig,
            "redis": RedisConfig,
            "log": LogConfig,
        }
        if name_ext_config:
            self._name_ext_config.update(name_ext_config)

    def get_ext_config(self, name: str) -> Optional[type[ConfigBase]]:
        """获取组件配置类

        :param str name: 配置名
        :return ConfigBase: 配置类
        """
        for key, ext_config in self._name_ext_config.items():
            if name.startswith(key):
                return ext_config
        return None

    def load_config(self):
        """导入配置"""
        self.config = ConfigParser()
        self.config.read(self.config_path)

    def load_exts(self):
        for key in self.config.keys():
            ext_config = self.get_ext_config(key)
            if not ext_config:
                continue

            self.exts[key] = ext_config().load_config(self.config[key]).init_ext()
