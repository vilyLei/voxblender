#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json

# 定义要写入的数据
data = {
    "name": "Vily",
    "age": 30,
    "city": "BeiJing"
}

# 将数据写入 JSON 格式的文件
with open('./assets/test.json', 'w') as f:
    json.dump(data, f)