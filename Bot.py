import questionHandler
import nextcord
import os
import dotenv
from nextcord.ext import commands

####=============================BOTSAGE CLASS====================================#####
class BotSage(commands.Bot):

    __statuses = ("DESKTOP", "MOBILE", "WEB")
    commandType = ("SPELL","SAGE","BACKGROUND","RACE","CLASS","FEAT","HELP")
    __memberStatus = __statuses[0]
    
    def __init__(self):
        intents = nextcord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.presences = True
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents = intents, help_command=None)
        self.qH = questionHandler.QuestionHandler()

    @staticmethod
    def getMemberStatus():
        return BotSage.__memberStatus

    def checkMemberStatus(self,member):
        status = BotSage.__statuses[0] #default status
        if member.raw_status == nextcord.Status.offline:
            status = BotSage.__statuses[0]
        elif member.desktop_status != nextcord.Status.offline:
            status = BotSage.__statuses[0]
        elif member.is_on_mobile() == True:
            status = BotSage.__statuses[1]
        elif member.web_status != nextcord.Status.offline:
            status = BotSage.__statuses[2]

        BotSage.__memberStatus = status

    def splitMessage(self,mes: str):
        mes_list = []

        pos = 1995
        while len(mes) > 2000 and pos != -1:
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

    async def commandToMessage(self, ctx, category:str):
        bot.checkMemberStatus(ctx.author)
        reply_s = bot.qH.handleQuestion(ctx.message.content, category, BotSage.getMemberStatus())

        if(len(reply_s) <= 2000):
            await ctx.reply(reply_s)
        else:
            splited_mes = bot.splitMessage(reply_s)
            for s in splited_mes:
                await ctx.send(s)


####===============================BOT INITIALIZATION==================================#####
dotenv.load_dotenv()
bot = BotSage()

####=============================ASYNC COMMANDS DEF====================================#####
@bot.command()
async def dndspell(ctx):
    await bot.commandToMessage(ctx, BotSage.commandType[0])

@bot.command()
async def dndrace(ctx):   
    await bot.commandToMessage(ctx,BotSage.commandType[3])

@bot.command()
async def dndbackground(ctx):
    await bot.commandToMessage(ctx,BotSage.commandType[2])

@bot.command()
async def dndfeat(ctx):
    await bot.commandToMessage(ctx,BotSage.commandType[5])

@bot.command()
async def dndclass(ctx):
    await bot.commandToMessage(ctx,BotSage.commandType[4])

@bot.command()
async def dndsage(ctx):
    await bot.commandToMessage(ctx,BotSage.commandType[1])

@bot.command()
async def dndhelp(ctx):
    await bot.commandToMessage(ctx,BotSage.commandType[6])

####===============================RUN METHOD==================================#####
bot.run(os.getenv('TOKEN'))
