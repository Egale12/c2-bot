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

        embed = discord.Embed(
            title="🟢 Stream Started",
            description="...",
            color=0x00ff66
        )

    



@bot.command(name="c2help")
async def c2help(ctx):
    embed = discord.Embed(
        title="📖 C2 Help Menu",
        description="قائمة أوامر البوت",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="🛡️ أوامر الإدارة",
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

    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

from discord.ext import commands

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"✅ تم طرد {member.mention}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 تم حظر {member.mention}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"✅ تم فك الحظر عن {user}")


@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(member.display_avatar.url)


@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author

    embed = discord.Embed(
        title="معلومات العضو",
        color=discord.Color.blue()
    )

    embed.add_field(name="الاسم", value=member.name, inline=False)
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="تاريخ الدخول", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild

    embed = discord.Embed(
        title="معلومات السيرفر",
        color=discord.Color.green()
    )

    embed.add_field(name="اسم السيرفر", value=guild.name, inline=False)
    embed.add_field(name="الأعضاء", value=guild.member_count, inline=False)
    embed.add_field(name="ID", value=guild.id, inline=False)



@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)


bot.run(TOKEN)
