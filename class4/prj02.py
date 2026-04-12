#######################匯入模組#######################
from ttkbootstrap import *
import sys
import os


#######################定義函數########################
def text():
    print("text")


#######################建立視窗########################
Window = Tk()
Window.title("My GUI")
#######################設定字型########################
font_size = 20
Window.option_add("*Font", ("Malgun Gothic", font_size))
#######################設定主題########################
Style = Style(theme="cyborg")
Style.configure("my.TButton", font=("Malgun Gothic", font_size))
#######################建立標籤########################
Label = Label(Window, text="Hello, World!")
Label.grid(row=0, column=0, sticky="w")
#######################建立按鈕########################
button = Button(Window, text="瀏覽", command="my.TButton")
button.grid(row=0, column=1, sticky="e")
button2 = Button(Window, text="顯示", command=text, style="my.TButton")
button2.grid(row=1, column=0, columnspan=2, sticky="ew")


#######################運行應用程式########################
Window.mainloop()
