from difflib import Match
import requests
import re
from googlesearch import search
from typing import List

from tableMaker import TableMaker

class Sage:
    
    def __init__(self):
        self.wiki_adress = "http://dnd5e.wikidot.com/"
        pass

    def askQuestion(self,questionCategory:str, question:str):
        response = self.getHttp(self.wiki_adress, questionCategory + ":" + question)
        if(response.status_code == 200):
            response = self.cutOutInfo(response.text)
            response += ( "Source: " + self.wiki_adress + questionCategory + ":" + question )
        else:
            response = self.getFailAnswer('Error code ' + str(response.status_code))

        return response

    def askExpandedQuestion(self,questionCategory:str, question:str, searchPhrase:str):
        response = self.getHttp(self.wiki_adress ,questionCategory + ":" + question)

        if(response.status_code == 200):
            if(searchPhrase == ""):
                response = self.cutOutInfo(response.text)
            else:
                respParts = self.findOccuernces(searchPhrase,response.text)
                response = ""
                index = 1
                for rP in respParts:
                    response += "***Match found no."+str(index)+":***\n" + self.cutOutInfo(rP) + "\n\n"
                    index += 1
            response += ( "Source: " + self.wiki_adress + questionCategory + ":" + question )
        else:
            response =  self.getFailAnswer('Error code ' + str(response.status_code))

        return response

    def findOccuernces(self, phrase:str, source_str:str) -> List[str]:
        findingsList = []
        anchor = '<h'

        positionsFound = re.finditer(phrase,source_str,re.I)        
        
        pF_Copy = re.finditer(phrase,source_str,re.I)
        count = 0
        for match in pF_Copy:
            count +=1

        if count == 0:
            findingsList.append("**Unfortunately, there was no matches for your search**")
        elif count > 10:
            findingsList.append("**Unfortunately, there was to many matches for your search, try to specify your search a little bit more**")
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
        return ('There is nothing like this in my all-knowing book! ( Reason: ' + reason + ' )')


    def askSearchQuestion(self, question:str, searchPhrase:str):
        adress = self.searchInGoogleEngine(question)
        
        response = self.getHttp(adress,"")

        if(response.status_code == 200):
            if(searchPhrase == ""):
                response = self.cutOutInfo(response.text)
            else:
                respParts = self.findOccuernces(searchPhrase,response.text)
                response = ""
                index = 1
                for rP in respParts:
                    response += "***Match found no."+str(index)+":***\n" + self.cutOutInfo(rP) + "\n\n"
                    index += 1  
            response += ( "Source: " + adress)
        else:
            response = ('There is nothing like this in my all-knowing book! ( error code: ' + str(response.status_code) + ')')

        return response

    def getHttp(self,adress:str, subadress:str):  
        y = requests.get(adress + subadress)
        return y

    def searchInGoogleEngine(self, query:str):
        query = query + " wikidot"
        #for first_http_adress in search(query, tld="co.in", num=1, stop=1, pause=2):
        #int: num_results=10, str: lang="en"
        # for first_http_adress in search(query, 1, 'en'):
        for first_http_adress in search(query, tld="co.in", num=1, stop=1, pause=3):
            return first_http_adress


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


    def cutOutInfo(self,textHtml):
        #cut out everything before interesting part
        pos = textHtml.find('<div id="page-content">')
        tx = ""
        if pos != -1: 
            tx = textHtml[pos:]
        else:
            tx = textHtml

        title = self.getTitle(textHtml)

        #cut out everything after interesting part
        # pos = tx.find('<!-- wikidot_bottom')
        pos = re.search("<div id=\"wad-dnd5e-below-content\"", tx)
        if pos:
            tx = tx[:pos.start()]
        else:         
            pos = re.search("<[\w\d\s=,\"-]*footer", tx)
            if pos:
                tx = tx[:pos.start()]

        #remove all empty lines
        tx = "".join([s for s in tx.strip().splitlines(True) if s.strip()])

        #search and edit tables
        regTab = re.compile("<table[\w\d\s\n\W]+?<\/table>")         #"(<table)|(<\/table>)")
        
        posTable = re.search(regTab, tx)
        tableMaker = None
        if(posTable):
            tableMaker = TableMaker()
        while(posTable):    
            #cut table form text and leave text without it
            cuttedTab = tx[posTable.start():] + tx[:posTable.end()]                 
            tx = tx[:posTable.start()] + tx[posTable.end():] 
            #cuttedTab = tablemaker...   make table biutiful
            cuttedTab = "\n\n```fix\n" +  tableMaker.createUnicodeTable(cuttedTab) + "```\n\n" 
            tx = tx[:posTable.start()] + cuttedTab + tx[posTable.start() + 1:] #SUS should be start + tab+ start i think
            #put in right position of the tx a new butiful table
            posTable = re.search(regTab, tx)

        tx = self.boldTextHeaders(tx)

        reg0 = re.compile("<\/p>")
        #reg1 = re.compile('(<\w+>)|(<\/[\w\s\/]+>)|(<.+>)')
        reg1 = re.compile("<[\/\w\d\s\n\W]+?>")
        
        #relpace end-of-paragraph symbols with new line
        tx = re.sub(reg0, "\n", tx)
        #remove all html related syntax (<something>)
        tx = re.sub(reg1, "", tx)

        tx = re.sub('\n{3,}', '\n\n', tx)

        return (title + tx)