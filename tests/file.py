import os
import time

time.ctime(os.stat(__file__).st_mtime)  # 文件的修改时间
time.ctime(os.stat(__file__).st_ctime)  # 文件的创建时间

time.localtime(os.stat(__file__).st_mtime)  # 文件访问时间 适合计算时间
# 上面不予赘述 , 用一个做以示例

ModifiedTime = time.localtime(os.stat(__file__).st_mtime)  # 文件访问时间
y = time.strftime('%Y', ModifiedTime)
m = time.strftime('%m', ModifiedTime)
d = time.strftime('%d', ModifiedTime)
H = time.strftime('%H', ModifiedTime)
M = time.strftime('%M', ModifiedTime)

print("文件信息打印 ...")
print("Year:%s / Month:%s / Day:%s / Hour:%s / Min:%s" % (y, m, d, H, M))

# 输出
"""
文件信息打印 ...
Year:2019 / Month:09 / Day:11 / Hour:16 / Min:50
"""
