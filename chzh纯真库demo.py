from qqwry import QQwry
from qqwry import updateQQwry


q = QQwry()
q.load_file('/Users/songzi/Desktop/ip/qqwry_lastest.dat')

print(q.is_loaded())
# q对象是否已加载数据，返回True或False

print(q.get_lastone())
# ('纯真网络', '2022年04月20日IP数据')

# 一般需要梯子
# filename = '/Users/songzi/Desktop/ip/qqwry_update.dat'
# ret = updateQQwry(filename)
# print(ret)
'''
当参数filename是str类型时，表示要保存的文件名。
成功后返回一个正整数，是文件的字节数；失败则返回一个负整数。

当参数filename是None时，函数直接返回qqwry.dat的文件内容（一个bytes对象）。
成功后返回一个bytes对象；失败则返回一个负整数。这里要判断一下返回值的类型是bytes还是int。

负整数表示的错误：
-1：下载copywrite.rar时出错
-2：解析copywrite.rar时出错
-3：下载qqwry.rar时出错
-4：qqwry.rar文件大小不符合copywrite.rar的数据
-5：解压缩qqwry.rar时出错
-6：保存到最终文件时出错
'''

print(q.lookup('8.8.8.8'))
# ('美国', '加利福尼亚州圣克拉拉县山景市谷歌公司DNS服务器')

print(q.lookup('114.114.114.114'))
# ('江苏省南京市', '南京信风网络科技有限公司GreatbitDNS服务器')
