#######################匯入模組#######################
# 匯入 tkinter 模組（用於建立圖形介面）
from tkinter import *  # 匯入 tkinter 所有名稱，方便使用按鈕、標籤等元件


#######################定義函數########################
def hi_fun():  # 定義按下顯示按鈕時呼叫的函式
    print("Hi,singular")  # 在終端機輸出文字
    global change
    if change == False:
        display.config(text="red", fg="black", bg="red")  # 更新標籤的文字和顏色
        change = True  # 將 change 設為 True，表示已經顯
    else:  # 如果 change 為 True，則清除顯示並改變顏色
        display.config(text="green", fg="black", bg="green")
        change = False  # 將 change 設為 False，表示已經清除顯示


change = True
#######################建立視窗########################
# 建立視窗物件
windows = Tk()  # 建立主視窗物件
# 設定視窗標題
windows.title("My First GUI")  # 設定主視窗標題
btn1 = Button(
    windows, text="show screen", command=hi_fun
)  # 建立按鈕，點擊時呼叫 hi_fun
btn1.pack()  # 將按鈕加入佈局
display = Label(windows, text="")  # 建立用於顯示訊息的標籤
display.pack()  # 將標籤加入佈局
#######################運行應用程式########################
# 運行應用程式
windows.mainloop()  # 進入主迴圈，保持視窗運作
