#######################匯入模組#######################
import requests

#######################定義常數########################
API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNTTS = "metric"
LANG = "zh_tw"
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
data = response.json()
#######################定義函數########################

#######################建立視窗########################

#######################運行應用程式########################
