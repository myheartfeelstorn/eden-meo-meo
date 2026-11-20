import discord
from discord.ext import commands

class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stay_channels = {}  # {guild_id: channel_id}

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            try:
                if ctx.voice_client:
                    if ctx.voice_client.channel == channel:
                        return await ctx.send(f"I'm already in **{channel.name}**!")
                    await ctx.voice_client.move_to(channel)
                else:
                    await channel.connect()
                await ctx.send(f"Already connected to **{channel.name}**")
            except Exception as e:
                await ctx.send(f"Failed to join voice channel: `{e}`")
                print(f"[Voice Error] {e}")
        else:
            await ctx.send("Join a channel first <:conchotucgian:1573157838526619741>")

    @commands.command()
    async def stay247(self, ctx):
        if not ctx.author.voice:
            return await ctx.send("Join a channel first <:conchotucgian:1573157838526619741>")

        channel = ctx.author.voice.channel
        try:
            if ctx.voice_client:
                await ctx.voice_client.move_to(channel)
            else:
                await channel.connect()

            self.stay_channels[ctx.guild.id] = channel.id
            await ctx.send(f"Okey i'll stay in **{channel.name}** from now!")
        except Exception as e:
            await ctx.send(f"Failed to enable 24/7: `{e}`")
            print(f"[Voice Error] {e}")

    @commands.command()
    async def leave(self, ctx):
        if ctx.guild.id in self.stay_channels:
            del self.stay_channels[ctx.guild.id]

        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("24/7 disabled and left the voice channel.")
        else:
            await ctx.send("I'm not in any voice channel <:conchotucgian:1573157838526619741>")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Only trigger if it's the bot itself getting disconnected
        if member.id == self.bot.user.id and after.channel is None:
            if before.channel:
                guild_id = before.channel.guild.id
                if guild_id in self.stay_channels:
                    channel = self.bot.get_channel(self.stay_channels[guild_id])
                    if channel:
                        try:
                            await channel.connect()
                        except Exception as e:
                            print(f"[Auto-Reconnect Error] {e}")

async def setup(bot):
    await bot.add_cog(VoiceCog(bot))