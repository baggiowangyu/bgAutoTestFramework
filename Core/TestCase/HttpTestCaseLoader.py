#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import os
import platform
import time

import jsonpatch
import xlrd

import Core.Interface.HttpInterface


class HttpTestCaseLoader:

    def __init__(self, http_server_ip, http_server_port, http_protocol):
        # 初始化成员变量
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.http_server_ip = http_server_ip
        self.http_server_port = http_server_port
        self.http_protocol = http_protocol

    def LoadTestCase(self, path):
        # 加载测试用例
        # 返回一个list()，里面是我们加载的所有测试用例数据
        try:
            test_case_file = xlrd.open_workbook(path)
            # 获取测试用例第一页
            test_case_file_sheet = test_case_file.sheets()[0]

            test_case_infos = list()
            row_counts = test_case_file_sheet.nrows
            for row_index in range(1, row_counts):
                # 逐个取单元格数据
                test_case_info = dict()
                test_case_info["case_id"] = str(test_case_file_sheet.cell(row_index, 0).value)
                test_case_info["case_name"] = test_case_file_sheet.cell(row_index, 1).value
                test_case_info["interface_uri"] = test_case_file_sheet.cell(row_index, 2).value
                test_case_info["call_method"] = test_case_file_sheet.cell(row_index, 3).value
                test_case_info["repeat_count"] = int(test_case_file_sheet.cell(row_index, 4).value)
                test_case_info["query_param"] = test_case_file_sheet.cell(row_index, 5).value
                test_case_info["body_param"] = test_case_file_sheet.cell(row_index, 6).value
                test_case_info["expected_result_type"] = test_case_file_sheet.cell(row_index, 7).value
                test_case_info["expected_result"] = test_case_file_sheet.cell(row_index, 8).value

                test_case_infos.append(test_case_info)

            return test_case_infos
        except Exception as e:
            print(u"加载测试用例失败！\n%s" % e)
        return

    def RunTestCase(self, module_name, case_list):
        # 执行测试用例，并记录每次测试的结果
        # 测试用结果格式：
        # {
        #     # 被测试的模块名称
        #     "module_name": "",
        #
        #     # 测试开始时间
        #     "start_time": 123,
        #     # 测试结束时间
        #     "end_time": 456,
        #     # 测试耗时
        #     "escape_time": 111,
        #
        #     "pass_case_count": 0,
        #     "failed_case_count": 0,
        #     "exception_case_count": 0,
        #     "unknow_case_count": 0,
        #
        #     "case_results": [
        #         {
        #             "case_id": "",
        #             "run_count": 10,
        #             "succeed_count": 9,
        #             "failed_count": 1,
        #             "failed_details": [
        #                 {
        #                     "test_index": 1,
        #                     "failed_info": ""
        #                 }
        #             ]
        #         }
        #     ]
        # }


        # 定义用例结果列表
        test_suite_result = dict()
        test_suite_result["module_name"] = module_name

        # 记录测试机器相关信息，包含（机器名称、IP地址、）
        test_suite_result["computer"] = platform.platform()
        test_suite_result["computer_architecture"] = platform.machine()
        test_suite_result["computer_processor"] = platform.processor()
        test_suite_result["computer_name"] = os.environ["COMPUTERNAME"]

        # 记录开始时间
        start_time = int(time.time())
        test_suite_result["start_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
        test_suite_result["case_results"] = list()

        failed_case_count = 0
        pass_case_count = 0

        interface = Core.Interface.HttpInterface.HttpInterface(self.http_server_ip, self.http_server_port, self.http_protocol)

        # 执行测试用例
        for case in case_list:

            # 定义用例结果
            case_result = dict()
            case_result["case_info"] = case
            case_result["run_count"] = case["repeat_count"]
            case_result["failed_details"] = list()

            # 获取期望结果
            expected_result = json.loads(case["expected_result"])
            case_result["interface_return"] = ""
            interface_return = ""

            # 获取重复次数
            succeed_count = 0
            failed_count = 0
            repeat_count = case["repeat_count"]
            for index in range(0, repeat_count):
                # 提取参数，调用接口
                interface_result = interface.SendRequest(case)

                # 在这里比对返回的Json结果是否相同
                real_result = json.loads(interface_result["http_response_data"])
                patch = jsonpatch.JsonPatch.from_diff(expected_result, real_result)
                if len(patch.patch) == 0:
                    # 这里记录调用成功的信息
                    succeed_count = succeed_count + 1
                else:
                    # 这里记录调用失败的信息
                    failed_count = failed_count + 1

                    failed_detail = dict()
                    failed_detail["test_index"] = index
                    if interface_result["http_state"] == 200:
                        failed_detail["failed_info"] = u"非期望返回值：%s" % interface_result["http_response_data"]
                    else:
                        failed_detail["failed_info"] = u"接口通信错误：%d" % interface_result["http_state"]

                    case_result["failed_details"].append(failed_detail)

                interface_return = str(index + 1) + ". " + interface_result["http_response_data"] + "<br/>"
                case_result["interface_return"] = case_result["interface_return"] + interface_return

            # 记录用例的成功/失败次数
            case_result["succeed_count"] = succeed_count
            case_result["failed_count"] = failed_count

            # 判断此用例是否通过（规则，只要有一次调用失败，则不通过）
            if case_result["failed_count"] > 0:
                failed_case_count = failed_case_count + 1
                case_result["result"] = "F"
            else:
                pass_case_count = pass_case_count + 1
                case_result["result"] = "P"

            # 插入本条用例的结果详情
            test_suite_result["case_results"].append(case_result)

        # 补充结束时间与耗时
        end_time = int(time.time())
        test_suite_result["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))
        test_suite_result["escape_time"] = end_time - start_time

        test_suite_result["failed_case_count"] = failed_case_count
        test_suite_result["pass_case_count"] = pass_case_count

        return test_suite_result


if __name__ == '__main__':
    loader = HttpTestCaseLoader()
