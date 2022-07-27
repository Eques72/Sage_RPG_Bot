import requests
import re
from googlesearch import search
from typing import List
import tableMaker as tM

class Sage:
    
    __searchPhraseBase = " wikidot dnd"
    __wikiWebAdress = "http://dnd5e.wikidot.com/"
    __failAnswers = ["Error code:", "**Unfortunately, there was no matches for your search**", "**Unfortunately, there was to many matches for your search, try to specify your search a little bit more**"]

    def __init__(self, clientStatus : str):
        self.clientStatus = clientStatus
        pass


    def askQuestion(self,questionCategory:str, question:str):
        response = self.getHttp(Sage.__wikiWebAdress, questionCategory + ":" + question)

        if(response.status_code == 200):
            response = self.preprareAnswer(response.text)
            response += ( "Source: " + Sage.__wikiWebAdress + questionCategory + ":" + question )
        else:
            response = self.getFailAnswer(Sage.__failAnswers[0] + str(response.status_code))

        return response


    def askExpandedQuestion(self,questionCategory:str, question:str, searchPhrase:str):
        response = self.getHttp(Sage.__wikiWebAdress ,questionCategory + ":" + question)

        return self.deepQuestionProcess(response, searchPhrase)


    def askSearchQuestion(self, question:str, searchPhrase:str):
        adress = self.searchInGoogleEngine(question)
        response = self.getHttp(adress,"")

        return self.deepQuestionProcess(response, searchPhrase)


    def deepQuestionProcess(self, response: str, searchPhrase:str):
        url = response.url
        if(response.status_code == 200 and url.find("wikidot") != -1):
            if(searchPhrase == ""):
                response = self.preprareAnswer(response.text)
            else:
                respParts = self.findOccuernces(searchPhrase,response.text)
                response = ""
                index = 1
                for rP in respParts:
                    response += "***Match found no."+str(index)+":***\n" + self.preprareAnswer(rP) + "\n\n"
                    index += 1  
            response += ( "Source: " + url )

        else:
            response = self.getFailAnswer(Sage.__failAnswers[0] + str(response.status_code))

        return response


    def getHttp(self,adress:str, subadress:str):  
        y = requests.get(adress + subadress)
        return y


    def searchInGoogleEngine(self, query:str):
        query = query + Sage.__searchPhraseBase
        for first_http_adress in search(query, tld="co.in", num=1, stop=1, pause=3):
            return first_http_adress


    def findOccuernces(self, phrase:str, source_str:str) -> List[str]:
        findingsList = []
        anchor = '<h'

        source_body = self.cutOutPortion(source_str)
        source_str = "<h>" + self.getTitle(source_str) + "<h>" + source_body

        positionsFound = re.finditer(phrase,source_str,re.I)        
        
        pF_Copy = re.finditer(phrase,source_str,re.I)
        count = 0
        for match in pF_Copy:
            count +=1

        if count == 0:
            findingsList.append(self.getFailAnswer(Sage.__failAnswers[1]))
        elif count > 10:
            findingsList.append(Sage.__failAnswers[2])
        else:
            allPositions = [] #to ensure unique resoults
            for pF in positionsFound:
                posAn = source_str.rfind(anchor,0,pF.start())
                posAnEnd = source_str.find(anchor,pF.start())
                
                if (posAn, posAnEnd) not in allPositions:
                    allPositions.append((posAn, posAnEnd))
                    finding = source_str[posAn:posAnEnd]
                    finding = re.sub(phrase, "__"+pF.group(0)+"__",finding,0,re.I)
                    findingsList.append(finding)

        return findingsList


    def getFailAnswer(self, reason='404'):
        return ('There is nothing like this in my all-knowing book! ( Reason:' + reason + ')')


    def getTitle(self, textHtml):
        regTitle = re.compile("(?<=<title>)(.*?)(?=<\/title>)")
        title = re.search(regTitle, textHtml)
        
        if isinstance(title, re.Match):
            title = "**" + title.group(0) + "**\n"
        else: 
            title = ""
 
        return title


    def boldTextHeaders(self, text):
        regSpan = re.compile("((<span[\w\s\d=\"-:%;]*>)|(<\/span>))")
        
        text = re.sub(regSpan,"**",text)
        return text


    def cutOutPortion(self, text):
        #cut out everything before interesting part
        pos = text.find('<div id="page-content">')
        tx = ""
        if pos != -1: 
            tx = text[pos:]
        else:
            tx = text

        #cut out everything after interesting part
        pos = re.search("<div id=\"wad-dnd5e-below-content\"", tx)
        if pos:
            tx = tx[:pos.start()]
        else:         
            pos = re.search("<[\w\d\s=,\"-]*footer", tx)
            if pos:
                tx = tx[:pos.start()]
        return tx


    def findAndMakeTables(self, text : str):
        #search and make tables
        regTab = re.compile("<table[\w\d\s\n\W]+?<\/table>")
        
        posTable = re.search(regTab, text)
        tMaker = None
        if(posTable):
            tMaker = tM.TableMaker(self.clientStatus)
        while(posTable):    
            #cut table form text and leave text without it
            cuttedTab = text[posTable.start():] + text[:posTable.end()]                 
            text = text[:posTable.start()] + text[posTable.end():] 

            #let table maker prepare a table and put it back in text
            cuttedTab = "\n\n```fix\n" +  tMaker.createUnicodeTable(cuttedTab) + "```\n\n" 
            text = text[:posTable.start()] + cuttedTab + text[posTable.start() + 1:]
           
            #search for any others html tables
            posTable = re.search(regTab, text)       
        return text


    def preprareAnswer(self,textHtml):
        
        tx = self.cutOutPortion(textHtml)
        title = self.getTitle(textHtml)

        #remove all empty lines
        tx = "".join([s for s in tx.strip().splitlines(True) if s.strip()])

        tx = self.findAndMakeTables(tx)

        tx = self.boldTextHeaders(tx)

        reg0 = re.compile("<\/p>")
        reg1 = re.compile("<[\/\w\d\s\n\W]+?>")
        
        #relpace end-of-paragraph symbols with new line
        tx = re.sub(reg0, "\n", tx)
        #remove all html related syntax (<something>)
        tx = re.sub(reg1, "", tx)
        #remove and reduce blocks of new-lines
        tx = re.sub('\n{3,}', '\n\n', tx)

        return (title + tx)