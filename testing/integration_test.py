import DataP_library
import unittest
from prettytable import PrettyTable

class TestAddAnalyzer(unittest.TestCase):
    def setUp(self):
        DataP_library.data = [('a', '1', '1', 'gg'), ('b', 'True', 'False', 'False'), ('c', 'test1', 'test2', ''), ('d', '1', '2', '3')]
        DataP_library.collectColumnInfo()

    def test_Size(self):
        addAnalyzer = DataP_library.AddAnalyzer()
        addAnalyzer.Size()
        testTable = PrettyTable(["entity", "instance", "name", "value", "quarantine"])
        testTable.add_row(["Dataset", "*", "Size", 3, "*"])
        self.assertEqual(addAnalyzer.table.get_string(), testTable.get_string())
    
    def test_Completeness(self):  
        addAnalyzer = DataP_library.AddAnalyzer()
        addAnalyzer.Completeness("b")
        addAnalyzer.Completeness("c")
        testTable = PrettyTable(["entity", "instance", "name", "value", "quarantine"])
        testTable.add_row(["Column", "b", "Completeness", "3/3", "*"])
        testTable.add_row(["Column", "c", "Completeness", "2/3", "*"])
        self.assertEqual(addAnalyzer.table.get_string(), testTable.get_string())

    def test_CountDistinct(self):
        addAnalyzer = DataP_library.AddAnalyzer()
        addAnalyzer.CountDistinct("a")
        testTable = PrettyTable(["entity", "instance", "name", "value", "quarantine"])
        testTable.add_row(["Column", "a", "Distinct", 2, "*"])
        self.assertEqual(addAnalyzer.table.get_string(), testTable.get_string())

    def test_StandardDeviation(self):
        addAnalyzer = DataP_library.AddAnalyzer()
        addAnalyzer.StandardDeviation("a")
        addAnalyzer.StandardDeviation("d")
        testTable = PrettyTable(["entity", "instance", "name", "value", "quarantine"])
        testTable.add_row(["Column", "a", "Standard Deviation", 0.0, "'row 3': 'gg'"])
        testTable.add_row(["Column", "d", "Standard Deviation", 0.8165, None])
        self.assertEqual(addAnalyzer.table.get_string(), testTable.get_string())

    def test_Maximun(self):
        addAnalyzer = DataP_library.AddAnalyzer()
        addAnalyzer.Maximun("a")
        addAnalyzer.Maximun("b")
        testTable = PrettyTable(["entity", "instance", "name", "value", "quarantine"])
        testTable.add_row(["Column", "a", "Maximun", 1.0, "'row 3': 'gg'"])
        testTable.add_row(["Error", "main component is non-numeric", "Maximun", "*", "*"])
        self.assertEqual(addAnalyzer.table.get_string(), testTable.get_string())

    def test_Minimun(self):
        addAnalyzer = DataP_library.AddAnalyzer()
        addAnalyzer.Minimun("d")
        addAnalyzer.Minimun("b")
        testTable = PrettyTable(["entity", "instance", "name", "value", "quarantine"])
        testTable.add_row(["Column", "d", "Minimun", 1.0, None])
        testTable.add_row(["Error", "main component is non-numeric", "Minimun", "*", "*"])
        self.assertEqual(addAnalyzer.table.get_string(), testTable.get_string())

    def test_Mean(self):
        addAnalyzer = DataP_library.AddAnalyzer()
        addAnalyzer.Mean("d")
        addAnalyzer.Mean("b")
        testTable = PrettyTable(["entity", "instance", "name", "value", "quarantine"])
        testTable.add_row(["Column", "d", "Mean", 2.0, None])
        testTable.add_row(["Error", "main component is non-numeric", "Mean", "*", "*"])
        self.assertEqual(addAnalyzer.table.get_string(), testTable.get_string())

    def test_Distance(self):
        DataP_library.collectColumnInfo()
        addAnalyzer = DataP_library.AddAnalyzer()
        addAnalyzer.Distance("a")
        addAnalyzer.Distance("b")
        addAnalyzer.Distance("z")
        testTable = PrettyTable(["entity", "instance", "name", "value", "quarantine"])
        testTable.add_row(["Column", "a", "Distance", 0.0, "'row 3': 'gg'"])
        testTable.add_row(["Error", "main component is non-numeric", "Distance", "*", "*"])
        testTable.add_row(["Error", "z" + " not found", "Distance", "*", "*"])
        self.assertEqual(addAnalyzer.table.get_string(), testTable.get_string())

class TestAddCheck(unittest.TestCase):
    def setUp(self):
        DataP_library.data = [('a', '1', '1', 'gg'), ('b', 'True', 'False', 'False'), ('c', 'test1', 'test2', ''), ('d', '1', '2', '-3')]
        DataP_library.collectColumnInfo()

    def test_Size(self):
        addCheck = DataP_library.AddCheck()
        addCheck.hasSize(3)
        addCheck.hasSize(2)
        testTable = PrettyTable(["check", "column name", "constraint", "constraint_status", "constraint_message"])
        testTable.add_row(["Is data size = " + "3", "*", "Size", "Success", ""])
        testTable.add_row(["Is data size = " + "2", "*", "Size", "Fail", "Size = " + "3"])
        self.assertEqual(addCheck.table.get_string(), testTable.get_string())
    
    def test_hasDataType(self):
        addCheck = DataP_library.AddCheck()
        addCheck.hasDataType("b", "Boolean")
        addCheck.hasDataType("c", "Number")
        addCheck.hasDataType("z", "String")
        testTable = PrettyTable(["check", "column name", "constraint", "constraint_status", "constraint_message"])
        testTable.add_row([".hasDataType(\"" + "b" + "\", " + "Boolean" + ")", "b", "DataType", "Success", ""])
        testTable.add_row([".hasDataType(\"" + "c" + "\", " + "Number" + ")", "c", "DataType", "Fail", "DataType = " + "String"])
        testTable.add_row([".hasDataType" + "(\"" + "z" + "\")", "z", "DataType", "Error", "column (" + "z" + ") " + "not found"])
        self.assertEqual(addCheck.table.get_string(), testTable.get_string())

    def test_isComplete(self):
        addCheck = DataP_library.AddCheck()
        addCheck.isComplete("a")
        addCheck.isComplete("c")
        testTable = PrettyTable(["check", "column name", "constraint", "constraint_status", "constraint_message"])
        testTable.add_row([".isComplete(\"" + "a" + "\")", "a", "Completeness", "Success", ""])
        testTable.add_row([".isComplete(\"" + "c" + "\")", "c", "Completeness", "Fail", "Empty row: " + "3"])
        self.assertEqual(addCheck.table.get_string(), testTable.get_string())
  
    def test_isUnique(self):
        addCheck = DataP_library.AddCheck()
        addCheck.isUnique("b")
        addCheck.isUnique("c")
        testTable = PrettyTable(["check", "column name", "constraint", "constraint_status", "constraint_message"])
        testTable.add_row([".isUnique(\"" + "b" + "\")", "b", "Unique", "Fail", "nonunique row: " + "3"])
        testTable.add_row([".isUnique(\"" + "c" + "\")", "c", "Unique", "Success", ""])
        self.assertEqual(addCheck.table.get_string(), testTable.get_string())

    def test_isNonNegative(self):
        addCheck = DataP_library.AddCheck()
        addCheck.isNonNegative("a")
        addCheck.isNonNegative("d")
        testTable = PrettyTable(["check", "column name", "constraint", "constraint_status", "constraint_message"])
        testTable.add_row([".isNonNegative(\"" + "a" + "\")", "a", "NonNegative", "Success", ""])
        testTable.add_row([".isNonNegative(\"" + "d" + "\")", "d", "NonNegative", "Fail", "negative row: " + "3"])
        self.assertEqual(addCheck.table.get_string(), testTable.get_string())

    def test_isContainedIn(self):
        addCheck = DataP_library.AddCheck()
        addCheck.isContainedIn("b", ["True", "False"])
        addCheck.isContainedIn("c", ["test1"])
        testTable = PrettyTable(["check", "column name", "constraint", "constraint_status", "constraint_message"])
        testTable.add_row([".isContainedIn(\"" + "b" + "\", " + str(["True", "False"]) + ")", "b", "ContainedIn", "Success", ""])
        testTable.add_row([".isContainedIn(\"" + "c" + "\", " + str(["test1"]) + ")", "c", "ContainedIn", "Fail", "nonContain row: " + "[2, 3]".replace("[", "", 1).replace("]", "", 1)])
        self.assertEqual(addCheck.table.get_string(), testTable.get_string())

if __name__ == '__main__':
    unittest.main()
