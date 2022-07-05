from typing import List
import pandas as pd
import re

class TableMaker:
    def __init__(self) -> None:
        self.MAX_WIDTH = 87 #80
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
                    if i == len(columnsData[j])-1 or columnsData[j][i] not in colSet :
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

    def calculateOptimalCellSize(self, cells, headers):
        col_lengths = [0] * len(cells[0])
        sum_len = 0

        for i in range(0, len(cells)):        
            for j in range(0,len(cells[i])):
                col_lengths[j] += len(cells[i][j])
                sum_len += len(cells[i][j])

        if len(cells[0]) == len(headers[len(headers)-1]):
            for j in range(0,len(headers[len(headers)-1])):
                col_lengths[j] += len(headers[len(headers)-1][j])
                sum_len += len(headers[len(headers)-1][j])

        cells_size = []
        separoators = 2 + len(cells[0]) - 1
        max_space_4_cells = self.MAX_WIDTH - separoators

        sum_cells_size = 0
        for cL in col_lengths:
            s = int(max_space_4_cells * (cL / sum_len))       
            sum_cells_size += s
            cells_size.append(s)

        for cell in cells_size:
            if cell < 2:
                difference = 2 - cell
                cells_size[cells_size.index(cell)] = 2
                tmp = max(cells_size)
                cells_size[cells_size.index(tmp)] -= difference

        # if sum_cells_size < max_space_4_cells:
        #     cells_size[len(cells_size)-1] += max_space_4_cells - sum_cells_size
        while sum_cells_size < max_space_4_cells:
            for i in range(0, ((max_space_4_cells - sum_cells_size) % len(cells_size))):
                cells_size[i] += 1
            sum_cells_size += (max_space_4_cells - sum_cells_size) % len(cells_size)
        while sum_cells_size > max_space_4_cells:
            for i in range(0, ((sum_cells_size - max_space_4_cells) % len(cells_size))):
                cells_size[i] -= 1
            sum_cells_size -= (sum_cells_size - max_space_4_cells) % len(cells_size)

        return cells_size


    def makeHorizontalEdge(self, cells_amount:int, cell_sizes, target_str:str):
        for i in range(0,cells_amount):       #+----------+---------+--------+
            target_str += self.CROSS_CHAR
            for j in range(0, cell_sizes[i]):
                target_str += self.HORIZONTAL_CHAR
        target_str += self.CROSS_CHAR + '\n'
        return target_str

    def makeRowContent(self, row, cell_sizes, target_str:str):
        multiline_content = []
        max_heigth = 1

        #wraps text to fit cell sizes and adds spaces to even the shape
        for i in range(0,len(row)):
            cell_multi_line = []
            while(len(row[i]) > cell_sizes[i]):
                cell_multi_line.append(row[i][:cell_sizes[i]])
                row[i] = row[i][cell_sizes[i]:]
            while(len(row[i]) < cell_sizes[i]):
                row[i] += ' '
            cell_multi_line.append(row[i])

            #calculates cell with most multilines (establishes row's height)
            if(len(cell_multi_line) > max_heigth):
                max_heigth = len(cell_multi_line)
            
            multiline_content.append(cell_multi_line)

        #creates actual row of the table
        for i in range(0,max_heigth):
            for j in range(0,len(multiline_content)):
                target_str += self.VERTICAL_CHAR
                if(len(multiline_content[j])-1 >= i):
                    target_str += multiline_content[j][i]
                else:
                    target_str += (" " * cell_sizes[j])
            target_str += self.VERTICAL_CHAR + '\n'
        
        return target_str


    #only one table at the time
    def createUnicodeTable(self, content:str):
        data = pd.read_html(content)[0]
        data4Cells = data.values

        data.rename(columns=lambda x: re.sub('Unnamed:[\w\s\d_]+','--',x),inplace = True)
        #convets every value to string
        for c in range(0, len(data4Cells)):
            for i in range(0, len( data4Cells[c] ) ):
                if isinstance(data4Cells[c][i], str):
                    pass
                else:
                    data4Cells[c][i] = str(data4Cells[c][i])
                data4Cells[c][i] = re.sub("^nan$", "-",data4Cells[c][i])



        cells_sizes = self.calculateOptimalCellSize(data4Cells, data.columns.values)

        if isinstance(data.columns, pd.MultiIndex):
            uni_table = self.createTableHeadForMultiindex(cells_sizes,data)
        else:
            uni_table = self.createTableHeadForIndex(cells_sizes,data)

        for c in range(0, len(data4Cells)):
            if c == len(data4Cells) - 1:
                uni_table = self.makeTablePart(data4Cells[c],cells_sizes,True, uni_table)
            else:
                uni_table = self.makeTablePart(data4Cells[c],cells_sizes,False, uni_table)
        

        return uni_table    
    

    def makeTablePart(self, row, cells_sizes, isEnding:bool, targetTable:str):
        
        if len(cells_sizes) != len(row):
            cell_size = self.calculateCellSize(len(row))
            tmp_sizes = []
            for i in range(0,len(row)):
                tmp_sizes.append(cell_size)
            cells_sizes = tmp_sizes

        tablePart = ""
    
        tablePart = self.makeHorizontalEdge(len(row), cells_sizes, tablePart)
        tablePart = self.makeRowContent(row, cells_sizes, tablePart)

        if(isEnding):
            tablePart = self.makeHorizontalEdge(len(row), cells_sizes, tablePart)            
        return targetTable + tablePart

    def createTableHeadForIndex(self,cells_sizes, data):
        col = data.columns.values

        tableHead = ""
        tableHead = self.makeTablePart(col,cells_sizes,False,tableHead)

        return tableHead   


    def createTableHeadForMultiindex(self,cells_sizes, data):
        colNames = data.columns.values

        colNames = self.prepareColumnsNames(colNames)

        table = ""
        for col in colNames:
            table = self.makeTablePart(col,cells_sizes,False, table)

        return table   