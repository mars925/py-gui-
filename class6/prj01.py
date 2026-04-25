#######################匯入模組#######################
import requests
import os
import sys

os.chdir(sys.path[0])
#######################定義常數########################
API_KEY = "0c06092fb6be7fd6bbe6ea457e7427fb"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNTTS = "metric"
LANG = "zh_tw"
ICON_URL = "http://openweathermap.org/img/wn/"
#######################主程式########################
city_name = input("請輸入城市名稱:")
send_url = (
    BASE_URL
    + "appid="
    + API_KEY
    + "&q="
    + city_name
    + "&units="
    + UNTTS
    + "&lang="
    + LANG
)
print(send_url)
response = requests.get(send_url)
info = response.json()
if "weather" in info and "main" in info:
    current_temperature = info["main"]["temp"]
    weather_description = info["weather"][0]["description"]
    print(f"{city_name}的天氣狀況: {weather_description}")
    print(f"{city_name}的溫度: {current_temperature}°C")
    ICON_URL = ICON_URL + info["weather"][0]["icon"] + "@2x.png"
    print(f"天氣圖示URL: {ICON_URL}")
    if ICON_response.status_code == 200:
        with open("weather_icon.png", "wb") as f:
            f.write(ICON_response.content)
        print("天氣圖示已成功下載並保存為 weather_icon.png")
        with open("weather_info.txt", "w", encoding="utf-8") as f:
            f.write(f"{city_name}的天氣狀況: {weather_description}\n")
            f.write(f"{city_name}的溫度: {current_temperature}°C\n")
        print("天氣資訊已成功保存為 weather_info.txt")
    else:
        print("無法下載天氣圖示，請確認URL是否正確。")
else:
    print("無法獲取天氣資訊，請確認城市名稱是否正確。")
