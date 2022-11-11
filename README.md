# IP-地址查询与分析


工作中经常要写报告，其中要分析国外以及港澳台地区的IP数量，没有找到合适的在线网站，最多一次也就100或者300个IP，但是工作中IP地址还有国内的，超级多。


所以，利用纯真IP地址库来本地查询IP地址归属。


使用纯真ip数据库qqwry.dat批量查询txt内ip的归属地

https://soapffz.com/archives/245/

纯真IP数据库解析qqwry.dat库文件。 QQWry IP数据库 纯真版收集了包括中国电信、中国移动、中国联通、长城宽带、聚友宽带等 ISP 的最新准确 IP 地址数据。IP数据库每5天更新一次，需要定期更新最新的IP数据库。

下载qqwry.dat的地址：https://raw.githubusercontent.com/out0fmemory/qqwry.dat/master/qqwry_lastest.dat

pip install分别安装qqwry和IPy库

将要查询的ip放到ip.txt并和qqwry.dat、.py文件在同一个目录即可运行

'''

Excel表格式：

    A：ip  B：数量  C：国家  D：地区
    
    A1     B1      C1      D1  
    
   →A2                     从这里开始读IP，开始查询，查询写入第三、四列


   Sheet1                  默认从这里加载数据
   
'''
