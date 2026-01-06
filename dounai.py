import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# 从环境变量获取配置
api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session_string = os.environ["TELEGRAM_SESSION"]

# 目标 Bot 用户名 (不带 @)
bot_username = 'doubledoubot' 
# 发送的签到指令
command = '/checkin'

async def main():
    async with TelegramClient(StringSession(session_string), api_id, api_hash) as client:
        print(f"正在连接 Telegram...")
        
        # 1. 发送签到指令
        print(f"正在向 @{bot_username} 发送指令: {command}")
        await client.send_message(bot_username, command)
        
        # 2. 等待 Bot 回复
        print("指令已发送，等待 Bot 回复...")
        
        try:
            # 捕获新消息：来自该 Bot，且不是我自己发出的
            # timeout=10 表示最多等10秒，等不到就放弃
            async with client.conversation(bot_username, timeout=15) as conv:
                # 注意：conversation 依赖于这一瞬间的交互，如果 Bot 反应慢或者有其他人同时发消息，
                # 简单的 get_response 可能会抓错。但对于个人 Userbot 这种场景通常足够。
                
                # 这里我们不用 conversation.send_message，因为上面已经发了。
                # 我们直接监听最新的回复。
                
                # 更稳健的方法是直接读取最新一条消息，直到它是 Bot 发的且时间是最近的
                # 但为了简单，我们循环检查最新消息
                
                for _ in range(15): # 尝试检查 15 次
                    await asyncio.sleep(1) # 每秒检查一次
                    messages = await client.get_messages(bot_username, limit=1)
                    if messages:
                        latest_msg = messages[0]
                        # 简单的判断：如果最新消息是 Bot 发的，且不是我们刚才发的指令（通常 Bot 回复会覆盖指令显示，或者在指令之后）
                        # 这里的逻辑是：只要最新一条消息不是我发的，就是回复
                        if not latest_msg.out: 
                            print("-" * 30)
                            print("⬇️ 签到结果 ⬇️")
                            print(latest_msg.text)
                            print("-" * 30)
                            return
                print("等待超时，未收到 Bot 回复。")

        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == '__main__':
    asyncio.run(main())
