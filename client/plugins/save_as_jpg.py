# import win32ui
#
# dlg = win32ui.CreateFileDialog(1)
# # dlg.Multiselect = True
# dlg.SetMultiselect(True)
# dlg.SetOFNInitialDir('.')  # 设置打开文件对话框中的初始显示目录
# dlg.DoModal()
# filename = dlg.GetPathName()  # 获取选择的文件名称
# print(filename)
import tkinter as tk
import os
from tkinter import filedialog
from PIL import Image

# BASE_DIR = os.path.dirname(os.getcwd())
BASE_DIR = os.getcwd()
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilenames(initialdir=BASE_DIR)
os.mkdir(os.path.join(BASE_DIR, 'jpg'))
for item in file_path:
    im = Image.open(item)
    im.save()