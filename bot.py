import discord
from discord.ext import commands
import maplestory
import database
from datetime import datetime,timedelta
from LOL import LOLAPI
import lunch
from dotenv import load_dotenv
import os
from updatelog import UpdateLog
import asyncio

load_dotenv()
discordtoken = os.getenv("discordbot")
discordtesttoken = os.getenv("discordtest")


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='%',intents=intents)

@bot.event
async def on_ready():
    guild_list = bot.guilds
    print(f"현재 디스코드 봇 가입 서버 개수 : {len(guild_list)}")
    output_text = "\n".join([f"{i.name}" for i in guild_list])
    print(f"목록\n {output_text}")
    with open("guild_list.txt", "w",encoding="utf-8") as f:
    # 파일에 텍스트 쓰기
        f.write(f"server len : {len(guild_list)}\n")
        f.write(f"server name\n")
        f.write(f"{output_text}")
    
    await bot.change_presence(activity=discord.Game(name="명령어 목록 %도움말"))
@bot.command()
async def 메이플(ctx,arg):
    msg = None
    db = database.maplecon()
    mapleapi = maplestory.maplestoryC()
    ocid = db.findOcid(arg)
    if ocid == None:
        msg =  mapleapi.ocid(arg)
        mapleapi.characterinfo(arg)
    if msg != None:
        await ctx.send(msg,reference=ctx.message)
    else:
        ocid = db.findOcid(arg)
        basic = db.findBasic(ocid)
        dbtime = datetime.strptime(basic[1],"%Y-%m-%dT%H:%M%z")
        yesterday = datetime.today() - timedelta(days=1)
        if mapleapi.update_time() and yesterday.date() != dbtime.date():
            mapleapi.updateCharacterinfo(arg)
            basic = db.findBasic(ocid)
        embed=discord.Embed(title="메이플 캐릭터 정보", color=0xff7300)
        embed.set_thumbnail(url=f"{basic[3]}")
        embed.add_field(name="닉네임", value=f"{arg}", inline=True)
        embed.add_field(name="길드명", value=f"{basic[2]}", inline=True)
        embed.add_field(name="직업", value=f"{basic[5]}", inline=True)
        embed.add_field(name="레벨", value=f"Lv.{basic[0]}", inline=True)
        embed.add_field(name="유니온레벨", value=f"Lv.{basic[6]}", inline=True)
        embed.add_field(name="무릉도장 기록", value=f"{basic[7]}층", inline=True)
        embed.set_footer(text=f"갱신일자 : {basic[1]}")
        await ctx.channel.send(embed=embed,reference=ctx.message)

@bot.command()
async def 롤(ctx,*args):
    arg = ''.join(args)
    print(arg)
    lolapi = LOLAPI()
    puuid,code = lolapi.getpuuid(arg)
    if code == -1:
        await ctx.channel.send(puuid,reference=ctx.message)
        return
    id,code = lolapi.getid(puuid)
    if code == -1:
        await ctx.channel.send(id)
        return
    blueteam,redteam = await lolapi.ingameinfo(id)

    if type(blueteam) == str:
        await ctx.channel.send(blueteam,reference=ctx.message)
        return
    else:
        embedblue = discord.Embed(title="블루팀", colour=0x00b7ff)
        embedblue.set_author(name=f"{arg}님의 현재 게임상황")
        embedblue.add_field(name=f"{blueteam[0]['summonerName']}",
                            value=f"{blueteam[0]['championname']}\n솔랭: {blueteam[0]['SOLO_tier']} {blueteam[0]['SOLO_rank']}\n자랭: {blueteam[0]['FREE_tier']} {blueteam[0]['FREE_rank']}",
                            inline=False)
        embedblue.add_field(name=f"{blueteam[1]['summonerName']}",
                            value=f"{blueteam[1]['championname']}\n솔랭: {blueteam[1]['SOLO_tier']} {blueteam[1]['SOLO_rank']}\n자랭: {blueteam[1]['FREE_tier']} {blueteam[1]['FREE_rank']}",
                            inline=False)
        embedblue.add_field(name=f"{blueteam[2]['summonerName']}",
                            value=f"{blueteam[2]['championname']}\n솔랭: {blueteam[2]['SOLO_tier']} {blueteam[2]['SOLO_rank']}\n자랭: {blueteam[2]['FREE_tier']} {blueteam[2]['FREE_rank']}",
                            inline=False)
        embedblue.add_field(name=f"{blueteam[3]['summonerName']}",
                            value=f"{blueteam[3]['championname']}\n솔랭: {blueteam[3]['SOLO_tier']} {blueteam[3]['SOLO_rank']}\n자랭: {blueteam[3]['FREE_tier']} {blueteam[3]['FREE_rank']}",
                            inline=False)
        embedblue.add_field(name=f"{blueteam[4]['summonerName']}",
                            value=f"{blueteam[4]['championname']}\n솔랭: {blueteam[4]['SOLO_tier']} {blueteam[4]['SOLO_rank']}\n자랭: {blueteam[4]['FREE_tier']} {blueteam[4]['FREE_rank']}",
                            inline=False)

        embedred = discord.Embed(title="레드팀", colour=0xff0000, timestamp=datetime.now())
        embedred.add_field(name=f"{redteam[0]['summonerName']}",
                            value=f"{redteam[0]['championname']}\n솔랭: {redteam[0]['SOLO_tier']} {redteam[0]['SOLO_rank']}\n자랭: {redteam[0]['FREE_tier']} {redteam[0]['FREE_rank']}",
                            inline=False)
        embedred.add_field(name=f"{redteam[1]['summonerName']}",
                            value=f"{redteam[1]['championname']}\n솔랭: {redteam[1]['SOLO_tier']} {redteam[1]['SOLO_rank']}\n자랭: {redteam[1]['FREE_tier']} {redteam[1]['FREE_rank']}",
                            inline=False)
        embedred.add_field(name=f"{redteam[2]['summonerName']}",
                            value=f"{redteam[2]['championname']}\n솔랭: {redteam[2]['SOLO_tier']} {redteam[2]['SOLO_rank']}\n자랭: {redteam[2]['FREE_tier']} {redteam[2]['FREE_rank']}",
                            inline=False)
        embedred.add_field(name=f"{redteam[3]['summonerName']}",
                            value=f"{redteam[3]['championname']}\n솔랭: {redteam[3]['SOLO_tier']} {redteam[3]['SOLO_rank']}\n자랭: {redteam[3]['FREE_tier']} {redteam[3]['FREE_rank']}",
                            inline=False)
        embedred.add_field(name=f"{redteam[4]['summonerName']}",
                            value=f"{redteam[4]['championname']}\n솔랭: {redteam[4]['SOLO_tier']} {redteam[4]['SOLO_rank']}\n자랭: {redteam[4]['FREE_tier']} {redteam[4]['FREE_rank']}",
                            inline=False)
        await ctx.channel.send(embed=embedblue,reference=ctx.message)
        await ctx.channel.send(embed=embedred,reference=ctx.message)
@bot.command()
async def 도움말(ctx):
    embedhelp=discord.Embed(title="도움말", description="빵먹는아이 봇은 모든 명령어를 %로 시작합니다. 문의 사항은 다음 깃허브 링크를 통해 문의해주세요.",color=0x2fa295)
    embedhelp.add_field(name='"%메이플" 캐릭터이름', value="메이플 캐릭터를 검색합니다.\n장기 미접속 캐릭터에 대해서는 검색이 불가 할 수 있습니다.", inline=False)
    embedhelp.add_field(name='"%롤" 닉네임', value="해당 플레이어가 현재 플레이 중인 롤 게임 정보를 가져옵니다.", inline=False)
    embedhelp.add_field(name='"%점메추"', value="점심메뉴를 추천해줍니다.", inline=False)
    embedhelp.add_field(name='"%업데이트목록"', value="빵먹는아이봇의 최근 업데이트 목록을 보여줍니다.", inline=False)

    embedhelp.add_field(name="", value="이 외의 내용은 추후 업데이트 예정입니다.", inline=False)
    await ctx.channel.send(embed=embedhelp)

@bot.command()
async def 점메추(ctx):
    lunchModel = lunch.lunch()
    menu = lunchModel.get_lunch()
    await ctx.channel.send(f"{ctx.message.author.mention}님! 점심으로 {menu} 어떤가요?")
    if menu == "왕돈가스":
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
            voice = await channel.connect() #음성채널 접속
            voice.play(discord.FFmpegPCMAudio(executable = '/usr/bin/ffmpeg',source="./esteregg/missing.mp3"))
            while voice.is_playing():  
                await asyncio.sleep(0.1)
            await voice.disconnect()  

@bot.command()
async def 업데이트목록(ctx):
    logClass = UpdateLog()
    log = logClass.get_update_log()
    content = "\n".join(log['content'])

    embed = discord.Embed(title="업데이트 내용",
                      colour=0x11ff00)
    embed.add_field(name=f"{log['date']}",
                    value=f"{content}",
                    inline=False)
    embed.set_footer(text=f"ver {log['ver']}")
    await ctx.channel.send(embed=embed)

@bot.command()
async def get_guild(ctx):
    guild_list = bot.guilds
    print(f"현재 디스코드 봇 가입 서버 개수 : {len(guild_list)}")
    output_text = "\n".join([f"{i.name}" for i in guild_list])
    print(f"목록\n {output_text}")
    with open("guild_list.txt", "w",encoding="utf-8") as f:
        # 파일에 텍스트 쓰기
        f.write(f"server len : {len(guild_list)}\n")
        f.write(f"server name\n")
        f.write(f"{output_text}")


bot.run(discordtoken)