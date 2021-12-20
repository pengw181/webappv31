# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/9/13 下午5:49


from app.VisualModeler.doctorwho.doctor_who import DoctorWho
from app.VisualModeler.process_editor.process.draw.process_info import Process
from app.VisualModeler.process_editor.process.draw.draw_process import DrawProcess
from app.VisualModeler.commonInfo.proxy import Proxy
from app.VisualModeler.commonInfo.field import ProfessionField
from app.VisualModeler.commonInfo.database import Database
from app.VisualModeler.commonInfo.script import Script
from app.VisualModeler.commonInfo.mailbox import Mail
from app.VisualModeler.commonInfo.ftp import FTP
from app.VisualModeler.commonInfo.system import ThirdSystem
from app.VisualModeler.commonInfo.interface import Interface
from app.VisualModeler.commonInfo.file import File
from app.VisualModeler.cmd.cmd_set import CmdSet
from app.VisualModeler.cmd.relurX import RulerX
from app.VisualModeler.cmd.regexp_template import RegexpTemplate
from common.log.logger import log
from app.com.wrapper.auto_login import auto_enter_vm


@auto_enter_vm
def actions(func, param):

    run_flag = True

    if func == "ChooseMenu":
        action = DoctorWho()
        action.choose_menu(menu_path=param.get("菜单"))

    elif func == "AddProcess":
        action = Process()
        action.add(process_name=param.get("流程名称"), field=param.get("专业领域"), process_type=param.get("流程类型"),
                   exec_mode=param.get("执行模式"), process_desc=param.get("流程说明"), advance_set=param.get("高级配置"))

    elif func == "UpdateProcess":
        action = Process()
        update_map = param.get("修改内容")
        action.update(obj=param.get("流程名称"), process_name=update_map.get("流程名称"), field=update_map.get("专业领域"),
                      exec_mode=update_map.get("执行模式"), process_desc=update_map.get("流程说明"),
                      advance_set=update_map.get("高级配置"))

    elif func == "DeleteProcess":
        action = Process()
        action.delete(obj=param.get("流程名称"))

    elif func == "ProcessDataClear":
        action = Process()
        action.data_clear(obj=param.get("流程名称"))

    elif func == "AddNode":
        action = DrawProcess(process_name=param.get("流程名称"))
        action.locate_node(node_type=param.get("节点类型"))

    elif func == "SetEndNode":
        action = DrawProcess(process_name=param.get("流程名称"))
        action.set_end_node(status=param.get("状态"))

    elif func == "NodeBusinessConf":
        action = DrawProcess(process_name=param.get("流程名称"))
        action.node_business_conf(node_type=param.get("节点类型"), node_name=param.get("节点名称"), **param.get("业务配置"))

    elif func == "NodeFetchConf":
        action = DrawProcess(process_name=param.get("流程名称"))
        action.node_fetch_conf(node_type=param.get("节点类型"), node_name=param.get("节点名称"), **param.get("取数配置"))

    elif func == "NodeOptConf":
        action = DrawProcess(process_name=param.get("流程名称"))
        action.node_operate_conf(node_type=param.get("节点类型"), node_name=param.get("节点名称"), array=param.get("操作配置"))

    elif func == "LineNode":
        action = DrawProcess(process_name=param.get("流程名称"))
        action.combine(source_node_name=param.get("起始节点名称"), target_node_name=param.get("终止节点名称"),
                       logic=param.get("关联关系"))

    elif func == "AddProxy":
        action = Proxy()
        action.add(proxy_name=param.get("代理名称"), ip=param.get("代理服务器"), port=param.get("代理端口"),
                   username=param.get("代理用户名"), pwd=param.get("代理密码"), protocol=param.get("代理协议"),
                   enable=param.get("是否有效"), data_type=param.get("数据类型"))

    elif func == "UpdateProxy":
        action = Proxy()
        update_map = param.get("修改内容")
        action.update(obj=param.get("代理名称"), proxy_name=update_map.get("代理名称"), ip=update_map.get("代理服务器"),
                      port=update_map.get("代理端口"), username=update_map.get("代理用户名"), pwd=update_map.get("代理密码"),
                      protocol=update_map.get("代理协议"), enable=update_map.get("是否有效"), data_type=update_map.get("数据类型"))

    elif func == "DeleteProxy":
        action = Proxy()
        action.delete(obj=param.get("代理名称"))

    elif func == "ProxyDataClear":
        action = Proxy()
        action.data_clear(obj=param.get("代理名称"))

    elif func == "AddField":
        action = ProfessionField()
        action.add(field_name=param.get("专业领域名称"))

    elif func == "UpdateField":
        action = ProfessionField()
        update_map = param.get("修改内容")
        action.update(obj=param.get("专业领域名称"), field_name=update_map.get("专业领域名称"))

    elif func == "DeleteField":
        action = ProfessionField()
        action.delete(obj=param.get("专业领域名称"))

    elif func == "FieldDataClear":
        action = ProfessionField()
        action.data_clear(obj=param.get("专业领域名称"))

    elif func == "AddDatabase":
        action = Database()
        action.add(db_name=param.get("数据库名称"), db_driver=param.get("数据库驱动"), db_url=param.get("数据库URL"),
                   username=param.get("用户名"), pwd=param.get("密码"), belong_type=param.get("归属类型"),
                   data_type=param.get("数据类型"))

    elif func == "UpdateDatabase":
        action = Database()
        update_map = param.get("修改内容")
        action.update(obj=param.get("数据库名称"), db_name=update_map.get("数据库名称"), db_driver=update_map.get("数据库驱动"),
                      db_url=update_map.get("数据库URL"), username=update_map.get("用户名"), pwd=update_map.get("密码"),
                      belong_type=update_map.get("归属类型"), data_type=update_map.get("数据类型"))

    elif func == "TestDatabase":
        action = Database()
        action.test(obj=param.get("数据库名称"))

    elif func == "DeleteDatabase":
        action = Database()
        action.delete(obj=param.get("数据库名称"))

    elif func == "DBDataClear":
        action = Database()
        action.data_clear(obj=param.get("数据库名称"))

    elif func == "AddScript":
        action = Script()
        action.add(script_name=param.get("脚本名称"), script_type=param.get("脚本类型"), data_type=param.get("数据类型"))

    elif func == "UpdateScript":
        action = Script()
        update_map = param.get("修改内容")
        action.update(obj=param.get("脚本名称"), script_name=update_map.get("脚本名称"), data_type=update_map.get("数据类型"))

    elif func == "SaveNewScriptVersion":
        action = Script()
        action.choose_version(script_name=param.get("脚本名称"), ver_no=param.get("版本号"))
        action.save_new_version()

    elif func == "AddScriptParams":
        action = Script()
        action.add_param(script_name=param.get("脚本名称"), ver_no=param.get("版本号"), params=param.get("脚本参数"))

    elif func == "UpdateScriptParams":
        action = Script()
        action.update_param(script_name=param.get("脚本名称"), ver_no=param.get("版本号"), params=param.get("脚本参数"))

    elif func == "DownloadScriptVersion":
        action = Script()
        action.download_version(script_name=param.get("脚本名称"), ver_no=param.get("版本号"))

    elif func == "DeleteScriptVersion":
        action = Script()
        action.delete_version(script_name=param.get("脚本名称"), ver_no=param.get("版本号"))

    elif func == "SubmitScriptApproval":
        action = Script()
        action.submit_for_approval(script_name=param.get("脚本名称"), ver_no=param.get("版本号"))

    elif func == "UploadScriptFile":
        action = Script()
        action.upload_script_file(script_name=param.get("脚本名称"), ver_no=param.get("版本号"), file_name=param.get("脚本文件名"))

    elif func == "ScriptFileRClick":
        action = Script()
        action.script_file_r_click(script_name=param.get("脚本名称"), ver_no=param.get("版本号"), file_name=param.get("脚本文件名"),
                                   operate=param.get("右键"))

    elif func == "UpdateScriptFileContent":
        action = Script()
        action.update_script_content(script_name=param.get("脚本名称"), ver_no=param.get("版本号"), file_name=param.get("脚本文件名"),
                                     content=param.get("脚本内容"))

    elif func == "DeleteScript":
        action = Script()
        action.delete(obj=param.get("脚本名称"))

    elif func == "ScriptDataClear":
        action = Script()
        action.data_clear(obj=param.get("脚本名称"))

    elif func == "AddMail":
        action = Mail()
        action.add(mail_addr=param.get("邮箱地址"), mail_type=param.get("邮箱类型"), data_type=param.get("数据类型"),
                   send_protocol=param.get("发送协议类型"), send_server=param.get("发送服务器地址"), send_port=param.get("发送端口"),
                   receive_protocol=param.get("接收协议类型"), receive_server=param.get("接收服务器地址"),
                   receive_port=param.get("接收端口"), username=param.get("账号"), pwd=param.get("密码或授权码"),
                   proxy_name=param.get("代理名称"), platf_account=param.get("平台账号"))

    elif func == "UpdateMail":
        action = Mail()
        update_map = param.get("修改内容")
        action.update(obj=param.get("邮箱地址"), mail_addr=update_map.get("邮箱地址"), mail_type=update_map.get("邮箱类型"),
                      data_type=update_map.get("数据类型"), send_protocol=update_map.get("发送协议类型"),
                      send_server=update_map.get("发送服务器地址"), send_port=update_map.get("发送端口"),
                      receive_protocol=update_map.get("接收协议类型"), receive_server=update_map.get("接收服务器地址"),
                      receive_port=update_map.get("接收端口"), username=update_map.get("账号"), pwd=update_map.get("密码或授权码"),
                      proxy_name=update_map.get("代理名称"), platf_account=update_map.get("平台账号"))

    elif func == "TestMail":
        action = Mail()
        action.test(obj=param.get("邮箱地址"))

    elif func == "DeleteMail":
        action = Mail()
        action.delete(obj=param.get("邮箱地址"))

    elif func == "MailDataClear":
        action = Mail()
        action.data_clear(obj=param.get("邮箱地址"))

    elif func == "AddFTP":
        action = FTP()
        action.add(server_name=param.get("服务器名称"), ip=param.get("服务器IP"), port=param.get("服务器端口"),
                   username=param.get("用户名"), pwd=param.get("密码"), server_type=param.get("服务器类型"),
                   encoding=param.get("服务器编码"), data_type=param.get("数据类型"))

    elif func == "UpdateFTP":
        action = FTP()
        update_map = param.get("修改内容")
        action.update(obj=param.get("服务器名称"), server_name=update_map.get("服务器名称"), ip=update_map.get("服务器IP"),
                      port=update_map.get("服务器端口"), username=update_map.get("用户名"), pwd=update_map.get("密码"),
                      server_type=update_map.get("服务器类型"), encoding=update_map.get("服务器编码"),
                      data_type=update_map.get("数据类型"))

    elif func == "TestFTP":
        action = FTP()
        action.test(obj=param.get("服务器名称"))

    elif func == "DeleteFTP":
        action = FTP()
        action.delete(obj=param.get("服务器名称"))

    elif func == "FTPDataClear":
        action = FTP()
        action.data_clear(obj=param.get("服务器名称"))

    elif func == "AddThirdSystem":
        action = ThirdSystem()
        action.add(platform=param.get("平台名称"), visit_url=param.get("平台地址"), network_tag=param.get("平台网络标识"),
                   browser_type=param.get("浏览器类型"), browser_timeout=param.get("浏览器超时时间"),
                   session_timeout=param.get("空闲刷新时间"), data_type=param.get("数据类型"),
                   first_click_set=param.get("是否优先点击页面元素"), enable_proxy_set=param.get("是否启用代理"),
                   enable_login_set=param.get("是否验证登录"))

    elif func == "TestThirdSystem":
        action = ThirdSystem()
        action.test(obj=param.get("平台名称"))

    elif func == "UpdateThirdSystem":
        action = ThirdSystem()
        update_map = param.get("修改内容")
        action.update(obj=param.get("平台名称"), platform=update_map.get("平台名称"), visit_url=update_map.get("平台地址"),
                      network_tag=update_map.get("平台网络标识"), browser_type=update_map.get("浏览器类型"),
                      browser_timeout=update_map.get("浏览器超时时间"), session_timeout=update_map.get("空闲刷新时间"),
                      data_type=update_map.get("数据类型"), first_click_set=update_map.get("是否优先点击页面元素"),
                      enable_proxy_set=update_map.get("是否启用代理"), enable_login_set=update_map.get("是否验证登录"))

    elif func == "DeleteThirdSystem":
        action = ThirdSystem()
        action.delete(obj=param.get("平台名称"))

    elif func == "ThirdSystemDataClear":
        action = ThirdSystem()
        action.data_clear(obj=param.get("平台名称"))

    elif func == "AddInterface":
        action = Interface()
        action.add(interface_name=param.get("接口名称"), interface_type=param.get("接口类型"),
                   interface_url=param.get("接口url"), data_type=param.get("数据类型"),
                   interface_namespace=param.get("接口空间名"), interface_method=param.get("接口方法名"),
                   request_type=param.get("请求方式"), timeout=param.get("超时时间"), proxy_name=param.get("代理名称"),
                   result_sample=param.get("返回结果样例"), request_header=param.get("接口请求头"),
                   request_parameter=param.get("接口参数"), request_body=param.get("请求体内容"))

    elif func == "TestInterface":
        action = Interface()
        action.test(obj=param.get("接口名称"))

    elif func == "UpdateInterface":
        action = Interface()
        update_map = param.get("修改内容")
        action.update(obj=param.get("接口名称"), interface_name=update_map.get("接口名称"),
                      interface_type=update_map.get("接口类型"), interface_url=update_map.get("接口url"),
                      data_type=update_map.get("数据类型"), interface_namespace=update_map.get("接口空间名"),
                      interface_method=update_map.get("接口方法名"), request_type=update_map.get("请求方式"),
                      timeout=update_map.get("超时时间"), proxy_name=update_map.get("代理名称"),
                      result_sample=update_map.get("返回结果样例"), request_header=update_map.get("接口请求头"),
                      request_parameter=update_map.get("接口参数"), request_body=update_map.get("请求体内容"))

    elif func == "DeleteInterface":
        action = Interface()
        action.delete(obj=param.get("接口名称"))

    elif func == "InterfaceDataClear":
        action = Interface()
        action.data_clear(obj=param.get("接口名称"))

    elif func == "MkDir":
        action = File(catalog=param.get("目录分类"))
        action.mkdir(parent_dir=param.get("目标目录"), dir_name=param.get("目录名"))

    elif func == "UpdateDir":
        action = File(catalog=param.get("目录分类"))
        action.update_dir(target_dir=param.get("目标目录"), new_dir=param.get("目录名"))

    elif func == "DeleteDir":
        action = File(catalog=param.get("目录分类"))
        action.delete_dir(dir_name=param.get("目标目录"))

    elif func == "UploadFile":
        action = File(catalog=param.get("目录分类"))
        action.upload_file(dir_name=param.get("目标目录"), file_name=param.get("文件名"))

    elif func == "DownloadFile":
        action = File(catalog=param.get("目录分类"))
        action.download_file(dir_name=param.get("目标目录"), file_name=param.get("文件名"))

    elif func == "DeleteFile":
        action = File(catalog=param.get("目录分类"))
        action.delete_file(dir_name=param.get("目标目录"), file_name=param.get("文件名"))

    elif func == "DownloadFileBatch":
        action = File(catalog=param.get("目录分类"))
        action.download_file_batch(dir_name=param.get("目标目录"), file_names=param.get("文件名"))

    elif func == "DeleteFileBatch":
        action = File(catalog=param.get("目录分类"))
        action.delete_file_batch(dir_name=param.get("目标目录"), file_names=param.get("文件名"))

    elif func == "DirDataClear":
        action = File(catalog=param.get("目录分类"))
        action.data_clear(obj=param.get("目标目录"))

    elif func == "AddCmdSet":
        action = CmdSet()
        action.add(cmd_name=param.get("指令名称"), cmd_category=param.get("指令类别"), cmd_use=param.get("指令用途"),
                   level=param.get("网元分类"), vendor=param.get("厂家"), netunit_model=param.get("设备型号"),
                   login_type=param.get("登录模式"), public_cmd=param.get("公有指令"), sensitive_cmd=param.get("隐藏输入指令"),
                   personal_cmd=param.get("个性指令"), cmd_timeout=param.get("指令等待超时"), command=param.get("指令"),
                   remark=param.get("说明"), rulerx_analyzer=param.get("指令解析模版"), cmd_pagedown=param.get("指令翻页符"),
                   expected_return=param.get("期待返回的结束符"), sensitive_regex=param.get("隐藏指令返回"))

    elif func == "CmdSetDataClear":
        action = CmdSet()
        action.data_clear(obj=param.get("指令名称"), fuzzy_match=param.get("模糊匹配"))

    elif func == "AddRulerX":
        action = RulerX()
        action.add(basic_cfg=param.get("基本信息配置"), result_format_cfg=param.get("结果格式化配置"),
                   segment_cfg=param.get("分段规则配置"), format_table_cfg=param.get("格式化二维表配置"),
                   judge_ruler=param.get("选择判断规则"), judge_cfg=param.get("判断规则配置"))

    elif func == "RulerXDataClear":
        action = RulerX()
        # action.data_clear(obj=param.get("指令名称"), fuzzy_match=param.get("模糊匹配"))

    elif func == "AddRegexpTemp":
        action = RegexpTemplate()
        action.add(regexp_name=param.get("模版名称"), remark=param.get("模版描述"), regexp_info=param.get("正则魔方"))

    elif func == "RegexpTempDataClear":
        action = RegexpTemplate()
        action.data_clear(obj=param.get("正则模版名称"), fuzzy_match=param.get("模糊匹配"))

    else:
        log.error("无效的动作函数")
        run_flag = False

    return run_flag


"""
    {
        "操作": "AddInterface",
        "参数": {
            "接口名称": "pw测试第三方restful接口",
            "接口类型": "restful",
            "接口url": ["http://192.168.88.228:5009/mock/http/notify"],
            "数据类型": "公有",
            "请求方式": "get",                   
            "超时时间": "30",
            "返回结果样例": {
                "结果类型": "字符串",
                "结果样例": "Interface request date save to database successfully!"
            },
            "接口请求头": [
                {
                    "参数名称": "名称",
                    "参数类型": "字符",
                    "参数默认值": "张三"
                },
                {
                    "参数名称": "年龄",
                    "参数类型": "数值",
                    "参数默认值": "20"
                },
                {
                    "参数名称": "地点",
                    "参数类型": "字符",
                    "参数默认值": "广州"
                }
            ],
            "请求体内容": {
                "请求体内容类型": "json",
                "请求体内容": {
                    "type": 1,
                    "name": "abc"
                }
            }
        }
    }

    {
        "操作": "DeleteInterface",
        "参数": {
            "接口名称": "pw测试第三方restful接口_nodify"
        }
    }

    {
        "操作": "InterfaceDataClear",
        "参数": {
            "接口名称": "pw测试第三方restful接口_nodify"
        }
    }

    {
        "操作": "UpdateInterface",
        "参数": {
            "接口名称": "pw测试第三方restful接口_nodify",
            "修改内容": {
                "接口名称": "pw测试第三方restful接口",
                "接口类型": "restful",
                "接口url": ["http://192.168.88.228:5009/mock/http/notify"],
                "数据类型": "公有",
                "请求方式": "put",                   
                "超时时间": "30",
                "代理名称": "自动化测试代理",
                "返回结果样例": {
                    "结果类型": "字符串",
                    "结果样例": "Interface request date save to database successfully!"
                },
                "接口请求头": [
                    {
                        "参数名称": "名称",
                        "参数类型": "字符",
                        "参数默认值": "张三"
                    },
                    {
                        "参数名称": "年龄",
                        "参数类型": "数值",
                        "参数默认值": "20"
                    },
                    {
                        "参数名称": "地点",
                        "参数类型": "字符",
                        "参数默认值": "广州"
                    }
                ],
                "请求体内容": {
                    "请求体内容类型": "json",
                    "请求体内容": {
                        "type": 1,
                        "name": "abc"
                    }
                }
            }
        }
    }

    {
        "操作": "ElementConfiguration",
        "参数": {
            "模版名称": "pw自动化测试爬虫模版",
            "元素配置": [
                {
                    "元素名称": "点击按钮",
                    "元素类型": "按钮",
                    "动作": "单击",
                    "标识类型": "xpath",
                    "元素标识": "//*[@id='btn']",
                    "描述": "点击按钮动作"
                }
            ]
        }
    }

    
    {
        "操作": "AddRulerX",
        "参数": {
            "基本信息配置": {
                "模版名称": "自动化ping解析模版",
                "模版说明": ["自动化ping解析模版"]
            },
            "结果格式化配置": {
                "分段": "否",
                "格式化成二维表": "是"
            },
            "格式化二维表配置": {
                "解析开始行": "1",
                "通过正则匹配数据列": "是",
                "正则魔方": {
                    "设置方式": "添加",
                    "正则模版名称": "ping指令解析",
                    "标签配置": [
                        {
                            "标签": "任意字符",
                            "值": "1到多个",
                            "是否取值": "无"
                        },
                        {
                            "标签": "空格",
                            "值": "1到多个",
                            "是否取值": "无"
                        },
                        {
                            "标签": "数字",
                            "值": "1到多个",
                            "是否取值": "绿色"
                        },
                        {
                            "标签": "自定义文本",
                            "值": "%",
                            "是否取值": "无"
                        },
                        {
                            "标签": "空格",
                            "值": "1到多个",
                            "是否取值": "无"
                        },
                        {
                            "标签": "自定义文本",
                            "值": "packet loss",
                            "是否取值": "无"
                        },
                        {
                            "标签": "任意字符",
                            "值": "1到多个",
                            "是否取值": "无"
                        }
                    ]
                },
                "样例数据": "ping_sample.txt"
            },
            "选择判断规则": "二维表结果判断",
            "判断规则配置": {
                "目标行": "所有行",
                "行结果关系": "或",
                "规则管理": [
                    {
                        "列名": "列1",
                        "关系": "不等于",
                        "匹配值": "0",
                        "条件满足时": "异常",
                        "匹配不到值时": "无数据进行规则判断",
                        "异常提示信息": "出现丢包率"
                    }
                ]
            }
        }
    }
    
    
    
    {
        "操作": "AddRulerX",
        "参数": {
            "基本信息配置": {
                "模版名称": "自动化板卡状态解析模版",
                "模版说明": ["自动化板卡状态解析模版"]
            },
            "结果格式化配置": {
                "分段": "否",
                "格式化成二维表": "是"
            },
            "格式化二维表配置": {
                "解析开始行": "1",
                "通过正则匹配数据列": "是",
                "正则魔方": {
                    "设置方式": "添加",
                    "正则模版名称": "板卡状态检查指令解析",
                    “高级模式”: "是",
                    "表达式": "(\\d+)\\s+(\\w+)\\s+(\\w+)\\s+(\\w+)\\s+(\\w+)\\s+(\\w+)\\s+"
                },
                "样例数据": "board_status_sample.txt"
            },
            "选择判断规则": "二维表结果判断",
            "判断规则配置": {
                "目标行": "所有行",
                "行结果关系": "且",
                "规则管理": [
                    {
                        "列名": "列5",
                        "关系": "等于",
                        "匹配值": "Normal",
                        "条件满足时": "正常",
                        "匹配不到值时": "无数据进行规则判断",
                        "异常提示信息": "板卡状态出现异常"
                    }
                ]
            }
        }
    }
    
    
    
    {
        "操作": "AddRulerX",
        "参数": {
            "基本信息配置": {
                "模版名称": "自动化date解析模版",
                "模版说明": ["自动化date解析模版"]
            },
            "结果格式化配置": {
                "分段": "否",
                "格式化成二维表": "是"
            },
            "格式化二维表配置": {
                "解析开始行": "1",
                "通过正则匹配数据列": "是",
                "正则魔方": {
                    "设置方式": "添加",
                    "正则模版名称": "date指令解析",
                    "标签配置": [
                        {
                            "标签": "任意字符",
                            "值": "1到多个",
                            "是否取值": "无"
                        },
                        {
                            "标签": "空格",
                            "值": "1到多个",
                            "是否取值": "无"
                        },
                        {
                            "标签": "数字",
                            "值": "1到多个",
                            "是否取值": "绿色"
                        },
                        {
                            "标签": "自定义文本",
                            "值": ":",
                            "是否取值": "无"
                        },
                        {
                            "标签": "数字",
                            "值": "1到多个",
                            "是否取值": "绿色"
                        },
                        {
                            "标签": "自定义文本",
                            "值": ":",
                            "是否取值": "无"
                        },
                        {
                            "标签": "数字",
                            "值": "1到多个",
                            "是否取值": "绿色"
                        },
                        {
                            "标签": "任意字符",
                            "值": "1到多个",
                            "是否取值": "无"
                        }
                    ]
                },
                "样例数据": "date_sample.txt"
            },
            "选择判断规则": "无需判断"
        }
    }
    
    
    {
        
        "操作": "AddRegexpTemp",
        "参数": {
            "模版名称": "自动化正则模版",
            "模版描述": "自动化正则模版描述，勿删",
            "正则魔方": {
                "标签配置": [
                    {
                        "标签": "自定义文本",
                        "自定义值": "pw",
                        "是否取值": "黄色"
                    },
                    {
                        "标签": "任意字符",
                        "长度": "1到多个",
                        "是否取值": "绿色"
                    },
                    {
                       "标签": "数字",
                        "正数负数": "正数",
                        "匹配小数": "是",
                        "匹配%": "是",
                        "匹配千分位": "是",
                        "匹配并去掉逗号": "是",
                        "长度": "1到多个",
                        "是否取值": "绿色"
                    },
                    {
                        "标签": "特殊字符",
                        "特殊字符": "$",
                        "长度": "1到多个",
                        "是否取值": "绿色"
                    },
                    {
                        "标签": "IP",
                        "IPV4": "是",
                        "IPV6": "是",
                        "是否取值": "绿色"
                    }
                ],
                "开启验证": "是",
                "验证信息": "ping_sample.txt"
            }
        }
    }
    
    """
