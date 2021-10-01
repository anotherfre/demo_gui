from tkinter import *
import datetime


def time_change():
    now_time.set(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    app.after(1000, time_change)


app = Tk()
now_time = StringVar()
_label = Label(app, textvariable=now_time)
now_time.set(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
_label.pack()
app.after(1000, time_change)
app.mainloop()
