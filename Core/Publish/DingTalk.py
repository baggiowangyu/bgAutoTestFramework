#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import requests


def PushDingTalk(url, content):

    pagrem = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "isAtAll": True
    }

    headers = {
        'Content-Type': 'application/json'
	}

    f = requests.post(url, data=json.dumps(pagrem), headers=headers)
    if f.status_code == 200:
        return True
    else:
        return False