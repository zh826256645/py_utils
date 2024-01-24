# -*- coding: utf-8 -*-
"""
Task 类
"""
from typing import Optional, Any


class Task:
    def __init__(
        self,
        tid: Optional[str] = None,
        value: Any = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        code: int = 0,
        result: Any = None,
        msg: Optional[str] = None,
        retry: int = 0,
        other: Any = None,
    ) -> None:
        self.tid = tid
        self.value = value
        self.start_time = start_time
        self.end_time = end_time
        self.code = code
        self.result = result
        self.msg = msg
        self.retry = retry
        self.other = other
        self.status = True

    def __bool__(self):
        return bool(self.value)

    def get_data(self) -> dict:
        return {key: value for key, value in self.__dict__.items() if value}
