#######################模組#######################
# asyncio 是 Python 內建的非同步工具。
# 可以把它想成「任務小管家」：如果某件事需要等網路回應，
# 它可以先去安排別的事，不會讓整個程式傻傻卡住。
import asyncio
import discord  # pip install -U discord.py；這個套件負責和 Discord 溝通
import os  # 用來讀取環境變數 pip install -U python-dotenv；把 .env 裡的設定讀進程式
import requests  # 用來向天氣網站送出請求，並接住回傳的資料
from mars.mars import WeatherAPI  # 從我們自己寫的 mars.py 裡匯入 WeatherAPI 類別，讓我們可以用它來查天氣
from dotenv import load_dotenv  #
#######################初始化#######################
load_dotenv()  # 讀取 .env 檔，讓程式可以拿到 DC_BOT_TOKEN 這類設定資料

# event loop 可以想成「非同步任務的轉盤」：
# 哪個工作先做、哪個工作要等一下，會由這個轉盤幫忙安排。
# Python 3.10+ 在主程式裡不一定會先自動準備好這個轉盤，
# 所以我們自己先建立一個給 Discord 使用。
asyncio.set_event_loop(asyncio.new_event_loop())

# Intent 可以想成「先跟 Discord 勾選：我想收到哪些類型的通知」。
# 如果沒有先打開某個 Intent，Discord 就不會把那種資料送給機器人。
intents = discord.Intents.default()
intents.message_content = True  # 允許機器人看到訊息真正的文字內容，這樣它才知道有人是不是輸入了 hello

bot = discord.Client(intents=intents)  # 建立機器人本體，並把 intents 交給它
tree = discord.app_commands.CommandTree(bot)  # 建立 slash 指令管理器，專門管理像 /hello 這種指令

weather_api=WeatherAPI(os.getenv("OPENWEATHER_API_KEY"))  # 建立一個 WeatherAPI 的實例，準備好查天氣用的設定；把 .env 裡的 OPENWEATHER_API_KEY 讀進來當作 API 金鑰
def build_embed(weather_summary):
    """把從 WeatherAPI 拿到的天氣資訊整理成 Discord 的 embed 格式。"""
    embed = discord.Embed(
        title=f"{weather_summary['city_name']} 的天氣",
        description=weather_summary["description"],
        color=0x1E90FF,  # Dodger Blue 的顏色代碼
    )
    icon_url = weather_api.get_icon_url(weather_summary["icon_code"])
    embed.set_thumbnail(url=icon_url)  # 把天氣圖示放在 embed 的縮圖位置

    embed.add_field(
        name="溫度",
        value=f"{weather_summary['temperature_celsius']} °C",
        inline=False,  # 這裡設定為 False，讓這個欄位獨占一行

    )
    return embed





#######################事件#######################
# @bot.event 這種寫法叫裝飾器，可以把它想成幫下面的函式貼上一張「事件處理員」標籤。
# def 是一般函式，通常會照順序一路做完。
# async def 是可以搭配 await 的函式；遇到需要等一下的工作時，
# 它可以先暫停，等事情完成後再回來繼續做。
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")  # 當機器人登入成功並準備好時，印出提示訊息
    # await 的意思比較像「這件事要花時間，先等它完成再往下」。
    # 它和 return 不一樣：await 等完之後還會繼續跑下面的程式；return 則是直接結束函式。
    # 這裡的 tree.sync() 會把我們寫好的 slash 指令送去 Discord 登記。
    await tree.sync()


@bot.event
async def on_message(message):
    # message 就是剛剛出現在頻道裡的一則訊息。
    if message.author == bot.user:  # 如果這句話是機器人自己說的，就不要回應自己，才不會一直自言自語
        return  # return 是「直接結束這個函式」；它不像 await 只是等一下，而是真的先離開這次工作
    if message.content == "hello":  # 如果訊息內容為 hello
        # send() 需要經過網路把訊息送回 Discord，所以要用 await 等它送完。
        await message.channel.send("Hey!")  # 回應 Hey!


#######################指令#######################
# @tree.command(...) 也是裝飾器，作用是幫下面的函式貼上「這是一個 slash 指令」的標籤。
# 使用者在 Discord 輸入 /hello 時，就會呼叫下面這個函式。
# slash 指令通常要和 Discord 來回溝通，所以這裡用 async def 來寫。
@tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    """輸入 /hello，機器人會回傳 Hey!"""
    # interaction 可以想成「這次有人使用指令時送來的資料包」，
    # 裡面會記錄是誰按的、在哪個地方按的，以及這次指令的相關資訊。
    # send_message() 也是網路工作，所以前面要加 await。
    await interaction.response.send_message("Hey!")  # 把 Hey! 回傳給使用者
@tree.command(name="weather", description="取得當前天氣資訊")
async def weather(interaction: discord.Interaction, city: str):
    """輸入 /weather [城市名稱]，機器人會回傳該城市的天氣資訊。"""
    await interaction.response.defer()  # 先回應「正在處理中...」，讓使用者知道指令有被收到，正在查資料 
    city_name = city.strip()  # 去掉使用者輸入的城市名稱前後的空白

    if not weather_api.api_key:
        await interaction.followup.send("天氣 API 金鑰未設定，無法查詢天氣資訊。")
        return
    try:
        weather_summary = weather_api.get_weather_summary(city)
    except(requests.RequestException, ValueError):
        await interaction.followup.send(f"查詢天氣資訊時發生錯誤：{e}")
        return
    if weather_summary is None:
        await interaction.followup.send(f"無法獲取 {city_name} 的天氣資訊，請確認城市名稱是否正確。")
        return
    embed = build_embed(weather_summary)  # 把天氣資訊整理成 Discord embed 格式
    await interaction.followup.send(embed=embed)  # 把 embed 回傳給使用
#######################啟動#######################
# def main() 把「啟動機器人」這件事單獨包成一個步驟。
# 這樣主程式看起來更整齊，以後如果啟動前還要加其他設定，也知道要放在哪裡。
# 這裡用普通的 def 就夠了，因為 main() 只是負責開始執行程式，
# 不需要在裡面 await 其他非同步工作。
def main():
    # os.getenv("DC_BOT_TOKEN") 會去 .env 裡找機器人的 token。
    # bot.run(...) 會讓機器人登入 Discord，然後開始待命。
    bot.run(os.getenv("DC_BOT_TOKEN"))


# 這個 if 可以想成一道入口檢查：
# 只有當這份檔案是「被直接執行」時，才會呼叫 main() 啟動機器人。
# 如果這份檔案只是被別的程式 import 進去，下面的 main() 就不會自動執行。
if __name__ == "__main__":
    main()  # 從這裡正式啟動整個程式