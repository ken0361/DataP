from DataP_library import *

printLogo()
createAnalyzerTemplate()

while(True):
    printTypeInMark()

    command = Command(input())

    if command.isEnd(): break
    elif command.isLoadData():
        command.readFile()
        collectColumnInfo()
        showRoot()
    elif command.isLoadAnalyzer():
        command.loadAnalyzer()
    elif command.isLoadCheck():
        command.loadCheck()
    elif command.isLoadSuggestions():
        constraintSuggestions()
    


