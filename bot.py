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
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"SYNC ERROR: {e}")

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
    log_channel = discord.utils.get(
        member.guild.text_channels,
        name="𝗖𝟮-𝗦𝗬𝗦𝗧𝗘𝗠"
    )

    if not log_channel:
        return

    # دخول روم
    if before.channel is None and after.channel is not None:
        voice_times[member.id] = datetime.now()

        embed = discord.Embed(
            title="🟢 Joined Channel 🎙️",
            description=f"{member.mention} joined the voice channel",
            color=0x00ff88
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(
            name="🔊 Channel",
            value=after.channel.mention,
            inline=False
        )
        embed.set_footer(text=f"ID: {member.id}")

        await log_channel.send(embed=embed)

    # خروج روم
    elif before.channel is not None and after.channel is None:

        duration = "Unknown"

        if member.id in voice_times:
            seconds = int(
                (datetime.now() - voice_times[member.id]).total_seconds()
            )

            hours = seconds // 3600
            minutes = (seconds % 3600) // 60

            duration = f"{hours}h {minutes}m"

        embed = discord.Embed(
            title="🔴 Left Channel 🎙️",
            description=f"{member.mention} left the voice channel",
            color=0xff4d4d
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(
            name="🔊 Channel",
            value=before.channel.name,
            inline=False
        )

        embed.add_field(
            name="⏱️ Time Spent",
            value=duration,
            inline=False
        )

        embed.set_footer(text=f"ID: {member.id}")

        await log_channel.send(embed=embed)

    # نقل روم
    elif before.channel != after.channel:

        embed = discord.Embed(
            title="🟡 Moved Channel 🔄",
            color=0xffcc00
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(
            name="📤 From",
            value=before.channel.mention,
            inline=True
        )

        embed.add_field(
            name="📥 To",
            value=after.channel.mention,
            inline=True
        )

        embed.set_footer(text=f"ID: {member.id}")

        await log_channel.send(embed=embed)

    # بدأ ستريم
    if not before.self_stream and after.self_stream:

        embed = discord.Embed(
            title="🟣 Stream Started 📺",
            description=f"{member.mention} started streaming",
            color=0x9b59b6
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        await log_channel.send(embed=embed)

    # وقف ستريم
    elif before.self_stream and not after.self_stream:

        embed = discord.Embed(
            title="🔴 Stream Ended 📺",
            description=f"{member.mention} stopped streaming",
            color=0xe74c3c
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        await log_channel.send(embed=embed)

    # فتح كام
    if not before.self_video and after.self_video:

        embed = discord.Embed(
            title="📷 Camera Enabled",
            description=f"{member.mention} turned on camera",
            color=0x3498db
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        await log_channel.send(embed=embed)

    # سكر كام
    elif before.self_video and not after.self_video:

        embed = discord.Embed(
            title="📷 Camera Disabled",
            description=f"{member.mention} turned off camera",
            color=0x95a5a6
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        await log_channel.send(embed=embed)

    #======[c2help]=====#
from discord import app_commands
import discord
import datetime

# /clear
@bot.tree.command(name="clear", description="حذف الرسائل")
async def clear(interaction: discord.Interaction, amount: int):
    if not interaction.user.guild_permissions.manage_messages:
        return await interaction.response.send_message("❌ لا تملك الصلاحية", ephemeral=True)

    await interaction.response.defer(ephemeral=True)
    await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"✅ تم حذف {amount} رسالة")

# /kick
@bot.tree.command(name="kick", description="طرد عضو")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No Reason"):
    if not interaction.user.guild_permissions.kick_members:
        return await interaction.response.send_message("❌ لا تملك الصلاحية", ephemeral=True)

    await member.kick(reason=reason)
    await interaction.response.send_message(f"👢 تم طرد {member.mention}")

# /ban
@bot.tree.command(name="ban", description="حظر عضو")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No Reason"):
    if not interaction.user.guild_permissions.ban_members:
        return await interaction.response.send_message("❌ لا تملك الصلاحية", ephemeral=True)

    await member.ban(reason=reason)
    await interaction.response.send_message(f"🔨 تم حظر {member.mention}")

# /unban
@bot.tree.command(name="unban", description="فك حظر عضو")
async def unban(interaction: discord.Interaction, user_id: str):
    if not interaction.user.guild_permissions.ban_members:
        return await interaction.response.send_message("❌ لا تملك الصلاحية", ephemeral=True)

    user = await bot.fetch_user(int(user_id))
    await interaction.guild.unban(user)
    await interaction.response.send_message(f"✅ تم فك حظر {user}")

# /mute
@bot.tree.command(name="mute", description="كتم عضو")
async def mute(interaction: discord.Interaction, member: discord.Member, minutes: int):
    if not interaction.user.guild_permissions.moderate_members:
        return await interaction.response.send_message("❌ لا تملك الصلاحية", ephemeral=True)

    until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
    await member.timeout(until)

    await interaction.response.send_message(
        f"🔇 تم كتم {member.mention} لمدة {minutes} دقيقة"
    )

# /unmute
@bot.tree.command(name="unmute", description="فك كتم عضو")
async def unmute(interaction: discord.Interaction, member: discord.Member):
    if not interaction.user.guild_permissions.moderate_members:
        return await interaction.response.send_message("❌ لا تملك الصلاحية", ephemeral=True)

    await member.timeout(None)
    await interaction.response.send_message(f"🔊 تم فك كتم {member.mention}")

# /lock
@bot.tree.command(name="lock", description="قفل الروم")
async def lock(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.manage_channels:
        return await interaction.response.send_message("❌ لا تملك الصلاحية", ephemeral=True)

    await interaction.channel.set_permissions(
        interaction.guild.default_role,
        send_messages=False
    )

    await interaction.response.send_message("🔒 تم قفل الروم")

# /unlock
@bot.tree.command(name="unlock", description="فتح الروم")
async def unlock(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.manage_channels:
        return await interaction.response.send_message("❌ لا تملك الصلاحية", ephemeral=True)

    await interaction.channel.set_permissions(
        interaction.guild.default_role,
        send_messages=True
    )

    await interaction.response.send_message("🔓 تم فتح الروم")

# /slowmode
@bot.tree.command(name="slowmode", description="تفعيل السلو مود")
async def slowmode(interaction: discord.Interaction, seconds: int):
    if not interaction.user.guild_permissions.manage_channels:
        return await interaction.response.send_message("❌ لا تملك الصلاحية", ephemeral=True)

    await interaction.channel.edit(slowmode_delay=seconds)
    await interaction.response.send_message(f"🐢 تم ضبط السلو مود على {seconds} ثانية")

# /nick
@bot.tree.command(name="nick", description="تغيير اسم عضو")
async def nick(interaction: discord.Interaction, member: discord.Member, nickname: str):
    if not interaction.user.guild_permissions.manage_nicknames:
        return await interaction.response.send_message("❌ لا تملك الصلاحية", ephemeral=True)

    await member.edit(nick=nickname)
    await interaction.response.send_message(f"✏️ تم تغيير اسم {member.mention}")

# /say
@bot.tree.command(name="say", description="إرسال رسالة")
async def say(interaction: discord.Interaction, message: str):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ لا تملك الصلاحية", ephemeral=True)

    await interaction.channel.send(message)
    await interaction.response.send_message("✅ تم الإرسال", ephemeral=True)


@bot.tree.command(name="ping", description="سرعة البوت")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"🏓 Pong! {round(bot.latency * 1000)}ms"
    )


    await interaction.response.send_message(
        embed=embed,
        view=VerifyView()
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
📁 إدارة
/clear
/kick
/ban
/unban
/mute
/unmute
/warn
/role
/removerole

📁 معلومات
/ping
/avatar
/userinfo
/serverinfo

📁 الرومات
/lock
/unlock
/slowmode

📁 أدوات
/say
/embed
/nick

📁 النظام
/setverify
/c2help
""",
        inline=False
    )

    await interaction.response.send_message(embed=embed)

    #======[c2help]=====#

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
    label="Verify",
    emoji="✅",
    style=discord.ButtonStyle.success
)
    
    async def verify_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        member_role = interaction.guild.get_role(1295597136947449999)
        unverified_role = interaction.guild.get_role(1516197855381950609)

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
            "✅ تم توثيقك بنجاح",
            ephemeral=True
        )


@bot.tree.command(
    name="verify",
    description="إرسال رسالة التوثيق"
)
async def verify(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🛡️ C2 SECURITY",
        description="""
 WELCOME TO C2 SECURITY🛡️

 لضمان أمان السيرفر ومنع الحسابات الوهمية
    اضغط الزر بالأسفل لإكمال التوثيق
""",
        color=0x00BFFF
    )

    # حط رابط صورة اللوقو هنا
    embed.set_image(url="https://i.postimg.cc/SxFGjg0z/IMG-0880.png")

    embed.set_footer(text="C2 SYSTEM • SECURITY")

    await interaction.response.send_message(
        embed=embed,
        view=VerifyView()
    )

from discord.ext import tasks
import aiohttp

class LoLNews:
    def __init__(self, bot):
        print("LOLNEWS CREATED")
        self.bot = bot
        self.channel_id = 1295599549808902155
        self.last_title = None
        self.news_loop.start()

    @tasks.loop(minutes=1)
    async def news_loop(self):
        channel = self.bot.get_channel(self.channel_id)

        if not channel:
            print("CHANNEL NOT FOUND")
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://www.riotgames.com/api/news"
                ) as response:

                    data = await response.json()

                    if not data.get("result"):
                        return

                    news = data["result"][0]

                    title = news["title"]

                    if title == self.last_title:
                        return

                    self.last_title = title

                    embed = discord.Embed(
                        title="🎮 League of Legends News",
                        description=title,
                        color=0x00BFFF
                    )

                    if news.get("bannerUrl"):
                        embed.set_image(url=news["bannerUrl"])

                    embed.add_field(
                        name="الرابط",
                        value=news["url"],
                        inline=False
                    )

                    await channel.send(embed=embed)

        except Exception as e:
            print(f"LOL NEWS ERROR: {e}")
    
bot.run(TOKEN)
