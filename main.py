#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import toml

import Core.TestCase.HttpTestCaseLoader

if __name__ == '__main__':
    print(u"加载配置信息")
    current_path = os.path.abspath(os.path.dirname(__file__))

    config_data = toml.load(os.getcwd() + "\\config.toml")

    # HTTP接口测试相关内容
    http_server_ip = config_data["http_service"]["ip"]
    http_server_port = config_data["http_service"]["port"]
    http_protocol = config_data["http_service"]["protocol"]

    # 加载测试用例
    loader = Core.TestCase.HttpTestCaseLoader.HttpTestCaseLoader(http_server_ip, http_server_port, http_protocol)
    case_list = loader.LoadTestCase(current_path + config_data["http_case"]["path"])

    # 执行测试用例
    print(u"执行测试用例")

    # 生成测试结果
    # 推送钉钉消息