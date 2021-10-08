import requests
import random
import string
from tkinter import *
from tkinter.filedialog import askdirectory
import threading


def download_image(text):
    url_list = text.split('//')
    for url in url_list:
        image_name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        resp = requests.get(url)
        if resp.status_code == 200:
            with open(image_name, 'wb') as f:
                f.write(resp.content)
    return True


def thread_it(func, *args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()


class App:
    def __init__(self):
        root = Tk()
        root.title("Image Tool")
        Label(root, text='路径：').grid(row=0, column=0)
        self.path = StringVar()
        Entry(root, textvariable=self.path).grid(row=0, column=1)
        Button(root, text='选择路径', command=self.select_path).grid(row=0, column=2)
        self.cnt_text = Text(root, height=6, width=30).grid(row=1, columnspan=3)
        Label(root, text='结果显示：').grid(row=2)
        Text(root, height=6, width=30).grid(row=3, columnspan=3)

        Button(root, text='开始下载', command=thread_it(self.start_download())).grid(row=4, column=1)
        root.mainloop()

    def select_path(self):
        """
        选择程序路径
        :return:
        """
        _path = askdirectory()
        self.path.set(_path)

    def start_download(self):
        content = self.cnt_text.get('1.0', 'end')
        if not content:
            return False
        result = download_image(content)


if __name__ == '__main__':
    app = App()
