import os
code = ['.py', '.kv']
total = 0
for dirn, dirns, filens in os.walk('.'):
    for f in filens:
        for e in code:
            if f.endswith(e):
                v = len(open(f'{dirn}/{f}').readlines())
                total += v
                print(f"文件{dirn}/{f}有码{v}行，共{total}行。")