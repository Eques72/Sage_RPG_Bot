import sage
from xmlrpc.client import boolean

class QuestionHandler:

    def __init__(self):
        pass

    def handleQuestion(self, question : str, clientStatus : str):
        s = sage.Sage(clientStatus)      
        question = question.lower()
        interpretedQuestion = self.interpreteQuestions(question) 

        answer = ""
        if(interpretedQuestion[3] == "simple"):
            answer = s.askQuestion(interpretedQuestion[0],interpretedQuestion[1])     
        elif(interpretedQuestion[3] == "deep"):
            if len(interpretedQuestion[2]) < 3 and len(interpretedQuestion[2]) != 0:
                answer = s.getFailAnswer("Search phrase after \"-f\" flag is too short")
            else:
                answer = s.askExpandedQuestion(interpretedQuestion[0],interpretedQuestion[1],interpretedQuestion[2])
        elif(interpretedQuestion[3] == "search"):
            if len(interpretedQuestion[2]) < 3 and len(interpretedQuestion[2]) != 0:
                answer = s.getFailAnswer("Search phrase after \"-f\" flag is too short")
            else:
                answer = s.askSearchQuestion(interpretedQuestion[1], interpretedQuestion[2])
        elif(interpretedQuestion[3] == "help"):
            f = open("helpInfo.txt", "r")
            if f.readable:
                answer = f.read()
            else:
                answer = s.getFailAnswer("File missing")
            f.close()
        else:
            answer = s.getFailAnswer("Command unknown")
        return answer
   

    def interpreteQuestions(self, question : str):
        prefix = ""
        postfix = ""
        searchText = ""
        type = "" #default if simple search, deep if feature for class, diferent for search
        data = ()

        if(question.startswith("!dndspell")): #simple no flags
            prefix = "spell"
            type = "simple"
            data = self.formQuestion(question, 0)
        elif(question.startswith("!dndfeat")): #simple no flags
            prefix = "feat"
            type = "simple"
            data = self.formQuestion(question, 0)
     #sage is used to search 
        elif(question.startswith("!dndsage")): #difereent flags
            prefix = "sage"
            type = "search"
            data = self.formQuestion(question, 1) 
     #use extra flag -f to search for specific ability 
     #use flag -s for subclass info eg artificer:armorer will be !dndclass artificer -s armorer
        elif(question.startswith("!dndclass")): #deep flags        
            prefix = ""
            type = "deep"
            data = self.formQuestion(question, 1)
     #use extra flag -f to search for specific ability 
        elif(question.startswith("!dndrace")): #deep flags
            prefix = "" 
            type = "deep"
            data = self.formQuestion(question, 1)
        elif(question.startswith("!dndbackground")): #simple no flags
            prefix = "background" 
            type = "simple"
            data = self.formQuestion(question, 0)
        elif(question.startswith("!dndhelp")): #simple no flags
            type = "help"
            data = ("", "")
        else:
            data = ("", "")
        postfix = data[0]
        searchText = data[1]

        return (prefix, postfix, searchText, type)


    def formQuestion(self, question : str, hasFlags : boolean):
        formedQ = ""
        flag_text = ""

        posSt = question.find(' ')
        posEnd = question.find('-')
        formedQ = self.cutStringPart(question,True, posSt,posEnd)

        while(hasFlags and posEnd != -1):
            question = question[(posEnd+1):]
            posSt = question.find(' ')
            posEnd = question.find('-')

            if(question[0] == 's'):
                formedQ += ':' + self.cutStringPart(question,True, posSt,posEnd)
            if(question[0] == 'f'):
                flag_text = self.cutStringPart(question,False, posSt,posEnd)

        return (formedQ, flag_text)


    def cutStringPart(self, s: str, replaceSpace:bool, start:int, end:int):
        res = ''
        s = s[start+1:]
        
        if(end == -1):
            res = s
        else:
            res = s[:(end-1-start)]

        res = res.strip()
        if replaceSpace:
            res = res.replace(' ', '-')
        return res