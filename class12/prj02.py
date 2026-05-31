import requests

API_KEY = "0c06092fb6be7fd6bbe6ea457e7427fb"  
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
UNITS="metric"  
LANG="zh_tw"

city_name="Taipei"
send_url=(f"{BASE_URL}?q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANG}")

print(f"發送的 URL：{send_url}")

response = requests.get(send_url)
response.raise_for_status()  # 如果回傳的狀態碼不是 200，這行會丟出例外，程式就會停止在這裡，不會繼續往下執行。
info=response.json()  # json() 會把網站回傳的 JSON 資料轉成 Python 字典

if "city" in info:
    for forecast in info["list"]:
        dt_txt = forecast["dt_txt"]
        temp = forecast["main"]["temp"]
        weather_desc = forecast["weather"][0]["description"]
        print(dt_txt, temp, weather_desc)
else:    print("無法獲取天氣資訊，請確認城市名稱是否正確。")