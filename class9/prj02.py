#######################模組#######################
# 1. asyncio是python內建的非同步工具
# 可以把它想成任務小管家
import asyncio
import discord
import os
from dotenv import load_dotenv

#######################初始化#######################
load_dotenv()
asyncio.set_event_loop(asyncio.new_event_loop())
intents = discord.Intents.default()
intents.message_content = True

#######################事件#######################

#######################指令#######################

#######################啟動#######################
