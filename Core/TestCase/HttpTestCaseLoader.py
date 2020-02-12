#!/usr/bin/python
# -*- coding: UTF-8 -*-


import os
import xlrd


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
            test_case_info = dict()

            row_counts = test_case_file_sheet.nrows
            for row_index in range(1, row_counts):
                test_case_info["case_id"] = test_case_file_sheet.cell(row_index, 0).value
                test_case_info["case_name"] = test_case_file_sheet.cell(row_index, 1).value
                test_case_info["interface_uri"] = test_case_file_sheet.cell(row_index, 2).value
                test_case_info["call_method"] = test_case_file_sheet.cell(row_index, 3).value
                test_case_info["repeat_count"] = test_case_file_sheet.cell(row_index, 4).value
                test_case_info["query_param"] = test_case_file_sheet.cell(row_index, 5).value
                test_case_info["body_param"] = test_case_file_sheet.cell(row_index, 6).value
                test_case_info["return"] = test_case_file_sheet.cell(row_index, 7).value

                test_case_infos.append(test_case_info)

            return test_case_infos
        except Exception as e:
            print(u"加载测试用例失败！\n%s" % e)
        return

if __name__ == '__main__':
    loader = HttpTestCaseLoader()
