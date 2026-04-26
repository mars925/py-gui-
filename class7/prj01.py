#######################匯入模組#######################
from ttkbootstrap import *  # pip install ttkbootstrap -U(在終端機
import sys
import os

#######################設定工作目錄########################
os.chdir(
    sys.path[0]
)  # 將當前工作目錄更改為腳本所在的目錄，這樣可以確保在運行腳本時能夠正確找到相關文件


#######################定義函數########################
def on_change():
    check_label.config(  # pyright: ignore[reportUndefinedVariable]
        text=str(check_type.get())
    )  # 當Checkbutton的值改變時，更新check_label的文本為check_type的當前值


#######################建立視窗########################
window = Tk()  # 建立視窗
window.title("Checkbutton")  # 設定視窗標題
########################設定字型########################
font_size = 20  # 設定字型大小
window.option_add(
    "*Font", ("Helvetica", font_size)
)  # 設定視窗的字型，*Font是tkinter中的一個選項，用於設定所有元件的字型
# 設定預設字型為Helvetica，大小為font_size
####
#####################設定主題########################
style = Style(theme="superhero")  # 設定主題為superhero
style.configure(
    "my.TButton", font=("Helvetica", font_size)
)  # 設定my.TButton的字型為Helvetica，大小為font_size
style.configure(
    "my.TCheckbutton", font=("Helvetica", font_size)
)  # 設定my.TCheckbutton的字型為Helvetica，大小為font_size
check_type = BooleanVar()  # 建立一個StringVar物件，用於存儲Checkbutton的值
check_type.set(True)  # 將check_type的值設置為True，表示Checkbutton默認為選中狀態
check_label(window, text="ture")  # pyright: ignore[reportUndefinedVariable]
check_label.grid(  # pyright: ignore[reportUndefinedVariable]
    row=1, column=2, padx=10, pady=10
)  # pyright: ignore[reportUndefinedVariable] # 將check_label放置在視窗中
#####################建立checkbutton########################
check = Checkbutton(
    window, variable=check_type, onvalue=True, offvalue=False, style="my.TCheckbutton"
)  # 建立一個Checkbutton，並將其變量設置為check_type，當選中時值為True，未選中時值為False，使用my.TCheckbutton的樣式
check.grid(row=1, column=1, padx=10, pady=10)  # 將check放置在視窗中
window.mainloop()  # 啟動視窗的主事件循環，讓視窗保持顯示狀態，等待用戶操作
