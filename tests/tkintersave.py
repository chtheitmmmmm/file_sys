import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename

root = tkinter.Tk()
root.title = "保存文件"

fn = asksaveasfilename(
    title='导出为PNG图片fewfwefwefefwefwefwefwefeefefwef导出为PNG图片fewfwefwefefwefwefwefwefeefefwef导出为PNG图片fewfwefwefefwefwefwefwefeefefwef导出为PNG图片fewfwefwefefwefwefwefwefeefefwef导出为PNG图片fewfwefwefefwefwefwefwefeefefwef',
    defaultextension='.png'
)
print(fn)