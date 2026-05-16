import discord
from discord.ext import commands
import os
import asyncio
import yt_dlp

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# إعدادات تشغيل الصوت من اليوتيوب بدون تقطيع
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'default_search': 'ytsearch',
    'nocheckcertificate': True,
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

@bot.event
async def on_ready():
    print(f'🚀 {bot.user} شغال وجاهز للمزيكا 24 ساعة!')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"👍 دخلت روم: {channel.name}")
    else:
        await ctx.send("❌ ادخل روم صوتي الأول يا صاحبي!")

@bot.command()
async def play(ctx, *, search: str):
    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            return await ctx.send("❌ ادخل روم صوتي الأول يا صاحبي!")
    
    await ctx.send(f"🔍 بدور على: **{search}**...")
    
    loop = asyncio.get_event_loop()
    try:
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(search, download=False))
        if 'entries' in data:
            track = data['entries'][0]
        else:
            track = data
            
        url = track['url']
        title = track['title']
        
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            
        source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)
        await ctx.send(f"🎶 مشغل دلوقتي: **{title}**")
        
    except Exception as e:
        print(e)
        await ctx.send("❌ حصلت مشكلة وأنا بشغل الأغنية، جرب تاني!")

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("🛑 وقفت المزيكا.")
    else:
        await ctx.send("❌ مفيش حاجة شغالة أصلاً!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 طلعت من الروم.")
    else:
        await ctx.send("❌ أنا مش في روم صوتي!")

# تشغيل البوت بالتوكن المخفي في Railway بأمان
bot.run('MTUwNTE2MDc3Mzg3MjM5MDE3NA.GVfCwh.vHrId43i0hPovjDAGQ0bKeLWnubBZq2nB1AbHA')
