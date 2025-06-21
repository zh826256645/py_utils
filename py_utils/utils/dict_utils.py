# -*- coding: utf-8 -*-
"""
字典工具
"""
import re


def unpack_dict(result, pattern, default=None):
    try:
        temp = result
        params = pattern.split(".")
        for param in params:
            index = None
            match = re.search(r"(.+)\[(-?\d+)\]", param)
            if match:
                param, index = match.groups()

            temp = temp[param]
            if index is not None:
                temp = temp[int(index)]

        return temp
    except Exception:
        return default


def main():
    data = {"items": [{"title": "123"}]}
    print(unpack_dict(data, "items[-1]"))


if __name__ == "__main__":
    main()
