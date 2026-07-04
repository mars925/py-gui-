#######################模組#######################
# asyncio 是 Python 內建的非同步工具。
# 可以把它想成「任務小管家」：如果某件事需要等網路回應，
# 它可以先去安排別的事，不會讓整個程式傻傻卡住。
import asyncio
import discord  # pip install -U discord.py；這個套件負責和 Discord 溝通
import os  # 用來讀取環境變數 pip install -U python-dotenv；把 .env 裡的設定讀進程式
import requests  # 用來向天氣網站送出請求，並接住回傳的資料
from mars.mars import (
    WeatherAPI,
)  # 從我們自己寫的 mars.py 裡匯入 WeatherAPI 類別，讓我們可以用它來查天氣
from dotenv import load_dotenv  #
from mars.mars import WeatherAPI, AIAssistant

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
intents.message_content = (
    True  # 允許機器人看到訊息真正的文字內容，這樣它才知道有人是不是輸入了 hello
)

bot = discord.Client(intents=intents)  # 建立機器人本體，並把 intents 交給它
tree = discord.app_commands.CommandTree(
    bot
)  # 建立 slash 指令管理器，專門管理像 /hello 這種指令

weather_api = WeatherAPI(
    os.getenv("OPENWEATHER_API_KEY")
)  # 建立一個 WeatherAPI 的實例，準備好查天氣用的設定；把 .env 裡的 OPENWEATHER_API_KEY 讀進來當作 API 金鑰
ai_assistant = AIAssistant(os.getenv("OPENAI_API_KEY"))
# 限制歷史紀錄的長度，避免訊息過多導致回應變慢或失敗
CHANNEL_HISTORY_LIMIT = 15
# system_prompt 像是給 AI 的角色卡，會影響 AI 回覆的語氣和工作方式。
CHAT_SYSTEM_PROMPT = """
你是一個在 Discord 群組頻道中協助大家的(gay) 助手。
請根據頻道歷史判斷大家正在討論什麼，再回答最新提到你的問題。
回覆請使用繁體中文，語氣兇一點、每句一髒話。
如果頻道歷史不足以判斷答案，請說明你還需要哪一個資訊。
如果需要提到特定使用者或其他 bot，請複製歷史訊息裡的 mention：<@使用者ID>。
使用 mention 時，請直接放在一般文字中，不要寫成 @名字，也不要加反斜線、反引號或程式碼區塊。
不要使用 @everyone、@here 或角色標記，也不要自己編造 mention ID。
"""
AI_REPLY_ALLOWED_MENTIONS = discord.AllowedMentions(
    users=True, roles=False, everyone=False, replied_user=True
)  # 只允許提到使用者，不允許提到角色或全體


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


def build_forecast_embed(forecast_summary):
    embeds = []

    for forecast in forecast_summary:
        embed = discord.Embed(
            title=f"{forecast['city_name']} 的天氣預報 - {forecast['datetime']}",
            description=f"敘述：{forecast['description']}",
            color=discord.Color.from_str("#1B14E2"),  # Dodger Blue 的顏色代碼
        )

        icon_url = weather_api.get_icon_url(forecast["icon_code"])
        embed.set_thumbnail(url=icon_url)  # 把天氣圖示放在 embed 的縮圖位置
        embed.add_field(
            name="溫度",
            value=f"{forecast['temperature_celsius']} °C",
            inline=False,  # 這裡設定為 False，讓這個欄位獨占一行
        )
        embeds.append(embed)

    return embeds


async def get_channel_history(channel, bot_user, limit=15, before=None):
    """取得頻道歷史訊息，過濾掉機器人自己的訊息，並限制在最近的幾則。"""
    old_messages = []
    history_messages = []
    # Discord 的訊息歷史是從新到舊的順序，所以我們要先把它們倒過來，才能從最舊的開始看。
    async for old_message in channel.history(
        limit=limit, before=before, oldest_first=False
    ):
        old_messages.append(old_message)
    for old_message in reversed(old_messages):
        # 只保留不是機器人自己發的訊息，這樣 AI 才能看到使用者說了什麼，而不是一直看到自己的回覆。
        # 這裡的 old_message.author 是訊息的發送者，如果它和 bot_user（機器人自己）一樣，就跳過這則訊息。
        # 這樣做的好處是，AI 在分析頻道歷史時，不會被自己的回覆干擾，能更專注在使用者的對話內容上。
        # 同時，我們也限制了歷史訊息的數量，避免一次拿太多訊息導致分析變慢或失敗。
        content = old_message.content.strip()
        if not content:
            continue  # 如果訊息內容是空的，就跳過這則訊息
        if old_message.author.id == bot_user.id:
            history_messages.append({"role": "assistant", "content": content})
        else:
            speaker_type = "機器人" if old_message.author.bot else "使用者"
            speaker_mention = old_message.author.mention
            user_content = (
                f"{old_message.author.display_name}"
                f"({speaker_type},{speaker_mention})說：{content}"
            )
            history_messages.append({"role": "user", "content": user_content})
    return history_messages


async def ask_with_discord_history(message):
    history_messages = await get_channel_history(
        channel=message.channel,
        bot_user=bot.user,
        limit=CHANNEL_HISTORY_LIMIT,
        before=message,
    )
    user_question = message.content.replace(f"<@{bot.user.id}>", "").strip()
    if not user_question:
        user_question = "根據前面對會,回應大家？"
    user_message = (
        f"{message.author.display_name}"
        f"(mention:{message.author.mention})說：{user_question}"
    )
    return ai_assistant.ask(
        system_prompt=CHAT_SYSTEM_PROMPT,
        user_message=user_message,
        history_messages=history_messages,
        temperature=0.5,
    )


#######################事件#######################
# @bot.event 這種寫法叫裝飾器，可以把它想成幫下面的函式貼上一張「事件處理員」標籤。
# def 是一般函式，通常會照順序一路做完。
# async def 是可以搭配 await 的函式；遇到需要等一下的工作時，
# 它可以先暫停，等事情完成後再回來繼續做。
@bot.event
async def on_ready():
    print(
        f"{bot.user} is ready and online!"
    )  # 當機器人登入成功並準備好時，印出提示訊息
    # await 的意思比較像「這件事要花時間，先等它完成再往下」。
    # 它和 return 不一樣：await 等完之後還會繼續跑下面的程式；return 則是直接結束函式。
    # 這裡的 tree.sync() 會把我們寫好的 slash 指令送去 Discord 登記。
    await tree.sync()


@bot.event
async def on_message(message):
    # message 就是剛剛出現在頻道裡的一則訊息。
    if (
        message.author == bot.user
    ):  # 如果這句話是機器人自己說的，就不要回應自己，才不會一直自言自語
        return  # return 是「直接結束這個函式」；它不像 await 只是等一下，而是真的先離開這次工作
    if message.content == "hello":  # 如果訊息內容為 hello
        # send() 需要經過網路把訊息送回 Discord，所以要用 await 等它送完。
        await message.channel.send("Hey!")  # 回應 Hey!
    elif bot.user in message.mentions:  # 如果訊息裡有提到機器人
        async with message.channel.typing():  # 顯示「機器人正在輸入中...」的狀態，讓使用者知道它正在處理
            answer, error = await ask_with_discord_history(message)
        if error:
            await message.channel.send(error)
        else:
            await message.reply(
                answer,
                mention_author=True,
                allowed_mentions=AI_REPLY_ALLOWED_MENTIONS,
            )  # 回覆使用者，並允許提到使用者，但不允許提到角色或全體


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
async def weather(
    interaction: discord.Interaction,
    city: str,
    forecast: bool = False,
    ai: bool = False,
):
    """輸入 /weather [城市名稱]，機器人會回傳該城市的天氣資訊。"""
    await interaction.response.defer()  # 先回應「正在處理中...」，讓使用者知道指令有被收到，正在查資料
    city_name = city.strip()  # 去掉使用者輸入的城市名稱前後的空白

    if not weather_api.api_key:
        await interaction.followup.send("天氣 API 金鑰未設定，無法查詢天氣資訊。")
        return
    try:
        if not forecast:
            weather_summary = weather_api.get_weather_summary(city)
            if weather_summary is None:
                await interaction.followup.send(
                    f"無法獲取 {city_name} 的天氣資訊，請確認城市名稱是否正確。"
                )
                return
        if not ai:
            forecast_summary = weather_api.get_forecast_summary(city)
            if forecast_summary is None:
                await interaction.followup.send(
                    f"無法獲取 {city_name} 的天氣預報資訊，請確認城市名稱是否正確。"
                )
                return

            embeds = build_forecast_embed(forecast_summary)
            await interaction.followup.send(embeds=embeds)  # 把 embed 回傳給使用者
            return
        row_forecast = weather_api.get_forecast(city)

    except (requests.RequestException, ValueError) as e:
        await interaction.followup.send(f"查詢天氣資訊時發生錯誤：{e}")
        return

    analysis, error = ai_assistant.ask(
        system_prompt="你是一個專業的氣象分析師，請根據以下的天氣預報資料，幫我分析未來幾天的天氣趨勢，並給出簡短的總結和建議。",
        user_message=f"以下是未來幾天的天氣預報資料\n{row_forecast}",
    )
    if error:
        await interaction.followup.send(f"與 ChatGPT 互動時發生錯誤：{error}")
    else:
        await interaction.followup.send(f"**{city}**\n{analysis}")


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
