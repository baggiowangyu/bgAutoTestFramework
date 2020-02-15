#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 测试报告生成器

class ReportGenerator:

    def GenerateDingTalkReport(self, case_result, report_detail):
        # 组织测试结论概要，如果结果推送到服务器了，将服务器地址一并发上
        module_name = case_result["module_name"]
        case_count = len(case_result["case_results"])
        pass_case_count = case_result["pass_case_count"]
        failed_case_count = case_result["failed_case_count"]
        pass_percent = float(pass_case_count) / float(case_count)

        report = self.dingtalkReportContent() % (module_name, case_count, pass_case_count, failed_case_count,
                                                 pass_percent, report_detail)

        return report


    def WriteHtmlResult(self, case_result):
        # 生成文件名
        print("")

    def GenerateHTMLReport(self, case_result):
        html_content = ""
        # 首先填充头部数据
        module_name = case_result["module_name"]
        title = module_name + u"模块测试报告"

        computer = case_result["computer"]
        computer_architecture = case_result["computer_architecture"]
        computer_processor = case_result["computer_processor"]
        computer_name = case_result["computer_name"]

        start_time = case_result["start_time"]
        end_time = case_result["end_time"]
        escape_time = str(case_result["escape_time"])

        pass_case_count = case_result["pass_case_count"]
        failed_case_count = case_result["failed_case_count"]

        html_report_header = self.htmlReportHeader() % (title, module_name, computer, computer_architecture,
                                                        computer_processor, computer_name, start_time, end_time,
                                                        escape_time, pass_case_count, failed_case_count)

        html_content = html_content + html_report_header

        for case_result in case_result["case_results"]:
            # 用例ID
            case_id = case_result["case_info"]["case_id"]
            case_name = case_result["case_info"]["case_name"]
            interface_uri = case_result["case_info"]["interface_uri"]
            call_method = case_result["case_info"]["call_method"]
            repeat_count = case_result["case_info"]["repeat_count"]
            query_param = case_result["case_info"]["query_param"]
            body_param = case_result["case_info"]["body_param"]
            expected_result = case_result["case_info"]["expected_result"]
            real_result = case_result["interface_return"]

            result = ""
            if case_result["result"] == "P":
                result = u"<td bgcolor=\"green\">通过</td>"
            elif case_result["result"] == "F":
                result = u"<td bgcolor=\"fail\">不通过</td>"

            case_result_content = self.htmlReportContent() % (case_id, case_name, interface_uri, call_method,
                                                              repeat_count, query_param, body_param, expected_result,
                                                              real_result, result)


            html_content = html_content + case_result_content

        html_content = html_content + self.htmlReportTail()
        return html_content

    def htmlReportHeader(self):
        return u'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="GBK">
    <title>%s</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- 引入 Bootstrap -->
    <link href="https://cdn.bootcss.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
    <!-- HTML5 Shim 和 Respond.js 用于让 IE8 支持 HTML5元素和媒体查询 -->
    <!-- 注意： 如果通过 file://  引入 Respond.js 文件，则该文件无法起效果 -->
    <!--[if lt IE 9]>
     <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
     <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
    <style type="text/css">
        .hidden-detail,.hidden-tr{
            display:none;
        }
    </style>
</head>
<body>

    <div class="col-md-8 col-md-offset-8" style="margin-left:3%%;">
    <h1>%s服务 自动测试结果</h1>
	
	<table  class="table table-hover table-condensed">
    	<tbody>
    	    <tr><td><strong>测试机操作系统:</strong> %s</td></tr>
    	    <tr><td><strong>测试机处理器架构:</strong> %s</td></tr>
    	    <tr><td><strong>测试机处理器信息:</strong> %s</td></tr>
    	    <tr><td><strong>测试机名称:</strong> %s</td></tr>
        	<tr><td><strong>开始时间:</strong> %s</td></tr>
			<tr><td><strong>结束时间:</strong> %s</td></tr>
			<tr><td><strong>测试耗时:</strong> %s</td></tr>
			<tr>
				<td>
					<strong>结果:</strong>
					<span >
						通过: <strong >%d</strong>
						不通过: <strong >%d</strong>
					</span>
				</td>                  
			</tr> 
		</tbody>
	</table>
	</div>
	
	<div class="row" style="margin:60px">
        <div style="margin-top: 18%%;">
			<div class="btn-group" role="group" aria-label="...">
				<button type="button" id="check-all" class="btn btn-primary">所有用例</button>
				<button type="button" id="check-success" class="btn btn-success">成功用例</button>
				<button type="button" id="check-danger" class="btn btn-danger">失败用例</button>
				<button type="button" id="check-warning" class="btn btn-warning">错误用例</button>
				<button type="button" id="check-except" class="btn btn-defult">异常用例</button>
			</div>
			<div class="btn-group" role="group" aria-label="..."></div>
			<table class="table table-hover table-condensed table-bordered" style="word-wrap:break-word; word-break:break-all;  margin-top: 7px;">
				<tr>
					<td><strong>用例ID</strong></td>
					<td><strong>用例名称</strong></td>
					<td><strong>接口路径</strong></td>
					<td><strong>调用方法</strong></td>
					<td><strong>重复次数</strong></td>
					<td><strong>Query参数</strong></td>
					<td><strong>Body参数</strong></td>
					<td><strong>期望返回结果</strong></td>
					<td><strong>实际返回结果</strong></td>  
					<td><strong>是否通过测试</strong></td>
				</tr>
        '''

    def htmlReportContent(self):
        return u'''
        <tr class="case-tr %%s">
					<td>%s</td><!-- 用例ID -->
					<td>%s</td><!-- 用例名称 -->
					<td>%s</td><!-- 接口路径 -->
					<td>%s</td><!-- 调用方法 -->
					<td>%d</td><!-- 重复次数 -->
					<td>%s</td><!-- Query参数 -->
					<td>%s</td><!-- Body参数 -->
					<td>%s</td><!-- 期望返回结果 -->
					<td>%s</td><!-- 实际返回结果 -->
					%s
				</tr>
        '''

    def htmlReportTail(self):
        return u'''
        </table>
		</div>
	</div>
	<script src="https://code.jquery.com/jquery.js"></script>
	<script src="https://cdn.bootcss.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
	<script type="text/javascript">
	$("#check-danger").click(function(e){
	    $(".case-tr").removeClass("hidden-tr");
        $(".success").addClass("hidden-tr");
        $(".warning").addClass("hidden-tr");
        $(".error").addClass("hidden-tr");
	});
	$("#check-warning").click(function(e){
		 $(".case-tr").removeClass("hidden-tr");
        $(".success").addClass("hidden-tr");
        $(".danger").addClass("hidden-tr");
        $(".error").addClass("hidden-tr");
	});
	$("#check-success").click(function(e){
		 $(".case-tr").removeClass("hidden-tr");
        $(".warning").addClass("hidden-tr");
        $(".danger").addClass("hidden-tr");
        $(".error").addClass("hidden-tr");
	});
	$("#check-except").click(function(e){
		 $(".case-tr").removeClass("hidden-tr");
        $(".warning").addClass("hidden-tr");
        $(".danger").addClass("hidden-tr");
        $(".success").addClass("hidden-tr");
	});
	$("#check-all").click(function(e){
	    $(".case-tr").removeClass("hidden-tr");
	});
	</script>

</body>
</html>
        '''

    def dingtalkReportContent(self):
        return u"%s 模块接口自动化测试结果：\n" \
               u"已执行测试用例数量：%d\n" \
               u"测试通过：%d个\n" \
               u"测试未通过：%d个\n" \
               u"测试通过率：%.2f%%\n\n" \
               u"详情参考：%s"
