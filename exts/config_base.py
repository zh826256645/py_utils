# -*- coding: utf-8 -*-
"""
Config 基类
"""
from typing import List
from typing_extensions import Self


class ConfigBase:
    KEYS: List[str] = []

    def load_config(self, config: dict) -> Self:
        """导入配置

        :param dict config: 配置数据
        :return Self: self
        """
        for key in self.KEYS:
            if config.get(key):
                setattr(self, key, config[key])
        return self

    def init_ext(self):
        pass
