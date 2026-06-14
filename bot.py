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
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")

    if channel:
        await channel.send(
            f"- Welcome to C2 .\n\n"
            f"- {member.mention} .\n\n"
            f"- Members: {member.guild.member_count} ."
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

        const { EmbedBuilder } = require('discord.js');


        embed = discord.Embed(
    title="🟢 Stream Started 🎧 🔴 LIVE",
    description=f"{member.mention} started streaming in the 🔊 {after.channel.name} voice channel",
    color=0x00ff66
)

embed.set_footer(text=f"ID: {member.id}")
embed.timestamp = discord.utils.utcnow()


await log_channel.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📖 C2 Help Menu",
        description="قائمة أوامر البوت",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="👋 أوامر الإدارة",
        value="""
!ban - حظر عضو
!kick - طرد عضو
!clear - حذف الرسائل
!mute - كتم عضو
!unmute - فك الكتم
        """,
        inline=False
    )

    embed.add_field(
        name="🎵 أوامر الموسيقى",
        value="""
!play - تشغيل أغنية
!stop - إيقاف الموسيقى
!skip - تخطي الأغنية
!leave - خروج البوت
        """,
        inline=False
    )

    embed.add_field(
        name="⚙️ أوامر عامة",
        value="""
!ping - سرعة البوت
!avatar - صورة العضو
!userinfo - معلومات العضو
!serverinfo - معلومات السيرفر
        """,
        inline=False
    )

    embed.set_footer(text="C2 Bot © 2026")
    await ctx.send(embed=embed


bot.run(TOKEN)