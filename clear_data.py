"""
本脚本用于清除所有数据，恢复到原始状态。

"""

#! Attention: 所有注册用户和用户上传的文件数据都会丢失！

if __name__ == '__main__':
    import csv, os
    dbroot = 'src/database'
    fileds = csv.DictReader(open(f'{dbroot}/logs.csv', 'r', encoding='utf-8')).fieldnames
    writer = csv.DictWriter(open(f'{dbroot}/logs.csv', 'w', encoding='utf-8'), fileds)
    writer.writerow({
        f: f
        for f in fileds
    })
    open(f'{dbroot}/users.db', 'wb')
    fileroot = f'{dbroot}/fileroot'
    dirs = []
    for dirn, dirns, filens in os.walk(fileroot):
        for filen in filens:
            os.remove(f'{dirn}/{filen}')
        for dn in dirns:
            dirs.insert(0, f'{dirn}/{dn}')
    for d in dirs:
        os.rmdir(d)