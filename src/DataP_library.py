import os.path
import math
import sys
import statistics
from prettytable import PrettyTable

global data, columnInfo
data = []
columnInfo = []

class Command:
    def __init__(self, userInput):
        self.command = userInput
        self.commands = self.command.split(" ")

    def readFile(self):
        global data
        data = []
        filename = self.commands[1]
        if not os.path.isfile(filename):
            print(filename + ' does not exist')
        else:
            with open(filename) as fobj:
                for line in fobj:
                    row = [x.strip() for x in line.split(',')]
                    data.append(row)

            data = list(zip(*[(row) for row in data]))

    def isLegalInput(self):
        if len(self.commands) == 2 and self.commands[0] == "load":
            return True
        else:
            return False

    def isEnd(self):
        if self.command == "end" or self.command == "exit":
            return True
        else:
            return False

    def isLoadData(self):
        if self.isLegalInput() and\
        (".txt" in self.commands[1] or ".csv" in self.commands[1]):
            return True
        else:
            return False
    
    def isLoadAnalyzer(self):
        if self.isLegalInput() and "analyzer.py" in self.commands[1]:
            return True
        else:
            return False

    def isLoadCheck(self):
        if self.isLegalInput() and "check.py" in self.commands[1]:
            return True
        else:
            return False

    def isLoadSuggestions(self):
        if self.isLegalInput() and "suggestion" in self.commands[1]:
            return True
        else:
            return False

    def loadAnalyzer(self):
        if data == []:
            print("Error: no data, please load a file")
        else:
            if not os.path.isfile("analyzer.py"):
                print('analyzer.py does not exist')
                return
            exec(open("analyzer.py").read())

    def loadCheck(self):
        if data == []:
            print("Error: no data, please load a file")
        else:
            if not os.path.isfile("check.py"):
                print('check.py does not exist')
                return
            exec(open("check.py").read())

class AddAnalyzer:
    def __init__(self):
        self.table = PrettyTable(["entity", "instance", "name", "value", "quarantine"])
   
    def Size(self):
        self.table.add_row(["Dataset", "*", "Size", len(data[0])-1, "*"])

    def Completeness(self, columnName):
        colNum = self.findColNum(columnName)
        if self.columnIllegal(columnName, colNum, "Completeness"): return
        completeness = str(columnInfo[colNum].get("size")-columnInfo[colNum].get("null")) +\
        "/" + str(columnInfo[colNum].get("size"))
        self.table.add_row(["Column", columnName, "Completeness", completeness, "*"])

    def CountDistinct(self, columnName):
        colNum = self.findColNum(columnName)
        if self.columnIllegal(columnName, colNum, "Distinct"): return
        self.table.add_row(["Column", columnName, "Distinct", columnInfo[colNum].get("distinct"), "*"])

    def Correlation(self, columnName1, columnName2):
        colNum1 = self.findColNum(columnName1)
        colNum2 = self.findColNum(columnName2)

        if self.columnIllegal(columnName1, colNum1, "Correlation"): return
        elif self.columnIllegal(columnName2, colNum2, "Correlation"): return
        elif self.columnNotNum(columnName1, colNum1, "Correlation"): return
        elif self.columnNotNum(columnName2, colNum2, "Correlation"): return

        avg1 = statistics.mean(float(n) for n in columnInfo[colNum1].get("cleanedCol"))
        avg2 = statistics.mean(float(n) for n in columnInfo[colNum2].get("cleanedCol"))
        tmp = 0
        for i in range(1, len(data[colNum1])):
            tmp = tmp + (self.num(data[colNum1][i])-avg1)*(self.num(data[colNum2][i])-avg2)
        cov = tmp/(len(data[colNum2])-1)
        try:
            sd1 = statistics.pstdev(float(n) for n in columnInfo[colNum1].get("cleanedCol"))
            sd2 = statistics.pstdev(float(n) for n in columnInfo[colNum2].get("cleanedCol"))
            r = round(cov/(sd1*sd2), 4)
            self.table.add_row(["Column", columnName1+", "+columnName2, "Correlation", r])
        except ZeroDivisionError:
            self.table.add_row(["Column", columnName1+", "+columnName2, "Correlation", 0.0])

    def StandardDeviation(self, columnName):
        colNum = self.findColNum(columnName)
        if self.columnIllegal(columnName, colNum, "Standard Deviation"): return
        elif self.columnNotNum(columnName, colNum, "Standard Deviation"): return
        sd = round(statistics.pstdev(float(n) for n in columnInfo[colNum].get("cleanedCol")), 4)
        self.table.add_row(["Column", columnName, "Standard Deviation", sd, columnInfo[colNum].get("quarantine")])

    def Maximun(self, columnName):
        colNum = self.findColNum(columnName)
        if self.columnIllegal(columnName, colNum, "Maximun"): return
        elif self.columnNotNum(columnName, colNum, "Maximun"): return
        maxNum = max(float(n) for n in columnInfo[colNum].get("cleanedCol"))
        self.table.add_row(["Column", columnName, "Maximun", maxNum, columnInfo[colNum].get("quarantine")])

    def Minimun(self, columnName):
        colNum = self.findColNum(columnName)
        if self.columnIllegal(columnName, colNum, "Minimun"): return
        elif self.columnNotNum(columnName, colNum, "Minimun"): return
        minNum = min(float(n) for n in columnInfo[colNum].get("cleanedCol"))
        self.table.add_row(["Column", columnName, "Minimun", minNum, columnInfo[colNum].get("quarantine")])

    def Mean(self, columnName):
        colNum = self.findColNum(columnName)
        if self.columnIllegal(columnName, colNum, "Mean"): return
        elif self.columnNotNum(columnName, colNum, "Mean"): return
        mean = round(statistics.mean(float(n) for n in columnInfo[colNum].get("cleanedCol")), 4)
        self.table.add_row(["Column", columnName, "Mean", mean, columnInfo[colNum].get("quarantine")])

    def DataType(self, columnName):
        colNum = self.findColNum(columnName)
        if self.columnIllegal(columnName, colNum, "DataType"): return
        self.table.add_row(["Column", columnName, "DataType", columnInfo[colNum].get("type"), "*"])

    def Distance(self, columnName):
        colNum = self.findColNum(columnName)
        if self.columnIllegal(columnName, colNum, "Distance"): return
        elif self.columnNotNum(columnName, colNum, "Distance"): return
        distance = max(float(n) for n in columnInfo[colNum].get("cleanedCol")) - min(float(n) for n in columnInfo[colNum].get("cleanedCol"))
        self.table.add_row(["Column", columnName, "Distance", distance, columnInfo[colNum].get("quarantine")])

    def run(self):
        print(self.table)
        
    #Help functions

    def findColNum(self, columnName):
        for i in range(0, len(data)):
            if data[i][0] == columnName:
                return i
        return -1

    def num(self, s):
        if s == "":
            return 0
        try:
            return int(s)
        except ValueError:
            return float(s)

    def caculateSD(self, colNum):
        global data
        sum = 0
        sum_square = 0
        for i in range(1, len(data[colNum])):
            sum = sum + self.num(data[colNum][i])
            sum_square = sum_square + pow(self.num(data[colNum][i]), 2)

        avg = sum/(len(data[colNum])-1)
        avg_square = sum_square/(len(data[colNum])-1)
        
        # because of binary error from float
        try:
            SD = round(math.sqrt(avg_square - pow(avg, 2)), 4)
            return SD
        except ValueError:
            return 0

    def columnIllegal(self, columnName, colNum, name):
        if colNum == -1:
            self.table.add_row(["Error", columnName + " not found", name, "*", "*"])
            return True
        else:
            return False

    def columnNotNum(self, columnName, colNum, name):
        if "Number" in columnInfo[colNum].get("type"):
            return False
        else:
            self.table.add_row(["Error", "main component is non-numeric", name, "*", "*"])
            return True

class AddCheck:
    def __init__(self):
        self.table = PrettyTable(["check", "column name", "constraint", "constraint_status", "constraint_message"])
    
    def hasSize(self, sizeNum):
        if sizeNum == len(data[0])-1:
            self.table.add_row(["Is data size = " + str(sizeNum), "*", "Size", "Success", ""])
        else:
            size = str(len(data[0])-1)
            self.table.add_row(["Is data size = " + str(sizeNum), "*", "Size", "Fail", "Size = " + size])
        
    def hasDataType(self, columnName, dataType):
        colNum = self.findColNum(columnName)
        if self.columnIllegal(columnName, colNum, "DataType"): return
        if dataType in columnInfo[colNum].get("type"):
            if columnInfo[colNum].get("quarantine") == None:
                self.table.add_row([".hasDataType(\"" + columnName + "\", " + dataType + ")", columnName, "DataType", "Success", ""])
            else:
                self.table.add_row([".hasDataType(\"" + columnName + "\", " + dataType + ")", columnName, "DataType", "Fail", columnInfo[colNum].get("quarantine")])
        else:
            self.table.add_row([".hasDataType(\"" + columnName + "\", " + dataType + ")", columnName, "DataType", "Fail", "DataType = " + columnInfo[colNum].get("type")])
    
    def isComplete(self, columnName):
        colNum = self.findColNum(columnName)
        if self.columnIllegal(columnName, colNum, "Completeness"): return
        if columnInfo[colNum].get("null") == 0:
            self.table.add_row([".isComplete(\"" + columnName + "\")", columnName, "Completeness", "Success", ""])
        else:
            emptyRow = str(columnInfo[colNum].get("nullRow")).replace("[", "", 1).replace("]", "", 1)
            self.table.add_row([".isComplete(\"" + columnName + "\")", columnName, "Completeness", "Fail", "Empty row: " + emptyRow])

    def isUnique(self, columnName):
        colNum = self.findColNum(columnName)
        if self.columnIllegal(columnName, colNum, "Unique"): return
        if columnInfo[colNum].get("nonUniqueRow") == []:
            self.table.add_row([".isUnique(\"" + columnName + "\")", columnName, "Unique", "Success", ""])
        else:
            nonUniqueRow = str(columnInfo[colNum].get("nonUniqueRow")).replace("[", "", 1).replace("]", "", 1)
            self.table.add_row([".isUnique(\"" + columnName + "\")", columnName, "Unique", "Fail", "nonunique row: " + nonUniqueRow])

    def isNonNegative(self, columnName):
        colNum = self.findColNum(columnName)
        if self.columnIllegal(columnName, colNum, "NonNegative"): return
        if columnInfo[colNum].get("negativeRow") == []:
            self.table.add_row([".isNonNegative(\"" + columnName + "\")", columnName, "NonNegative", "Success", ""])
        else:
            negativeRow = str(columnInfo[colNum].get("negativeRow")).replace("[", "", 1).replace("]", "", 1)
            self.table.add_row([".isNonNegative(\"" + columnName + "\")", columnName, "NonNegative", "Fail", "negative row: " + negativeRow])

    def isContainedIn(self, columnName, array):
        colNum = self.findColNum(columnName)
        nonContain = []
        if self.columnIllegal(columnName, colNum, "ContainedIn"): return
        for j in range(1, len(data[colNum])):
            if data[colNum][j] not in array:
                nonContain.append(j)
        if nonContain == []:
            self.table.add_row([".isContainedIn(\"" + columnName + "\", " + str(array) + ")", columnName, "ContainedIn", "Success", ""])
        else:
            self.table.add_row([".isContainedIn(\"" + columnName + "\", " + str(array) + ")", columnName, "ContainedIn", "Fail", "nonContain row: " + str(nonContain).replace("[", "", 1).replace("]", "", 1)])

    def run(self):
        print(self.table)

    #Help functions

    def findColNum(self, columnName):
        global data
        for i in range(0, len(data)):
            if data[i][0] == columnName:
                return i
        return -1
    
    def columnIllegal(self, columnName, colNum, name):
        if name == "DataType":
            head = ".has"
        else:
            head = ".is"
        if colNum == -1:
            self.table.add_row([head + name + "(\"" + columnName + "\")", columnName, name, "Error", "column (" + columnName + ") " + "not found"])
            return True
        else:
            return False


def printLogo():
    logo ="""
 welcome  _____        _        _____  
         |  __ \      | |      |  __ \ 
         | |  | | __ _| |_ __ _| |__) |
         | |  | |/ _` | __/ _` |  ___/ 
         | |__| | (_| | || (_| | |     
         |_____/ \__,_|\__\__,_|_|    version 3.0
                              
 DataP, a data quality tool developed based on Deequ, 
 provides a constraints suggestion system and a Python library 
 to perform anomaly detection to dataset.
 The commands contain:
 1. load dataset_name (to load dataset into DataP)
 2. load analyzer.py  (to execute the analysis program)
 3. load suggestion   (to execute auto constraints suggestion)
 4. load check.py     (to execute anomaly detection)
       """
    print(logo)

def printTypeInMark():
    print("DataP> ", end="")

def showRoot():
    if data == []:
        return
    print("root")
    for i in range(len(data)):
        for j in range(len(data[i])):
            if j == 0:
                print("|-- "+data[i][j]+": ", end="")
                print(columnInfo[i].get("type"))

def createAnalyzerTemplate():
    library = "from DataP_library import *\n\naddAnalyzer = AddAnalyzer()\n\n\"\"\"\n"
    example1 = "Edit addAnalyzer functions here:\naddAnalyzer.Size()\naddAnalyzer.Completeness(\"column_name\")\n"
    example2 = "addAnalyzer.CountDistinct(\"column_name\")\naddAnalyzer.DataType(\"column_name\")\n"
    run = "\"\"\"\n\naddAnalyzer.run()\n"
    code = library + example1 + example2 + run
    f = open("analyzer.py", "w")
    f.write(code)
    f.close()

#collect colum information

def collectColumnInfo():
    global columnInfo
    columnInfo = []

    for i in range(len(data)):
        colInfo = {
            "size" : len(data[i]) - 1,
            "number" : 0,
            "integer" : 0,
            "boolean" : 0,
            "string" : 0,
            "null" : 0,
            "nullRow": [],
            "positive" : 0,
            "negativeRow" : [],
            "maxLen" : len(max(data[i][1:len(data[i])], key=len)),
            "minLen" : len(min(data[i][1:len(data[i])], key=len)),
            "distinct" : None,
            "distinctValue" : None,
            "nonUniqueRow": [],
            "type" : None,
            "cleanedCol" : [],
            "quarantine": None
        }

        _updateDataInfo(colInfo, i)
        _updateColType(colInfo)
        _updateDistinct(colInfo, i)
        if "Number" in colInfo.get("type"):
            _updateQuarantine(colInfo, i, "number")
        elif "Boolean" in colInfo.get("type"):
            _updateQuarantine(colInfo, i, "boolean")

        columnInfo.append(colInfo)

def _updateDataInfo(colInfo, i):
    for j in range(1, len(data[i])):
        if data[i][j] == "":
            colInfo["null"] += 1
            colInfo["nullRow"].append(j)
        elif any(item in data[i][j] for item in ["T", "F", "True", "False"]):
            colInfo["boolean"] += 1
        elif data[i][j].replace('.','',1).replace('-','',1).isdigit():
            colInfo["number"] += 1
            if "." not in data[i][j]:
                colInfo["integer"] += 1
            if "-" not in data[i][j]:
                colInfo["positive"] += 1
            else:
                colInfo["negativeRow"].append(j)
        else:
            colInfo["string"] += 1

def _updateColType(colInfo):
    mostValueType = max(colInfo.get("number"), colInfo.get("boolean"), colInfo.get("string"))
    if colInfo.get("number") == mostValueType and\
    colInfo.get("integer") == colInfo.get("number"):
        colInfo["type"] = "Number (Integer)"
    elif colInfo.get("number") == mostValueType:
        colInfo["type"] = "Number"
    elif colInfo.get("boolean") == mostValueType:
        colInfo["type"] = "Boolean"
    elif colInfo.get("string") == mostValueType:
        colInfo["type"] = "String"
    else:
        colInfo["type"] = "Inconsistent"

def _updateQuarantine(colInfo, i, colType):
    if(colInfo.get("size") == colInfo.get(colType)):
        colInfo["cleanedCol"] = list(data[i][1:len(data)])
        return
    
    cleanedCol = list(data[i])
    cleanedCol.pop(0)
    quarantine = dict()
    
    if colType == "number":
        for j in range(1, len(data[i])):
            if not data[i][j].replace('.','',1).replace('-','',1).isdigit():
                quarantine["row "+str(j)] = data[i][j]
                cleanedCol.remove(data[i][j])
    elif colType == "boolean":
        for j in range(1, len(data[i])):
            if not any(item in data[i][j] for item in ["T", "F", "True", "False"]):
                quarantine["row "+str(j)] = data[i][j]
                cleanedCol.remove(data[i][j])

    colInfo["cleanedCol"] = cleanedCol
    colInfo["quarantine"] = str(quarantine).replace('{','',1).replace('}','',1)

def _updateDistinct(colInfo, i):
    distinct = []
    for j in range(1, len(data[i])):
        if data[i][j] not in distinct:
                distinct.append(data[i][j])
        else:
            colInfo["nonUniqueRow"].append(j)

    colInfo["distinct"] = len(distinct)
    if len(distinct) < 5:
        colInfo["distinctValue"] = distinct

# auto constraints suggestion

def constraintSuggestions():
    global columnInfo
    if data == []:
        print("error: no data, please load a file")
        return
    
    table = PrettyTable(["column", "suggestted constraint"])
    ratio = 0.9
    code = "from DataP_library import *\n\naddCheck = AddCheck()\n\n"

    for i in range(len(columnInfo)):
        if 1-(columnInfo[i].get("null")/columnInfo[i].get("size")) >= ratio:
            table.add_row([data[i][0], ".isComplete(\"" + data[i][0] + "\")"])
            code = code + "addCheck.isComplete(\"" + data[i][0] + "\")\n"
        if columnInfo[i].get("positive")/columnInfo[i].get("size") >= ratio:
            table.add_row([data[i][0], ".isNonNegative(\"" + data[i][0] + "\")"])
            code = code + "addCheck.isNonNegative(\"" + data[i][0] + "\")\n"
        if columnInfo[i].get("distinct")/columnInfo[i].get("size") >= ratio:
            table.add_row([data[i][0], ".isUnique(\"" + data[i][0] + "\")"])
            code = code + "addCheck.isUnique(\"" + data[i][0] + "\")\n"
        if columnInfo[i].get("integer")/columnInfo[i].get("size") >= ratio:
            table.add_row([data[i][0], ".hasDataType(\"" + data[i][0] + "\", \"Integer\")"])
            code = code + "addCheck.hasDataType(\"" + data[i][0] + "\", \"Integer\")\n"
        elif columnInfo[i].get("number")/columnInfo[i].get("size") >= ratio:
            table.add_row([data[i][0], ".hasDataType(\"" + data[i][0] + "\", \"Number\")"])
            code = code + "addCheck.hasDataType(\"" + data[i][0] + "\", \"Number\")\n"
        if columnInfo[i].get("boolean")/columnInfo[i].get("size") >= ratio:
            table.add_row([data[i][0], ".hasDataType(\"" + data[i][0] + "\", \"Boolean\")"])
            code = code + "addCheck.hasDataType(\"" + data[i][0] + "\", \"Boolean\")\n"
        if columnInfo[i].get("type") == "String" and columnInfo[i].get("distinct") < 5:
            table.add_row([data[i][0], ".isContainedIn(\"" + data[i][0] + "\", " + str(columnInfo[i].get("distinctValue")) + ")"])
            code = code + "addCheck.isContainedIn(\"" + data[i][0] + "\", " + str(columnInfo[i].get("distinctValue")) + ")\n"
    
    code = code + "#add other addCheck functions\n"
    code = code + "\naddCheck.run()\n"
    f = open("check.py", "w")
    f.write(code)
    f.close()
    print(table)
        


