import discord
from discord.ext import commands
from datetime import timedelta

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Không có lý do"):
        """Đuổi thành viên khỏi server."""
        await member.kick(reason=reason)
        await ctx.send(f"👢 Đã kick **{member.display_name}**. Lý do: {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Không có lý do"):
        """Cấm vĩnh viễn thành viên khỏi server."""
        await member.ban(reason=reason)
        await ctx.send(f"🔨 Đã ban **{member.display_name}**. Lý do: {reason}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, member: discord.Member, role: discord.Role):
        """remove or add roles to member """
        # Automatically removes the role if they have it, or adds it if they don't
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f"➖ Đã gỡ role **{role.name}** khỏi **{member.display_name}**.")
        else:
            await member.add_roles(role)
            await ctx.send(f"➕ Đã cấp role **{role.name}** cho **{member.display_name}**.")

    @commands.command(aliases=["mute", "timeout"])
    @commands.has_permissions(moderate_members=True)
    async def restrict(self, ctx, member: discord.Member, minutes: int = 10, *, reason="Không có lý do"):
        """Hạn chế (Mute) người dùng nhắn tin trong khoảng thời gian nhất định."""
        duration = discord.utils.utcnow() + timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await ctx.send(f"🔇 Đã cấm chat **{member.display_name}** trong {minutes} phút. Lý do: {reason}")

    # Bắt lỗi cục bộ cho riêng file moderation.py để tránh crash
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Bạn không đủ quyền trong server để dùng lệnh này!")
        elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            await ctx.send("⚠️ Sai cú pháp. Hãy tag đúng người hoặc role. Ví dụ: `.kick @user [lý do]`")

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))