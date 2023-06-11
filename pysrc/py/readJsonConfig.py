#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json

import sysinfo

version = sysinfo.getVersion()
print("version: ", version)

file = open('./assets/config.json','rb')
jsonDataStr = file.read()
print("jsonDataStr: \n", jsonDataStr)
jsonObj = json.loads(jsonDataStr)
print("jsonObj: \n", jsonObj)
print("\n>>>")
print('jsonObj["renderer-proc"]: \n', jsonObj["renderer-proc"])
print("\n>>>")
print('jsonObj["resource"]: \n', jsonObj["resource"])