import os
import discord
from discord.ext import commands
import yt_dlp

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")
    print(f"Logged in as {bot.user}")


@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="・𝐖𝐄𝐋𝐂𝐎𝐌𝐄")

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

    #======[c2help]=====#


@bot.tree.command(name="ping", description="سرعة البوت")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"🏓 Pong! {round(bot.latency * 1000)}ms"
    )

@bot.tree.command(name="avatar", description="صورة العضو")
async def avatar(interaction: discord.Interaction):
    await interaction.response.send_message(
        interaction.user.display_avatar.url
    )

@bot.tree.command(name="userinfo", description="معلومات العضو")
async def userinfo(interaction: discord.Interaction):
    member = interaction.user

    embed = discord.Embed(
        title="معلومات العضو",
        color=discord.Color.blue()
    )

    embed.add_field(name="الاسم", value=member.name, inline=False)
    embed.add_field(name="ID", value=member.id, inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(
    name="serverinfo",
    description="معلومات السيرفر"
)
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild

    embed = discord.Embed(
        title="معلومات السيرفر",
        color=discord.Color.green()
    )

    embed.add_field(
        name="اسم السيرفر",
        value=guild.name,
        inline=False
    )

    embed.add_field(
        name="الأعضاء",
        value=guild.member_count,
        inline=False
    )

    embed.add_field(
        name="ID",
        value=guild.id,
        inline=False
    )

    await interaction.response.send_message(embed=embed)

    embed.add_field(name="اسم السيرفر", value=guild.name, inline=False)
    embed.add_field(name="الأعضاء", value=guild.member_count, inline=False)
    embed.add_field(name="ID", value=guild.id, inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="c2help", description="عرض أوامر البوت")
async def c2help(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📖 C2 Help Menu",
        description="قائمة أوامر البوت",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="⚙️ أوامر عامة",
        value="""
/ping
/avatar
/userinfo
/serverinfo
/c2help
""",
        inline=False
    )

    await interaction.response.send_message(embed=embed)

    #======[c2help]=====#


import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

MEMBER_ROLE_ID = 1295597136947449999
UNVERIFIED_ROLE_ID = 1516197855381950609

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Verify",
        style=discord.ButtonStyle.success,
        emoji="✅",
        custom_id="verify_button"
    )
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        member_role = interaction.guild.get_role(MEMBER_ROLE_ID)
        unverified_role = interaction.guild.get_role(UNVERIFIED_ROLE_ID)

        if member_role in interaction.user.roles:
            await interaction.response.send_message(
                "✅ أنت موثق مسبقاً",
                ephemeral=True
            )
            return

        await interaction.user.add_roles(member_role)

        if unverified_role:
            await interaction.user.remove_roles(unverified_role)

        await interaction.response.send_message(
            "✅ تم توثيقك بنجاح، أهلاً بك في السيرفر!",
            ephemeral=True
        )

@bot.event
async def on_ready():
    bot.add_view(VerifyView())
    print(f"✅ Logged in as {bot.user}")

@bot.command()
@commands.has_permissions(administrator=True)
async def verify(ctx):

    embed = discord.Embed(
        title="🔰 Verification",
        description="اضغط على الزر بالأسفل للتوثيق والدخول إلى السيرفر.",
        color=0x3498db
    )

    embed.set_footer(text="C2 SYSTEM")

    await ctx.send(
        embed=embed,
        view=VerifyView()
    )

bot.run(TOKEN)
