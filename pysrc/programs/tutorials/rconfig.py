#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json

def getVersion():
    return 101

def getJsonObjFromFile(path):
    file = open(path,'rb')
    jsonDataStr = file.read()
    print("jsonDataStr: \n", jsonDataStr)
    jsonObj = json.loads(jsonDataStr)
    return jsonObj