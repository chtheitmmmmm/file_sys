import os
from PIL import Image

#print(os.listdir())

import tkintertry

from tkintertry import filedialog

root = tkinter.Tk()    # 创建一个Tkinter.Tk()实例

root.withdraw()      # 将Tkinter.Tk()实例隐藏

default_dir = r"/Users/chengmin/code"

#file_path = tkinter.filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(default_dir)))

file_path = filedialog.askdirectory(initialdir=default_dir)
print(file_path)


