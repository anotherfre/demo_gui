# -*- coding: utf-8 -*-
from tkinter import *
import threading
from tkinter.filedialog import askopenfilename
import traceback
import tkinter.messagebox as mb
import win32gui
from mbpipei import *
import pywinauto


def thread_it(func, *args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()


def get_app_info():
    hwnd = win32gui.FindWindow(r"Win32Window", u"阴阳师-网易游戏")
    hwnd = win32gui.GetWindowRect(hwnd)
    return hwnd


class App:
    def __init__(self):
        root = Tk()
        root.title('Lets Start')
        # root.geometry("300x200")
        self.path = StringVar()
        self._flag = threading.Event()
        self._flag.clear()

        _label = Label(root, text='路径:').grid(row=0, column=0)
        self._button_choose = Button(root, text='选择程序', command=self.select_path).grid(row=0, column=2)
        self._button_start = Button(root, text='启动程序', command=lambda: thread_it(self.start_app)).grid(row=0, column=3)

        _entry = Entry(root, textvariable=self.path).grid(row=0, column=1)
        if os.path.exists('script_cache/app_cache.txt'):
            with open("script_cache/app_cache.txt", 'r', encoding='utf-8') as file:
                file_cont = file.read()
                self.path.set(file_cont)

        self._text = Text(root, height=6, width=50)
        if os.path.exists('script_cache/script_cache.txt'):
            with open("script_cache/script_cache.txt", 'r', encoding='utf-8') as file:
                file_cont = file.read()
                self._text.insert(INSERT, file_cont)
        self._text.grid(row=1, columnspan=4)
        self._button_script = Button(root, text="执行/终止", command=lambda: thread_it(self.script_status))
        self._button_script.grid(row=2, columnspan=4)

        self.make_dirs()

        root.mainloop()

    @staticmethod
    def make_dirs():
        if not os.path.exists('reg_images'):
            os.mkdir('reg_images')
        if not os.path.exists('script_cache'):
            os.mkdir('script_cache')

    def select_path(self):
        """
        选择程序路径
        :return:
        """
        _path = askopenfilename()
        self.path.set(_path)
        with open("script_cache/app_cache.txt", 'w+', encoding='utf-8') as file:
            file_cont = file.read()
            if file_cont != _path:
                file.write(_path)

    def start_app(self):
        """
        启动程序
        :return:
        """
        if self.path.get() == '':
            mb.showinfo('提示', '请先选择程序路径')
            return 0
        try:
            try:
                pywinauto.Application('win32').connect(path="onmyoji.exe")
            except:
                pywinauto.Application(backend="win32").start(self.path.get())
        except:
            print(traceback.format_exc())
            mb.showinfo('信息', '启动失败')

    def start_script(self):

        try:
            content = self._text.get("1.0", "end")
        except:
            self._flag.clear()
            mb.showinfo('提示', '输入文件格式有误')
            return
        try:
            pic_list = []
            _list = content.split('\n')
            for cont in _list:
                if cont != '':
                    pic_list.append(cont)
            hwnd = get_app_info()

            if len(pic_list) == 0:
                self._flag.clear()
                mb.showinfo("提示", "输入文件格式错误")
                return

            # 读取脚本文件缓存
            with open("script_cache/script_cache.txt", 'w+', encoding='utf-8') as file:
                file_cont = file.read()
                if file_cont != content:
                    file.write(content)

            while self._flag.is_set():
                click_temp('reg_images/' + pic_list[0], hwnd[0], hwnd[1], hwnd[2], hwnd[3])
                for img in pic_list:
                    if self._flag.is_set():
                        img = 'reg_images/' + img
                        click_temp(img, hwnd[0], hwnd[1], hwnd[2], hwnd[3])
                    else:
                        break
        except:
            self._flag.clear()
            print(traceback.format_exc())
            mb.showinfo('提示', traceback.format_exc())

    def script_status(self):
        if self._flag.is_set():
            self._flag.clear()
        else:
            self._flag.set()
        self.start_script()


if __name__ == '__main__':
    app = App()
