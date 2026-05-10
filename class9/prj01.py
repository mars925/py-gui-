def run_announce9(func):
    print("開始執行函式...")
    func()
    print("函式執行完畢！")


def say_hello():
    print("Hello, World!")


print("直接呼叫")
say_hello()


# return wrapper
def gift_wrap(func):
    def wrapper():
        print("開始執行函式...")
        func()
        print("函式執行完畢！")

    return wrapper


def say_hello():
    print("Hello, World!")


def run_with_announce(func):
    print("準備執行...")
    func()
    print("函式執行完畢！")


print("直接呼叫:")
say_hello()
print()
print("透過 run_with_announce 呼叫:")
run_with_announce(say_hello)


def gift_wrap(func):
    def wrapper():
        print("---...")
        func()
        print("函式執行完畢！")

    return wrapper


say_hello = gift_wrap(say_hello)  # 手動包裝函式
say_hello()  # 執行包裝後的函式S


# ==================================================
# 使用裝飾詞來紀錄函式的呼叫次數
# ===================================================
# python提供了更簡潔的寫法:在寒士定義上方接@
@gift_wrap  # 等於:say_hello = gift_wrap(say_hello)
def say_hello():
    print("Hello, World!")


say_hello()  # 自動執行

print()
print(">>>連結Discord Bot<<<")
print(">>>@bot.event<<<")
print(">>>@bot.event，Discord Bot的事件裝飾詞<<<")

print("===============================")


# ===============================
# 第四段:帶參數的裝飾詞
# ===============================
def register_commad(name,description):
    print(f"[登記]指令/{name}:{description}")

    def decorator(func):
        def wrapper():
            print(f"[執行指令]/{name}...")
            func()

        return wrapper
    return decorator
@register_commad(name="hello",description=description="打招呼")
def hello_command():
    print( "你好!我是hello指令!")

hello_command()
print("===============================")