#######################匯入模組#######################
from ttkbootstrap import *  # pip install ttkbootstrap -U(在終端機
import sys
import os
from PIL import Image, ImageTk  # pip install Pillow

#######################設定工作目錄########################
os.chdir(sys.path[0])
#######################建立視窗########################
window = Tk()  # 建立視窗
window.title("Label Image")  # 設定視窗標題
########################讀取圖片########################
image = Image.open("weather.jpg")  # 使用PIL庫的Image模組打開圖片文件
weather_phote = ImageTk.PhotoImage(image)  # 將PIL圖像對象轉換為Tkinter可用的圖像對象
########################建立標籤########################
weather_label = Label(
    window, image=weather_phote
)  # 建立一個Label，並將其圖像設置為weather_photo
weather_label.pack(padx=20, pady=20)  # 將weather_label放置在視窗中
weather_label.image = (
    weather_phote  # 將weather_photo保存為weather_label的屬性，以防止被垃圾回收
)
window.mainloop()  # 啟動視窗的主事件循環，讓視窗保持顯示狀態，等待用戶操作
