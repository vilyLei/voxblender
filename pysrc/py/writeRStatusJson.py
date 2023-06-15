#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json

statusData = {
"rendering-ins":"jetty-scene-renderer",
"rendering-task":
    {
        "uuid":"rtrt88970-8990",
        "taskID":1,
        "name":"high-image-rendering",
        "phase":"finish",
        "progress":20,
        "times":2
    },
"rendering-status":"task:running"
}
rtask = statusData["rendering-task"]
rtask["progress"] = 29
rtask["times"] = 3
# 将数据写入 JSON 格式的文件
with open('./assets/rstatus.json', 'w') as f:
    json.dump(statusData, f)