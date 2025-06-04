# -*- coding: utf-8 -*-
'''
@fucntion: 使用纯真ip数据库qqwry.dat批量查询txt内ip的归属地
https://soapffz.com/archives/245/
纯真IP数据库解析qqwry.dat库文件。 QQWry IP数据库 纯真版收集了包括中国电信、中国移动、中国联通、长城宽带、聚友宽带等 ISP 的最新准确 IP 地址数据。IP数据库每5天更新一次，需要定期更新最新的IP数据库。
下载qqwry.dat的地址：https://raw.githubusercontent.com/out0fmemory/qqwry.dat/master/qqwry_lastest.dat
pip install分别安装qqwry和IPy库
将要查询的ip放到ip.txt并和qqwry.dat、.py文件在同一个目录即可运行
'''

import os
import sys
from qqwry import QQwry
from IPy import IP

def batch_query_and_print():
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 检查qqwry_lastest.dat文件是否存在
    db_path = os.path.join(script_dir, "qqwry_lastest.dat")
    if not os.path.exists(db_path):
        print("错误: 脚本所在目录下未找到qqwry_lastest.dat文件")
        print("请从以下地址下载: https://raw.githubusercontent.com/out0fmemory/qqwry.dat/master/qqwry_lastest.dat")
        sys.exit(1)
    
    # 查找脚本所在目录下的所有txt文件
    txt_files = [f for f in os.listdir(script_dir) if f.endswith('.txt') and f != "qqwry_lastest.dat"]
    
    if not txt_files:
        print("错误: 脚本所在目录下未找到txt文件")
        sys.exit(1)
    
    # 显示txt文件列表供用户选择
    print("找到以下txt文件:")
    for i, filename in enumerate(txt_files, 1):
        print(f"{i}. {filename}")
    
    # 获取用户选择
    while True:
        try:
            choice = int(input("请输入要查询的txt文件编号: "))
            if 1 <= choice <= len(txt_files):
                selected_file = txt_files[choice - 1]
                break
            else:
                print("输入无效，请输入有效的编号")
        except ValueError:
            print("输入无效，请输入数字")
    
    # 读取选中的txt文件中的IP地址
    input_file_path = os.path.join(script_dir, selected_file)
    try:
        with open(input_file_path, 'r') as f:
            ip_list = f.read().splitlines()
    except Exception as e:
        print(f"读取文件失败: {e}")
        sys.exit(1)
    
    # 验证IP地址格式
    invalid_ips = []
    for ip in ip_list:
        try:
            IP(ip)
        except Exception:
            invalid_ips.append(ip)
    
    if invalid_ips:
        print("发现不符合规范的IP地址:")
        for ip in invalid_ips:
            print(f"- {ip}")
        print("请检查并修正后重新运行")
        sys.exit(1)
    
    # 加载IP数据库并查询
    q = QQwry()
    q.load_file(db_path)
    
    # 准备输出文件路径
    output_filename = f"{os.path.splitext(selected_file)[0]}_result.txt"
    output_file_path = os.path.join(script_dir, output_filename)
    
    # 执行查询并写入结果
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f_out:
            for ip in ip_list:
                result = q.lookup(ip)
                if result:
                    country, area = result
                    query_results = f"{ip} {country} {area}"
                else:
                    query_results = f"{ip} 未找到匹配信息"
                
                print(query_results)
                f_out.write(query_results + "\n")
        
        print(f"\n查询完成，结果已保存到: {output_file_path}")
    except Exception as e:
        print(f"写入结果失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    batch_query_and_print()    
