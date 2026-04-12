#######################匯入模組#######################
# 匯入 tkinter 模組（用於建立圖形介面）
from tkinter import *  # 匯入 tkinter 所有名稱，方便使用按鈕、標籤等元件
import sys
import os
from PIL import Image, ImageTk

#######################設定工作目錄#######################
os.chdir(sys.path[0])  # 將工作目錄切換到當前腳本所在的目錄


#######################定義函數########################
def move_circle(event):
    key = event.keysym  # 获取按键的名称
    if key == "Up":  # 如果按键是 "Up"
        canvas.move(circle, 0, -10)  # 将圆向上移动 10 像素
    elif key == "Down":  # 如果按键是 "Down"
        canvas.move(circle, 0, 10)  # 将圆向下移动 10 像素
    elif key == "Left":  # 如果按键是 "Left"
        canvas.move(circle, -10, 0)  # 将圆向左移动 10 像素
    elif key == "Right":  # 如果按键是 "Right"
        canvas.move(circle, 10, 0)  # 将圆向右移动 10 像素


#######################建立視窗########################
# 建立視窗物件
windows = Tk()  # 建立主視窗物件
#######################設定視窗圖片########################
windows.iconbitmap("")  # 設定視窗的圖示為 "icon.ico" 文件

#######################創建畫布########################
canvas = Canvas(windows, width=600, height=600, bg="white")
canvas.pack()  # 將 Canvas 元件加入視窗並顯示

#######################載入圖片########################
image = Image.open("bdbfa0e91db7423d2e91950976ef9992.png")  # 使用 PIL 库打开图片文件
image = image.resize((600, 600))  # 调整图片大小为 600x600 像素
img = ImageTk.PhotoImage(image)  # 将 PIL 图像对象转换为 Tkinter 可用的图像对象
#######################顯示圖片########################
my_img = canvas.create_image(
    300, 300, image=img
)  # 在 Canvas 上顯示圖片，位置為 (300, 300)
circle = canvas.create_oval(
    250, 150, 300, 200, fill="red"
)  # 在 Canvas 上绘制一个红色的圆，位置为 (250, 150) 到 (300, 200)，线宽为 5
rect = canvas.create_rectangle(
    350, 150, 400, 200, fill="blue"
)  # 在 Canvas 上绘制一个蓝色的矩形，位置为 (350, 150) 到 (400, 200)，线宽为 5
msg = canvas.create_text(
    300, 250, text="Hello, World!", font=("Arial", 20), fill="green"
)  # 在 Canvas 上显示文本 "lamb"，位置为 (300, 250)，字体为 Arial，大小为 20，颜色为绿色
img_logo = Image.open("logo.png")  # 使用 PIL 库打开 logo.png 图片文件
img_logo = img_logo.resize((100, 100))  # 调整 logo 图片大小
img_logo_tk = ImageTk.PhotoImage(
    img_logo
)  # 将 PIL 图像对象转换为 Tkinter 可用的图像对象
logo = canvas.create_image(
    50, 50, image=img_logo_tk
)  # 在 Canvas 上显示 logo 图片，位置为 (50, 50)
#######################綁定按鍵事件########################
canvas.bind_all("<Key>", move_circle)  # 綁定所有按鍵事件到 move_circle 函數
#######################運行應用程式########################
# 運行應用程式
windows.mainloop()  # 進入主迴圈，保持視窗運作
