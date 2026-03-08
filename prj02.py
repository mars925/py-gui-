#######################匯入模組#######################
# 匯入 tkinter 模組
from tkinter import *


#######################定義函數########################
def hi_fun():
    print("Hi,singular")
    display.config(text="Hi Singular", fg="red", bg="black")


def clear_fun():
    display.config(text="", fg="black", bg="white")


#######################建立視窗########################
# 建立視窗物件
windows = Tk()
# 設定視窗標題
windows.title("My First GUI")
btn1 = Button(windows, text="show screen", command=hi_fun)
btn1.pack()
btn2 = Button(windows, text="clear screen", command=clear_fun)
btn2.pack()
display = Label(windows, text="")
display.pack()
#######################運行應用程式########################
# 運行應用程式
windows.mainloop()
