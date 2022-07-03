import pandas as pd

class TableMaker:
    def __init__(self) -> None:
        self.MAX_WIDTH = 89 #80
        self.HORIZONTAL_CHAR = '═'
        self.VERTICAL_CHAR = '║'
        self.CROSS_CHAR = '╬'
        pass 

    #use only for multiindex
    def prepareColumnsNames(self, columnsData):
        colTab = []

        max_siz = 1
        for c in columnsData:
             if(max_siz < len(c)):
                max_siz = len(c)

        for i in range(0,max_siz):
            colSet = []
            for j in range(0,len(columnsData)):
                if(len(columnsData[j]) >= i):
                    if(columnsData[j][i] not in colSet):
                        colSet.append(columnsData[j][i])
                else:
                    tmp_str = "Empty_cell: " + str(i)
                    colSet.append(tmp_str)
            colTab.append(colSet)

        return colTab


    def calculateCellSize(self, length:int):
        separoators = 2 + length - 1
        cell_size = (self.MAX_WIDTH-separoators-((self.MAX_WIDTH-separoators)%separoators)) / length
        cell_size = int(cell_size)
        return cell_size


    def makeHorizontalEdge(self, cells_amount:int, cell_size:int, target_str:str):
        for i in range(0,cells_amount):       #+----------+---------+--------+
            target_str += self.CROSS_CHAR
            for j in range(0, cell_size):
                target_str += self.HORIZONTAL_CHAR
        target_str += self.CROSS_CHAR + '\n'
        return target_str


    def makeVerticalContent(self, columns, cell_size:int, empty_cell:str, target_str:str):
        multiline_content = []
        max_width = 1
        for head in columns:
            head_multi = []
            while(len(head) > cell_size):
                head_multi.append(head[:cell_size])
                head = head[cell_size:]
            while(len(head) < cell_size):
                head += ' '
            head_multi.append(head)
            if(len(head_multi) > max_width):
                max_width = len(head_multi)
            multiline_content.append(head_multi)

        for i in range(0,max_width):
            for j in range(0,len(multiline_content)):
                target_str += self.VERTICAL_CHAR
                if(len(multiline_content[j])-1 >= i):
                    target_str += multiline_content[j][i]
                else:
                    target_str += empty_cell
            target_str += self.VERTICAL_CHAR + '\n'
        
        return target_str


    #only one table at the time
    def createUnicodeTable(self, content:str):
        data = pd.read_html(content)[0]

        if isinstance(data.columns, pd.MultiIndex):
            uni_table = self.createTableForMultiindex(data)
        else:
            uni_table = self.createTableForIndex(data)

        return uni_table    
    

    def makeTablePart(self, column, isEnding:bool, targetTable:str):
        cell_size = self.calculateCellSize(len(column))
        tablePart = ""
        #make empty cell content
        empty_cell = ""
        for i in range(0, cell_size):
            empty_cell += ' '

        tablePart = self.makeHorizontalEdge(len(column), cell_size, tablePart)
        tablePart = self.makeVerticalContent(column, cell_size, empty_cell, tablePart)

        if(isEnding):
            tablePart = self.makeHorizontalEdge(len(column), cell_size, tablePart)            
        return targetTable + tablePart

    def createTableForIndex(self, data):
        data4Cells = data.values
        col = data.columns

        table = ""
        table = self.makeTablePart(col,False,table)

        #for cells in data4Cells:
        for c in range(0, len(data4Cells)):
            for i in range(0, len( data4Cells[c] ) ):
                if isinstance(data4Cells[c][i], str):
                    pass
                else:
                    data4Cells[c][i] = str(data4Cells[c][i])
            
            if c == len(data4Cells) - 1:
                table = self.makeTablePart(data4Cells[c],True, table)
            else:
                table = self.makeTablePart(data4Cells[c],False, table)
        
        return table   


    def createTableForMultiindex(self, data):
        data4Cells = data.values
        colNames = data.columns

        colNames = self.prepareColumnsNames(colNames)

        table = ""

        for col in colNames:
            table = self.makeTablePart(col,False, table)
        
        for c in range(0, len(data4Cells)):
            for i in range(0, len( data4Cells[c] ) ):
                if isinstance(data4Cells[c][i], str):
                    pass
                else:
                    data4Cells[c][i] = str(data4Cells[c][i])
            
            if c == len(data4Cells) - 1:
                table = self.makeTablePart(data4Cells[c],True, table)
            else:
                table = self.makeTablePart(data4Cells[c],False, table)

        return table   