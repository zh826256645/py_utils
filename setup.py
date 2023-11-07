# -*- coding: utf-8 -*-
from setuptools import setup

VERSION = "0.1.1"
DESCRIPTION = "My python utils"
LONG_DESCRIPTION = "My python utils"

# 配置
setup(
    # 名称必须匹配文件名 'verysimplemodule'
    name="py_utils",
    version=VERSION,
    author="xiguashu",
    author_email="zh826256645@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    install_requires=[],  # add any additional packages that
    # 需要和你的包一起安装，例如：'caer'
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
