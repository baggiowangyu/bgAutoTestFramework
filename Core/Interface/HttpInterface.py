#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests


class HttpInterface:

    def __init__(self, ip, port, protocol):
        self.server_ip = ip
        self.server_port = port
        self.server_protocol = protocol
        self.url_prefix = "%s://%s:%d" % (self.server_protocol, self.server_ip, self.server_port)
        self.cookies = ""

    def SendRequest(self, case):
        # 发送用例中的请求，接收返回结果
        # 返回结果，是测试用例的执行结果，其中包括

        response = ""

        if case["call_method"] == "POST":
            # 准备一下POST需要的数据
            post_header = dict()
            post_header["Content-Type"] = "application/json"
            post_header["Accept"] = "application/json"

            url_tmp = self.url_prefix + case["interface_uri"]

            # 判断是否需要附加Query数据
            if len(case["query_param"]) > 0:
                url = url_tmp + "?" + case["query_param"]
            else:
                url = url_tmp

            response = requests.post(url=url, data=case["body_param"], headers=post_header)
        elif case["call_method"] == "GET":
            url_tmp = self.url_prefix + case["interface_uri"]

            # 判断是否需要附加Query数据
            if len(case["query_param"]) > 0:
                url = url_tmp + "?" + case["query_param"]
            else:
                url = url_tmp

            response = requests.get(url=url)

        self.cookies = response.cookies

        # http通信结果
        interface_result = dict()
        interface_result["http_state"] = response.status_code

        # 判断通信结果，若结果为200 OK，则保存Cookie
        if response.status_code == 200:
            # http返回值，可以是任何数据，Json、XML、
            interface_result["http_response_data_type"] = response.headers["Content-Type"]
            interface_result["http_response_data"] = str(response.content, "utf-8")

        return interface_result

