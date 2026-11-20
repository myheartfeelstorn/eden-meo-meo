import os
import colorama
import sys
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import wavelink  # <--- Thêm thư viện wavelink

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

load_dotenv(os.path.join(BASE_DIR, "setting", ".env"))
TOKEN = os.getenv("BOT_TOKEN")
PREFIX = os.getenv("PREFIX", ".")

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.voice_states = True

        super().__init__(command_prefix=PREFIX, intents=intents)
        self.remove_command("help")
async def setup_hook(self):
    try:
        node = wavelink.Node(
            uri="http://67.220.85.63:6223",  # Lấy từ phần server port & address
            password="homiesmusic"             # Lấy từ phần password trong yml
        )
        await wavelink.Pool.init(nodes=[node])
        print("🔗 Đã kết nối thành công tới Lavalink Node từ xa!")
    except Exception as e:
        print(f"❌ Không thể kết nối tới Lavalink: {e}")
    
        # 2. Tự động nạp cogs từ thư mục cogs/command
        cogs_dir = os.path.join(BASE_DIR, "cogs", "command")
        print("=" * 45)
        print(f"📂 Đang tìm cogs tại: {cogs_dir}")
        print("=" * 45)

        if not os.path.exists(cogs_dir):
            print(f"❌ Không tìm thấy thư mục! Các thư mục hiện tại: {os.listdir(BASE_DIR)}")
            return

        for filename in sorted(os.listdir(cogs_dir)):
            if filename.endswith(".py") and not filename.startswith("_"):
                ext_name = f"cogs.command.{filename[:-3]}"
                try:
                    await self.load_extension(ext_name)
                    print(f"✅ Đã tải: {ext_name}")
                except Exception as e:
                    print(f"❌ Lỗi tải {ext_name} -> {type(e).__name__}: {e}")

        print("-" * 45)
        print(f"📦 Tổng số Cogs đã nạp : {len(self.cogs)}")
        print(f"⌨️  Tổng số Lệnh (Cmd)  : {len(self.commands)}")
        print("=" * 45)

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name="eden dau yeu")
        await self.change_presence(status=discord.Status.dnd, activity=activity)
        print(f"🟢 Bot đã đăng nhập với tên {self.user} (ID: {self.user.id}) | Tiền tố: {PREFIX}")

async def main():
    if not TOKEN:
        print("❌ LỖI: Thiếu BOT_TOKEN trong setting/.env!")
        return

    bot = MyBot()
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())