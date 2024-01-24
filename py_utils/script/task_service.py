# -*- coding: utf-8 -*-
"""
Task 服务

用 Redis 做队列
"""
import json
import time
import uuid
from abc import abstractmethod
from typing import Any

from redis import Redis

from py_utils.script.service import Service
from py_utils.script.task import Task


class TaskService(Service):
    def __init__(self):
        super().__init__()

        self.enable_same_task = False
        self.task_time_out = 600

        self.retry_times = 3

    @property
    def task_redis(self) -> Redis:
        if self.redis:
            return self.redis

        raise Exception("缺少 Task Redis")

    def get_task_lock_key(self, task: Task) -> str:
        return f"task_service.{self.task_key}.{task.value}.lock"

    @abstractmethod
    def task_key(self) -> str:
        """任务 key"""
        pass

    @abstractmethod
    def pull_queue(self) -> Any:
        """从任务队列获取数据"""
        return self.task_redis.rpop(self.task_key)

    @abstractmethod
    def push_queue(self, task: Task):
        """推送数据到队列中"""
        self.task_redis.lpush(self.task_key, json.dumps(task.get_data()))

    def get_tid(self) -> str:
        """获取任务 ID

        默认使用 UUID
        """
        return str(uuid.uuid1())

    def get_task(self) -> Task:
        """获取任务

        初始化：任务 ID、code、value、任务开始时间
        """
        value = self.pull_queue()
        data = {}
        if value:
            data = json.loads(value)

        task = Task(**data)
        task.code = 0
        task.start_time = int(time.time())
        task.end_time = None

        return task

    def main(self):
        self.before_task()

        task = self.get_task()
        if not task:
            time.sleep(0.5)
            return

        status = self.lock_task(task)
        if not status:
            time.sleep(0.5)
            return

        status = self.work(task)
        task.status = status
        if task.status is False:
            self.retry_task(task)

        self.finish_task(task)

    @abstractmethod
    def work(self, task: Task) -> bool:
        pass

    def before_task(self) -> bool:
        return True

    def lock_task(self, task: Task) -> bool:
        """work 执行前的 hook"""
        if not self.enable_same_task:
            lock_key = self.get_task_lock_key(task)
            if self.task_redis.get(lock_key):
                return False

            if not self.task_redis.set(lock_key, "T", ex=self.task_time_out, nx=True):
                return False

        return True

    def retry_task(self, task: Task):
        pass

    def finish_task(self, task: Task):
        if not self.enable_same_task:
            self.task_redis.delete(self.get_task_lock_key(task))


def main():
    TaskService.run_forever()


if __name__ == "__main__":
    main()
