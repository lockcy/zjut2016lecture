#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @auther : lockcy
import nonebot
from os import path
import config
if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'awesome', 'plugins'),
        'awesome.plugins'
    )
    nonebot.run()