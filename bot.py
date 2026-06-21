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

    global lol_news_system

    if 'lol_news_system' not in globals():
        lol_news_system = LoLNews(bot)

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


@bot.event
async def on_ready():
    #bot.add_view(VerifyView())
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


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

rom discord.ext import tasks

class LoLNews:
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1295599549808902155
        self.news_loop.start()
        print("LoLNews Started")

    @tasks.loop(minutes=1)
    async def news_loop(self):
        print("NEWS LOOP WORKING")

        channel = self.bot.get_channel(self.channel_id)

        if channel is None:
            print("Channel not found")
            return

        embed = discord.Embed(
            title="🎮 League of Legends",
            description="آخر أخبار وتحديثات League of Legends",
            color=0x00BFFF
        )

        embed.set_footer(text="C2 SYSTEM • GAMING")

        await channel.send(embed=embed)

    @news_loop.before_loop
    async def before_news_loop(self):
        await self.bot.wait_until_ready()

    
bot.run(TOKEN)
