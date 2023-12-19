# -*- coding: utf-8 -*-
"""
Task 服务
"""
import time
import uuid
from abc import abstractmethod

from typing import Any

from py_utils.script.service import Service
from py_utils.script.task import Task


class TaskService(Service):
    def __init__(self):
        super().__init__()

        self.enable_same_task = False
        self.task_time_out = 600

    def is_same_task_running(self, task: Task) -> bool:
        return False

    @abstractmethod
    def pull_queue(self) -> Any:
        """获取 Task 的值"""
        pass

    @abstractmethod
    def push_queue(self):
        pass

    def get_tid(self) -> str:
        """获取任务 ID

        默认使用 UUID
        """
        return str(uuid.uuid1())

    def get_task(self) -> Task:
        """获取任务

        初始化：任务 ID、code、value、任务开始时间
        """
        return Task(
            tid=self.get_tid(),
            code=0,
            value=self.pull_queue(),
            start_time=int(time.time()),
        )

    def main(self):
        task = self.get_task()
        if not task:
            time.sleep(0.5)
            return

        if not self.enable_same_task and self.is_same_task_running(task):
            time.sleep(0.5)
            return

        self.before_work(task)

        status = self.work(task)
        task.status = status
        if task.status is False:
            self.retry_task(task)

        self.after_work(task)

        self.finish_task(task)

    @abstractmethod
    def work(self, task: Task) -> bool:
        pass

    def before_work(self, task: Task):
        pass

    def after_work(self, task: Task):
        pass

    def retry_task(self, task: Task):
        pass

    def finish_task(self, task: Task):
        pass


def main():
    TaskService.run_forever()


if __name__ == "__main__":
    main()
