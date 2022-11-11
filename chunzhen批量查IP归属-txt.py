# -*- coding: utf-8 -*-
'''
@fucntion: 使用纯真ip数据库qqwry.dat批量查询txt内ip的归属地
https://soapffz.com/archives/245/
纯真IP数据库解析qqwry.dat库文件。 QQWry IP数据库 纯真版收集了包括中国电信、中国移动、中国联通、长城宽带、聚友宽带等 ISP 的最新准确 IP 地址数据。IP数据库每5天更新一次，需要定期更新最新的IP数据库。
下载qqwry.dat的地址：https://raw.githubusercontent.com/out0fmemory/qqwry.dat/master/qqwry_lastest.dat
pip install分别安装qqwry和IPy库
将要查询的ip放到ip.txt并和qqwry.dat、.py文件在同一个目录即可运行
'''

from qqwry import QQwry
from IPy import IP


def batch_query_and_print():
    q = QQwry()
    q.load_file('/Users/songzi/Desktop/ip/qqwry_lastest.dat')
    with open('/Users/songzi/Desktop/ip/1.txt') as f:
        ip_list = f.read().splitlines()
        for read_content in ip_list:
            try:
                IP(read_content)
            except Exception:
                print("有不符合规范的IP地址，请检查后重新运行")
                exit(0)
    address_list = [q.lookup(ip) for ip in ip_list]
    for i, j in zip(ip_list, address_list):
        query_results = f"{i} {j[0]} {j[1]}"
        print(query_results)
        with open("/Users/songzi/Desktop/ip/2.txt", 'a', encoding='utf-8') as f:
            f.writelines(query_results+"\n")


if __name__ == "__main__":
    batch_query_and_print()