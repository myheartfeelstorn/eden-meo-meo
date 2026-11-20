import discord
from discord.ext import commands
from discord.ui import Select, View, Button

class HelpSelect(Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(
                label="Treo Voice",
                description="Sử dụng để bot treo 24/7 trong kênh thoại",
                emoji="<:emoji_119:1573154066484433077>",
                value="voice"
            ),
            discord.SelectOption(
                label="Moderation",
                description="Quản lí server",
                emoji="<:head_mod:1573154412094947380>",
                value="moderation"
            ),
            discord.SelectOption(
                label="Feedback",
                description="Send feedback to the bot developers",
                emoji="📝",
                value="feedback"
            ),
        ]
        super().__init__(
            placeholder="Chọn một danh mục để xem câu hỏi...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        choice = self.values[0]
        
            

        if choice == "voice":
            embed = discord.Embed(
                title="🎧 Voice & 24/7 Stay in Call",
                description="Quản lý kết nối kênh thoại của bot:",
                color=discord.Color.green()
            )
            embed.add_field(name="!join", value="Bắt bot vào kênh thoại của bạn.", inline=False)
            embed.add_field(name="!stay247", value="Giữ bot treo trong kênh thoại 24/7.", inline=False)
            embed.add_field(name="!leave", value="Ngắt kết nối bot khỏi kênh thoại.", inline=False)

        elif choice == "moderation":
            embed = discord.Embed(
                title="moderation",
                description="Các lệnh quản lý thành viên trong server:",
                color=discord.Color.red()
            )
            embed.add_field(name="!kick <member> [reason]", value="Đuổi thành viên khỏi server.", inline=False)
            embed.add_field(name="!ban <member> [reason]", value="Cấm thành viên vĩnh viễn khỏi server.", inline=False)

        elif choice == "feedback":
            embed = discord.Embed(
                title="📝 Feedback System",
                description="Báo lỗi hoặc đề xuất tính năng mới cho đội ngũ phát triển:",
                color=discord.Color.gold()
            )
            embed.add_field(name="!feedback <nội dung>", value="Gửi góp ý trực tiếp đến Admin.", inline=False)

        await interaction.response.edit_message(embed=embed)


class HomeButton(Button):
    def __init__(self, home_embed):
        super().__init__(label="Trang Chủ", style=discord.ButtonStyle.secondary, emoji="🏠")
        self.home_embed = home_embed

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.home_embed)


class HelpView(View):
    def __init__(self, bot, home_embed):
        super().__init__(timeout=180)
        self.add_item(HelpSelect(bot))
        self.add_item(HomeButton(home_embed))


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def custom_help(self, ctx):
        embed = discord.Embed(
            title="Your Fav Puppy",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_image(url="https://i.pinimg.com/736x/be/eb/8a/beeb8af9061a66e88e754c574cd9c0ed.jpg")
        embed.add_field(name="own and dev by", value="<@1435052845006196796> / Eden", inline=True)
        embed.add_field(name="command number", value=str(len(self.bot.commands)), inline=True)
        
        view = HelpView(self.bot, embed)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))