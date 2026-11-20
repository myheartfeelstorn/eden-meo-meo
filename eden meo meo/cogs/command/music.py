import discord
from discord.ext import commands
import wavelink

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play")
    async def play(self, ctx, *, search: str):
        """Phát nhạc qua Lavalink node riêng của bạn"""
        if not ctx.author.voice:
            return await ctx.send("❌ Hãy vào một kênh thoại trước!")

        # Kết nối voice channel và gán player
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        # Tìm kiếm bài hát qua Lavalink sources (YouTube, SoundCloud, v.v.)
        tracks = await wavelink.Playable.search(search)
        if not tracks:
            return await ctx.send("❌ Không tìm thấy bài hát nào phù hợp!")

        track = tracks[0]
        await vc.play(track)
        await ctx.send(f"🎶 Đang phát: **{track.title}**")

async def setup(bot):
    await bot.add_cog(MusicCog(bot))