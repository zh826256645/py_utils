# -*- coding: utf-8 -*-
"""
Instruction
"""
import sys
import logging

from exts.config_base import ConfigBase


class LogConfig(ConfigBase):
    KEYS = ["file_name", "base_path", "path", "debug", "fmt", "date_fmt"]

    def __init__(
        self,
        file_name: str = None,
        base_path: str = None,
        path: str = None,
        debug: bool = False,
        fmt: str = "%(asctime)s - %(levelname)s: %(message)s",
        date_fmt: str = "%Y-%m-%d %H:%M:%S %p",
    ) -> None:
        """init log

        :param str file_name: log filename
        :param str base_path: file base path
        :param str path: base_path/filename
        :param bool debug: True or False

        :param str fmt: log formatting
        :param str date_fmt: date formatting
        """
        self.file_name = file_name
        self.base_path = base_path
        self.path = path
        self.debug = debug
        self.fmt = fmt
        self.date_fmt = date_fmt

    def build_path(self):
        file_name = self.file_name or __name__
        if file_name[-4:] != ".log":
            file_name = f"{file_name}.log"

        if self.base_path:
            self.path = f"{self.base_path}/{file_name}"
        else:
            self.path = file_name

    def init_ext(self) -> logging.Logger:
        self.build_path()

        log = logging.getLogger("log_ext")
        formatter = logging.Formatter(self.fmt, self.date_fmt)
        if self.debug:
            log.setLevel(logging.DEBUG)

            steam_handler = logging.StreamHandler(sys.stderr)
            steam_handler.setFormatter(formatter)
            log.addHandler(steam_handler)
        else:
            log.setLevel(logging.INFO)
            file_handler = logging.FileHandler(self.path)
            file_handler.setFormatter(formatter)
            log.addHandler(file_handler)

        return log


def main():
    log = LogConfig(debug=True).init_ext()
    log.info("Hello World!")


if __name__ == "__main__":
    main()
