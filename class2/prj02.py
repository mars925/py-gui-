#######################匯入模組#######################
# 匯入 tkinter 模組（用於建立圖形介面）
from tkinter import *  # 匯入 tkinter 所有名稱，方便使用按鈕、標籤等元件
import random  # 匯入 random 模組，用於生成隨機數字


#######################定義函數########################
def hi_fun():  # 定義按下顯示按鈕時呼叫的函式
    # 顯示"Hi,singular"並隨機選擇一種顏色
    fg_colors = "#" + "".join(
        [random.sample("0123456789ABCDEF") for j in range(6)]
    )  # 隨機生成前景色的十六進位顏色碼
    bg_colors += random.choice("0123456789ABCDEF")  # 隨機生成背景色的十六進位顏色碼
    display.config(
        text="Hi Singular", fg=fg_colors, bg=bg_colors
    )  # 更新標籤的文字和顏色


#######################建立視窗########################
# 建立視窗物件
windows = Tk()  # 建立主視窗物件

#######################運行應用程式########################
# 運行應用程式
windows.mainloop()  # 進入主迴圈，保持視窗運作
