#######################匯入模組#######################
import sys
import os
from ttkbootstrap import *

#######################設定工作目錄########################


#######################定義函數########################
def show_result():
    entry_text = entry.get()  # 获取 Entry 中的文本
    try:
        result = eval(entry_text)  # 计算表达式的结果
    except:
        result = "無效的表達式"  # 如果计算失败，显示错误信息
    label.config(text=result)


#######################建立視窗########################

Window = Tk()
Window.title("My GUI")
#######################建立標籤########################
label = Label(Window, text="計算結果")
label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
#######################建立按鈕########################
button = Button(Window, text="顯示計算結果", command=show_result, style="my.TButton")
button.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
#######################建立Entry########################
entry = Entry(Window, width=30)
entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
#######################設定字型########################
font_size = 20
Window.option_add("*Font", ("Malgun Gothic", font_size))
#######################設定主題########################
style = Style(theme="minty")
style.configure("my.TButton", font=("Helvetica", font_size))

#######################運行應用程式########################
Window.mainloop()
