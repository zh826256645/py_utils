# -*- coding: utf-8 -*-
"""
测试 ExtLoader
"""

from py_utils.exts.ext_loader import ExtLoader


def main():
    loader = ExtLoader(config_path="tests/config.ini")
    loader.load_exts()
    loader.exts.log.info("Hello World!")

    print(loader.exts.mongo.list_database_names())


if __name__ == "__main__":
    main()
