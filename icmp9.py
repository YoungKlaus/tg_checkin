import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# 从环境变量获取配置（为了安全，不要直接写在代码里）
api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session_string = os.environ["TELEGRAM_SESSION"]
bot_username = os.environ["BOT_USERNAME"]

async def main():
    print(f"DEBUG: 从环境变量读取到的 Bot 用户名是: {repr(bot_username)}")
    # 使用 StringSession 初始化，无需再次登录
    async with TelegramClient(StringSession(session_string), api_id, api_hash) as client:
        print(f"正在连接 Telegram...")
        
        # 获取与 Bot 的对话历史中的最新一条消息
        # limit=1 表示只取最后一条
        messages = await client.get_messages(bot_username, limit=1)
        
        if not messages:
            print("未找到与该 Bot 的对话记录。")
            return

        latest_msg = messages[0]
        print(f"找到最新消息: {latest_msg.text[:50]}...") # 打印前50个字符预览

        # 检查消息是否有按钮
        if latest_msg.buttons:
            print("检测到按钮，正在尝试点击第一个按钮...")
            try:
                # 点击第一行第一列的按钮 (0, 0)
                await latest_msg.click(0)
                
                # 等待几秒钟，因为 Bot 修改消息文本需要时间
                print("点击完成，等待 Bot 更新结果...")
                await asyncio.sleep(5) 
                
                # 重新获取这条消息以查看更新后的文本
                # 使用 get_messages 获取最新的状态
                updated_msgs = await client.get_messages(bot_username, ids=[latest_msg.id])
                if updated_msgs:
                    print("-" * 30)
                    print("⬇️ 签到结果 ⬇️")
                    print(updated_msgs[0].text)
                    print("-" * 30)
                
            except Exception as e:
                print(f"点击失败: {e}")
        else:
            print("最新消息中没有检测到按钮，无法签到。")

if __name__ == '__main__':
    asyncio.run(main())
