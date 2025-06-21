# -*- coding: utf-8 -*-
"""
天眼 client
"""
import json
from dataclasses import asdict, dataclass

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass
class EyeSetting:
    token: str
    env_: str
    eye_domain: str


@dataclass
class SaParam:
    k: str
    v: str
    tp: str

    def dict(self):
        return {k: v for k, v in asdict(self).items()}


class EyeClient:

    def __init__(self, token: str, env_: str = "prod", eye_domain: str | None = None):
        self.eye_setting = EyeSetting(
            token=token, env_=env_, eye_domain=eye_domain or "https://eye.oa.com"
        )
        self.mongo = EyeMongoClient(self.eye_setting)
        self.sa = EyeSaClient(self.eye_setting)


class EyeMongoClient:

    def __init__(self, eye_setting: EyeSetting):
        self.eye_setting = eye_setting

    def get_headers(self) -> dict:
        return {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "dnt": "1",
            "ignorecanceltoken": "false",
            "origin": "https://eye.oa.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://eye.oa.com/project/home/database?pid=64cf1058a0d0bdb0ea376b55&pj=at&env=prod&root=mongodb_status&action=mongo_dms&level=notice",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "token": self.eye_setting.token,
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "cookie": "session=6eeaa965-1991-11f0-b2fb-525400e7f65b",
        }

    def find(
        self,
        coll_name: str,
        mongo_url: str,
        query: dict | None = None,
        sort: dict | None = None,
        project: dict | None = None,
        page: int = 1,
        default_limit: int = 200,
        limit: int | None = None,
    ):
        post_data = {
            "env": self.eye_setting.env_,
            "pid": "64cf1058a0d0bdb0ea376b55",
            "url": mongo_url,
            "col": coll_name,
            "stype": "find",
            "default_limit": str(default_limit),
            "page": str(page),
            "op_id": "2a7a063a298c61f8e54ef7f8c9d6b132",
        }
        if limit:
            post_data["limit"] = str(limit)

        for key, value in [("query", query), ("sort", sort), ("projection", project)]:
            if value:
                post_data[key] = json.dumps(value, ensure_ascii=False)

        return self.to_request(data=post_data)

    def aggregate(
        self,
        coll_name: str,
        mongo_url: str,
        aggregate_query: list | None = None,
        page: int = 1,
        default_limit: int = 200,
    ):
        if not aggregate_query:
            aggregate_query = []

        post_data = {
            "env": self.eye_setting.env_,
            "pid": "64cf1058a0d0bdb0ea376b55",
            "url": mongo_url,
            "col": coll_name,
            "stype": "aggregate",
            "default_limit": str(default_limit),
            "query": json.dumps(aggregate_query, ensure_ascii=False),
            "skip_max_time": "false",
            "page": str(page),
            "op_id": "87264568a0e7e7e4d9075a68d08ba81b",
        }

        return self.to_request(data=post_data)

    def insert_one(self, coll_name: str, mongo_url: str, data: dict):
        if not data:
            raise Exception("不能插入空数据")

        post_data = {
            "env": self.eye_setting.env_,
            "pid": "64cf1058a0d0bdb0ea376b55",
            "url": mongo_url,
            "col": coll_name,
            "stype": "insert",
            "default_limit": "50",
            "query": json.dumps(data, ensure_ascii=False),
            "page": "1",
            "op_id": "87264568a0e7e7e4d9075a68d08ba81b",
        }

        return self.to_request(data=post_data)

    def update_one(
        self,
        coll_name: str,
        mongo_url: str,
        query: dict,
        data: dict,
        upsert: bool = False,
    ):
        post_data = {
            "env": self.eye_setting.env_,
            "pid": "64cf1058a0d0bdb0ea376b55",
            "url": mongo_url,
            "col": coll_name,
            "stype": "update",
            "page": "1",
            "limit": "50",
            "query": json.dumps(query, ensure_ascii=False),
            "update": json.dumps(data, ensure_ascii=False),
            "justone": "1",
        }
        if upsert:
            post_data["upsert"] = "1"

        return self.to_request(data=post_data)

    def update_many(
        self,
        coll_name: str,
        mongo_url: str,
        query: dict,
        data: dict,
    ):
        post_data = {
            "env": self.eye_setting.env_,
            "pid": "64cf1058a0d0bdb0ea376b55",
            "url": mongo_url,
            "col": coll_name,
            "stype": "update",
            "page": "1",
            "limit": "50",
            "query": json.dumps(query, ensure_ascii=False),
            "update": json.dumps(data, ensure_ascii=False),
        }

        return self.to_request(data=post_data)

    def to_request(self, data: dict) -> dict | list:
        return requests.post(
            f"{self.eye_setting.eye_domain}/api/mongo_dms/exec_shell/",
            headers=self.get_headers(),
            data=data,
            verify=False,
        ).json()["data"]["datas"]


class EyeSaClient:
    def __init__(self, eye_setting: EyeSetting):
        self.eye_setting = eye_setting

    def get_headers(self) -> dict:
        return {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "dnt": "1",
            "ignorecanceltoken": "false",
            "origin": "https://eye.oa.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://eye.oa.com/project/home/database?pid=64cf1058a0d0bdb0ea376b55&pj=at&env=prod&root=mongodb_status&action=mongo_dms&level=notice",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "token": self.eye_setting.token,
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "cookie": "session=6eeaa965-1991-11f0-b2fb-525400e7f65b",
        }

    def tc(
        self,
        params: list[SaParam],
        task_key: str,
        pool: str,
        cache: int = 300,
        timeout: int = 60,
        put: int = 1,
    ) -> dict:
        data = {
            "tid": "6810a5a3c692cc248a83a1a0",
            "env": self.eye_setting.env_,
            "pid": "64cf1061a0d0bdb0ea376b68",
            "pool": pool,
            "task_key": task_key,
            "method": "tc",
            "cache": str(cache),
            "timeout": str(timeout),
            "get_track": "false",
            "put": str(put),
            "params": json.dumps(
                [param.dict() for param in params], ensure_ascii=False
            ),
        }
        response = requests.post(
            "https://eye.oa.com/api/spider_inter/debug/",
            headers=self.get_headers(),
            data=data,
            verify=False,
        )
        print(response.json())
        return response.json()["data"]["data"]


def main():
    eye_client = EyeClient(
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNWZkMzM3ZTZlNzExYmY5ZTdiNzZkM2U3IiwiZXhwIjo1ODY5NjZ9.4bjYi2zYUPSpA4eZdnD9eFmcfd2QFZF4J0dfqFfFHJw"
    )
    result = eye_client.sa.tc(
        [
            SaParam(
                "keyword",
                "onlyshop-1/reed-diffuser-white-jasmine-zara-home-pengharum-ruangan-fragrance-100-ml",
                "string",
            )
        ],
        "tokopedia.item.detail",
        "AS",
    )
    print(result)


if __name__ == "__main__":
    main()
