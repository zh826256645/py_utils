# -*- coding: utf-8 -*-
"""
测试 ExtLoader
"""

from exts.ext_loader import ExtLoader


def main():
    loader = ExtLoader(config_path="/Users/zhonghao/Projects/py_utils/test/config.ini")
    loader.load_exts()
    loader.exts.log.info("Hello World!")


if __name__ == "__main__":
    main()
