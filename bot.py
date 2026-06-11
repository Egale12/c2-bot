import os
import discord
from discord.ext import commands
import yt_dlp

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="・𝐖𝐄𝐋𝐂𝐎𝐌𝐄")

    if channel:
        await channel.send(
            f"🎉 أهلاً وسهلاً {member.mention} في سيرفر {member.guild.name}!"
        )

#======[loge]=====#
import discord
from datetime import datetime

voice_times = {}

@bot.event
async def on_voice_state_update(member, before, after):

    log_channel = discord.utils.get(member.guild.text_channels, name="𝗖𝟮-𝗦𝗬𝗦𝗧𝗘𝗠")

    if not log_channel:
        return

    # دخول روم
    if before.channel is None and after.channel is not None:

        voice_times[member.id] = datetime.now()

        embed = discord.Embed(
            title="🎤 دخول روم صوتي",
            color=0x00ff66
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(
            name="👤 العضو",
            value=member.mention,
            inline=False
        )

        embed.add_field(
            name="🔊 الروم",
            value=after.channel.mention,
            inline=False
        )

        embed.set_footer(text=f"ID: {member.id}")

        await log_channel.send(embed=embed)

    # خروج روم
    elif before.channel is not None and after.channel is None:

        join_time = voice_times.get(member.id)

        duration = "غير معروف"

        if join_time:
            seconds = int((datetime.now() - join_time).total_seconds())
            minutes = seconds // 60
            duration = f"{minutes} دقيقة"

        embed = discord.Embed(
            title="🔴 خروج من روم صوتي",
            color=0xff0000
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(
            name="👤 العضو",
            value=member.mention,
            inline=False
        )

        embed.add_field(
            name="🔊 الروم",
            value=before.channel.name,
            inline=False
        )

        embed.add_field(
            name="⏱️ مدة الجلسة",
            value=duration,
            inline=False
        )

        embed.set_footer(text=f"ID: {member.id}")

        await log_channel.send(embed=embed)

    # انتقال بين الرومات
    elif before.channel != after.channel:

        embed = discord.Embed(
            title="🔄 انتقال بين الرومات",
            color=0xffcc00
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(
            name="👤 العضو",
            value=member.mention,
            inline=False
        )

        embed.add_field(
            name="📤 من",
            value=before.channel.name,
            inline=True
        )

        embed.add_field(
            name="📥 إلى",
            value=after.channel.name,
            inline=True
        )

        embed.set_footer(text=f"ID: {member.id}")

        await log_channel.send(embed=embed)
from discord.ui import View
import discord

class VerifyView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="✅ Verify",
        style=discord.ButtonStyle.green
    )
    async def verify_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        member_role = discord.utils.get(
            interaction.guild.roles,
            name="Member"
        )

        unverified_role = discord.utils.get(
            interaction.guild.roles,
            name="Unverified"
        )

        if not member_role:
            await interaction.response.send_message(
                "❌ لم يتم العثور على رتبة Member",
                ephemeral=True
            )
            return

        if unverified_role:
            await interaction.user.remove_roles(unverified_role)

        await interaction.user.add_roles(member_role)

        await interaction.response.send_message(
            "✅ تم التوثيق بنجاح",
            ephemeral=True
        )


@bot.command()
async def verify(ctx):

    embed = discord.Embed(
        title="🔐 C2 Verification System",
        description="""
━━━━━━━━━━━━━━━━━━

👋 مرحباً بك في C2

✅ اضغط الزر بالأسفل للتوثيق

🎯 عند التوثيق:
• إزالة رتبة Unverified
• إعطاء رتبة Member

━━━━━━━━━━━━━━━━━━
""",
        color=0x57F287
    )

    embed.set_footer(
        text="C2 Security 🔒 Verification System"
    )

    await ctx.send(
        embed=embed,
        view=VerifyView()
    )

bot.run(TOKEN)
