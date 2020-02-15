#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time

import toml

import Core.TestCase.HttpTestCaseLoader
import Core.Report.ReportGenerator
import Core.Publish.FtpClient
import Core.Publish.DingTalk

if __name__ == '__main__':
    print(u"加载配置信息")
    current_path = os.path.abspath(os.path.dirname(__file__))

    config_data = toml.load(os.getcwd() + "\\config.toml")

    # HTTP接口测试相关内容
    http_server_ip = config_data["http_service"]["ip"]
    http_server_port = config_data["http_service"]["port"]
    http_protocol = config_data["http_service"]["protocol"]

    # FTP配置
    ftp_host = config_data["ftp"]["host"]
    ftp_user = config_data["ftp"]["username"]
    ftp_pass = config_data["ftp"]["password"]
    ftp_path = config_data["ftp"]["path"]
    http_result_root = config_data["ftp"]["http_root_url"]

    # 钉钉推送地址
    dingtalk_url = config_data["ding_talk"]["post_url"]

    module_name = config_data["module"]["name"]

    # 加载测试用例
    loader = Core.TestCase.HttpTestCaseLoader.HttpTestCaseLoader(http_server_ip, http_server_port, http_protocol)
    case_list = loader.LoadTestCase(current_path + config_data["case"]["http_case_path"])

    # 执行测试用例
    print(u"执行测试用例")
    case_result = loader.RunTestCase(module_name, case_list)
    # print(case_result)

    # 生成测试结果
    report_generator = Core.Report.ReportGenerator.ReportGenerator()
    html_report = report_generator.GenerateHTMLReport(case_result)
    # print(html_report)

    # 创建文件名
    start_time = int(time.time())
    t = time.strftime("%Y%m%d_%H%M%S", time.localtime(start_time))
    html_file_name = "%s_%s_%s.html" % (case_result["module_name"], case_result["computer_name"], t)
    try:
        f = open(html_file_name, "w")
        f.write(html_report)
        f.close()
    except Exception as e:
        print(e)
        exit(4)

    # 如果配置了FTP推送文件，则推送
    ftp_client = Core.Publish.FtpClient.FtpClient(ftp_host, ftp_user, ftp_pass)
    if ftp_client.Connect():
        remote_path = ftp_path + html_file_name
        if ftp_client.PushFile(html_file_name, remote_path):
            print(u"推送结果成功")
        else:
            print(u"推送结果失败")

    # 删除结果
    # 还是不删除吧，本地留个底
    # os.remove(html_file_name)

    # 将测试结果推送到测试结果Web服务器（实际上是推送到一个FTP路径下，同时也是Web路径）
    http_url = http_result_root + html_file_name
    dingtalk_report = report_generator.GenerateDingTalkReport(case_result, http_url)
    print(dingtalk_report)

    # 推送钉钉消息
    if Core.Publish.DingTalk.PushDingTalk(dingtalk_url, dingtalk_report):
        print(u"钉钉消息推送成功")
    else:
        print(u"钉钉消息推送失败")