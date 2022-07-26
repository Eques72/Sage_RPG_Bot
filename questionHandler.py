import sage
from xmlrpc.client import boolean

class QuestionHandler:

    __questionTypes = ["SIMPLE","DEEP","SEARCH","HELP"]
    __failAnswers = ["Search phrase after \"-f\" flag is too short", "File missing","Command unknown"]
    __helpFileName = "helpInfo.txt"

    def __init__(self):
        pass

    def handleQuestion(self, question : str, questionCategory : str, clientStatus : str):
        s = sage.Sage(clientStatus)      
        
        question = question.lower()
        interpretationResoults = self.interpreteQuestions(question, questionCategory) 

        answer = ""
        if(interpretationResoults[3] == QuestionHandler.__questionTypes[0]):
            answer = s.askQuestion(interpretationResoults[0],interpretationResoults[1])     

        elif(interpretationResoults[3] == QuestionHandler.__questionTypes[1]):
            if len(interpretationResoults[2]) < 3 and len(interpretationResoults[2]) != 0:
                answer = s.getFailAnswer(QuestionHandler.__failAnswers[0])
            else:
                answer = s.askExpandedQuestion(interpretationResoults[0],interpretationResoults[1],interpretationResoults[2])

        elif(interpretationResoults[3] == QuestionHandler.__questionTypes[2]):
            if len(interpretationResoults[2]) < 3 and len(interpretationResoults[2]) != 0:
                answer = s.getFailAnswer(QuestionHandler.__failAnswers[0])
            else:
                answer = s.askSearchQuestion(interpretationResoults[1], interpretationResoults[2])

        elif(interpretationResoults[3] == QuestionHandler.__questionTypes[3]):
            f = open(QuestionHandler.__helpFileName, "r")
            if f.readable:
                answer = f.read()
            else:
                answer = s.getFailAnswer(QuestionHandler.__failAnswers[1])
            f.close()

        else:
            answer = s.getFailAnswer(QuestionHandler.__failAnswers[2])

        return answer
   

    def interpreteQuestions(self, question : str, questionCategory : str):
        prefix = ""
        postfix = ""
        searchText = ""
        type = ""
        data = ("","")

        if(questionCategory == "SPELL"): #simple no flags
            prefix = "spell"
            type = QuestionHandler.__questionTypes[0]
            data = self.formQuestion(question, 0)

        elif(questionCategory == "FEAT"): #simple no flags
            prefix = "feat"
            type = QuestionHandler.__questionTypes[0]
            data = self.formQuestion(question, 0)

        #sage is used to search 
        elif(questionCategory == "SAGE"): #search, with/without flags
            prefix = "sage"
            type = QuestionHandler.__questionTypes[2]
            data = self.formQuestion(question, 1) 
     
        elif(questionCategory == "CLASS"): #deep flags        
            prefix = ""
            type = QuestionHandler.__questionTypes[1]
            data = self.formQuestion(question, 1)
     
        elif(questionCategory == "RACE"): #deep flags
            prefix = "" 
            type = QuestionHandler.__questionTypes[1]
            data = self.formQuestion(question, 1)

        elif(questionCategory == "BACKGROUND"): #simple no flags
            prefix = "background" 
            type = QuestionHandler.__questionTypes[0]
            data = self.formQuestion(question, 0)

        elif(questionCategory == "HELP"): #simple no flags
            type = QuestionHandler.__questionTypes[3]
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