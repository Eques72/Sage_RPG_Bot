from questionHandler import questionHandler
from nextcord.ext import commands
import nextcord
import os
from dotenv import load_dotenv


def splitMessage(mes: str):
    mes_list = []

    while(len(mes) > 2000):
       pos = mes.rfind("\n",0,2000)
       if mes[0:pos].count("```")%2 == 0: 
        mes_list.append(mes[0:pos])
        mes = mes[pos:]
       else:
        pos = mes.rfind("\n",0,pos-1)
        if mes[0:pos].count("```")%2 == 0:
            mes_list.append(mes[0:pos])
            mes = mes[pos:] 
        else:
            mes_list.append(mes[0:pos]+"```")
            mes = "```fix\n" + mes[pos:]

    mes_list.append(mes)

    return mes_list

load_dotenv()

qH = questionHandler()

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!',description="Sage has all the answers ", intents = intents)

@bot.command()
async def dndspell(ctx):
    reply_s = qH.handleQuestion(ctx.message.content)

    if(len(reply_s) <= 2000):
         await ctx.reply(reply_s)
    else:
        splited_mes = splitMessage(reply_s)
        for s in splited_mes:
            await ctx.send(s)

@bot.command()
async def dndrace(ctx):
    reply_s = qH.handleQuestion(ctx.message.content)

    if(len(reply_s) <= 2000):
         await ctx.reply(reply_s)
    else:
        splited_mes = splitMessage(reply_s)
        for s in splited_mes:
            await ctx.send(s)

@bot.command()
async def dndbackground(ctx):
    reply_s = qH.handleQuestion(ctx.message.content)

    if(len(reply_s) <= 2000):
         await ctx.reply(reply_s)
    else:
        splited_mes = splitMessage(reply_s)
        for s in splited_mes:
            await ctx.send(s)

@bot.command()
async def dndfeat(ctx):
    reply_s = qH.handleQuestion(ctx.message.content)

    if(len(reply_s) <= 2000):
         await ctx.reply(reply_s)
    else:
        splited_mes = splitMessage(reply_s)
        for s in splited_mes:
            await ctx.send(s)

@bot.command()
async def dndclass(ctx):
    reply_s = qH.handleQuestion(ctx.message.content)

    if(len(reply_s) <= 2000):
         await ctx.reply(reply_s)
    else:
        splited_mes = splitMessage(reply_s)
        for s in splited_mes:
            await ctx.send(s)

@bot.command()
async def dndsage(ctx):
    reply_s = qH.handleQuestion(ctx.message.content)

    if(len(reply_s) <= 2000):
         await ctx.reply(reply_s)
    else:
        splited_mes = splitMessage(reply_s)
        for s in splited_mes:
            await ctx.send(s)

@bot.command()
async def dndhelp(ctx):
    reply_s = qH.handleQuestion(ctx.message.content)

    if(len(reply_s) <= 2000):
         await ctx.reply(reply_s)
    else:
        splited_mes = splitMessage(reply_s)
        for s in splited_mes:
            await ctx.send(s)

bot.run(os.getenv('TOKEN'))
