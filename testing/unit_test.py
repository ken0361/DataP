import DataP_library
import unittest

class TestCommand(unittest.TestCase):
    def test_isEnd(self):
        command = DataP_library.Command("end")
        self.assertTrue(command.isEnd())
        command = DataP_library.Command("exit")
        self.assertTrue(command.isEnd())
        command = DataP_library.Command("left")
        self.assertFalse(command.isEnd())
    
    def test_isLegalInput(self):
        command = DataP_library.Command("load file.txt")
        self.assertTrue(command.isLegalInput())
        command = DataP_library.Command("load")
        self.assertFalse(command.isLegalInput())
        command = DataP_library.Command("insert file.txt")
        self.assertFalse(command.isLegalInput())
    
    def test_isLoadData(self):
        command = DataP_library.Command("load file.txt")
        self.assertTrue(command.isLoadData())
        command = DataP_library.Command("load file.csv")
        self.assertTrue(command.isLoadData())
        command = DataP_library.Command("load file.html")
        self.assertFalse(command.isLoadData())
        command = DataP_library.Command("insert file.txt")
        self.assertFalse(command.isLoadData())
   
    def test_isLoadAnalyzer(self):
        command = DataP_library.Command("load analyzer.py")
        self.assertTrue(command.isLoadAnalyzer())
        command = DataP_library.Command("load analyzer.txt")
        self.assertFalse(command.isLoadAnalyzer())
        command = DataP_library.Command("insert analyzer.py")
        self.assertFalse(command.isLoadAnalyzer())
   
    def test_isLoadCheck(self):
        command = DataP_library.Command("load check.py")
        self.assertTrue(command.isLoadCheck())
        command = DataP_library.Command("load check.txt")
        self.assertFalse(command.isLoadCheck())
   
    def test_isLoadSuggestions(self):
        command = DataP_library.Command("load suggestion")
        self.assertTrue(command.isLoadSuggestions())
        command = DataP_library.Command("load suggestions")
        self.assertTrue(command.isLoadSuggestions())
        command = DataP_library.Command("load suggest")
        self.assertFalse(command.isLoadSuggestions())

class TestAddAnalyzer(unittest.TestCase):
    def test_findColNum(self):
        addAnalyzer = DataP_library.AddAnalyzer()
        DataP_library.data = [('a', '1', '2', '3'), ('b', '4', '5', '6')]
        self.assertEqual(addAnalyzer.findColNum('a'), 0)
        self.assertEqual(addAnalyzer.findColNum('d'), -1)

    def test_num(self):
        addAnalyzer = DataP_library.AddAnalyzer()
        self.assertEqual(addAnalyzer.num(""), 0)
        self.assertEqual(addAnalyzer.num("1"), 1)
        self.assertEqual(addAnalyzer.num("1.1"), 1.1)
        self.assertEqual(addAnalyzer.num("-1"), -1)
        self.assertEqual(addAnalyzer.num("-1.1"), -1.1)

    def test_caculateSD(self):
        addAnalyzer = DataP_library.AddAnalyzer()
        DataP_library.data = [('a', '1', '1', '1'), ('b', '1', '2', '3')]
        self.assertEqual(addAnalyzer.caculateSD(0), 0)
        self.assertEqual(addAnalyzer.caculateSD(1), 0.8165)

    def test_columnIllegal(self):
        addAnalyzer = DataP_library.AddAnalyzer()
        self.assertFalse(addAnalyzer.columnIllegal("column name", 5, "name"))
        self.assertTrue(addAnalyzer.columnIllegal("column name", -1, "name"))

    def test_columnNotNum(self):
        addAnalyzer = DataP_library.AddAnalyzer()
        colInfo = { "type" : "Number"}
        DataP_library.columnInfo.append(colInfo)
        colInfo = { "type" : "Number (Integer)"}
        DataP_library.columnInfo.append(colInfo)
        colInfo = { "type" : "String"}
        DataP_library.columnInfo.append(colInfo)

        self.assertFalse(addAnalyzer.columnNotNum("column name", 0, "name"))
        self.assertFalse(addAnalyzer.columnNotNum("column name", 1, "name"))
        self.assertTrue(addAnalyzer.columnNotNum("column name", 2, "name"))

class TestAddCheck(unittest.TestCase):
    def test_findColNum(self):
        addCheck = DataP_library.AddCheck()
        DataP_library.data = [('a', '1', '2', '3'), ('b', '4', '5', '6')]
        self.assertEqual(addCheck.findColNum('a'), 0)
        self.assertEqual(addCheck.findColNum('d'), -1)

    def test_columnIllegal(self):
        addCheck = DataP_library.AddCheck()
        self.assertFalse(addCheck.columnIllegal("column name", 5, "name"))
        self.assertTrue(addCheck.columnIllegal("column name", -1, "name"))

class TestCollectColInfo(unittest.TestCase):
    def setUp(self):
        DataP_library.data = [('a', '1', '1', 'gg'), ('b', 'True', 'False', 'False'), ('c', 'test1', 'test2', '')]

    def test_updateDataInfo(self):
        #('a', '1', '1', 'gg')
        colInfo1 = {
            "size" : 0,
            "number" : 0,
            "integer" : 0,
            "boolean" : 0,
            "string" : 0,
            "null" : 0,
            "nullRow": [],
            "positive" : 0,
            "negativeRow" : [],
            "maxLen" : 0,
            "minLen" : 0,
            "distinct" : None,
            "distinctValue" : None,
            "nonUniqueRow": [],
            "type" : None,
            "cleanedCol" : [],
            "quarantine": None
        }
        DataP_library._updateDataInfo(colInfo1, 0)
        self.assertEqual(colInfo1.get("number"), 2)
        self.assertEqual(colInfo1.get("integer"), 2)
        self.assertEqual(colInfo1.get("positive"), 2)
        self.assertEqual(colInfo1.get("string"), 1)
        #('b', 'True', 'False', 'False')
        colInfo2 = {
            "size" : 0,
            "number" : 0,
            "integer" : 0,
            "boolean" : 0,
            "string" : 0,
            "null" : 0,
            "nullRow": [],
            "positive" : 0,
            "negativeRow" : [],
            "maxLen" : 0,
            "minLen" : 0,
            "distinct" : None,
            "distinctValue" : None,
            "nonUniqueRow": [],
            "type" : None,
            "cleanedCol" : [],
            "quarantine": None
        }
        DataP_library._updateDataInfo(colInfo2, 1)
        self.assertEqual(colInfo2.get("boolean"), 3)
        self.assertEqual(colInfo2.get("null"), 0)
        self.assertEqual(colInfo2.get("string"), 0)
        #('c', 'test1', 'test2', '')
        colInfo3 = {
            "size" : 0,
            "number" : 0,
            "integer" : 0,
            "boolean" : 0,
            "string" : 0,
            "null" : 0,
            "nullRow": [],
            "positive" : 0,
            "negativeRow" : [],
            "maxLen" : 0,
            "minLen" : 0,
            "distinct" : None,
            "distinctValue" : None,
            "nonUniqueRow": [],
            "type" : None,
            "cleanedCol" : [],
            "quarantine": None
        }
        DataP_library._updateDataInfo(colInfo3, 2)
        self.assertEqual(colInfo3.get("string"), 2)
        self.assertEqual(colInfo3.get("null"), 1)
        self.assertEqual(colInfo3.get("nullRow"), [3])

    def test_updateColType(self):
        #('a', '1', '1', 'gg')
        colInfo = {
            "size" : 0,
            "number" : 0,
            "integer" : 0,
            "boolean" : 0,
            "string" : 0,
            "null" : 0,
            "nullRow": [],
            "positive" : 0,
            "negativeRow" : [],
            "maxLen" : 0,
            "minLen" : 0,
            "distinct" : None,
            "distinctValue" : None,
            "nonUniqueRow": [],
            "type" : None,
            "cleanedCol" : [],
            "quarantine": None
        }
        DataP_library._updateDataInfo(colInfo, 0)
        DataP_library._updateColType(colInfo)
        self.assertEqual(colInfo.get("type"), "Number (Integer)")
        #('b', 'True', 'False', 'False')
        colInfo = {
            "size" : 0,
            "number" : 0,
            "integer" : 0,
            "boolean" : 0,
            "string" : 0,
            "null" : 0,
            "nullRow": [],
            "positive" : 0,
            "negativeRow" : [],
            "maxLen" : 0,
            "minLen" : 0,
            "distinct" : None,
            "distinctValue" : None,
            "nonUniqueRow": [],
            "type" : None,
            "cleanedCol" : [],
            "quarantine": None
        }
        DataP_library._updateDataInfo(colInfo, 1)
        DataP_library._updateColType(colInfo)
        self.assertEqual(colInfo.get("type"), "Boolean")
        #('c', 'test1', 'test2', '')
        colInfo = {
            "size" : 0,
            "number" : 0,
            "integer" : 0,
            "boolean" : 0,
            "string" : 0,
            "null" : 0,
            "nullRow": [],
            "positive" : 0,
            "negativeRow" : [],
            "maxLen" : 0,
            "minLen" : 0,
            "distinct" : None,
            "distinctValue" : None,
            "nonUniqueRow": [],
            "type" : None,
            "cleanedCol" : [],
            "quarantine": None
        }
        DataP_library._updateDataInfo(colInfo, 2)
        DataP_library._updateColType(colInfo)
        self.assertEqual(colInfo.get("type"), "String")

    def test_updateQuarantine(self):
        colInfo = {
            "size" : 0,
            "number" : 0,
            "integer" : 0,
            "boolean" : 0,
            "string" : 0,
            "null" : 0,
            "nullRow": [],
            "positive" : 0,
            "negativeRow" : [],
            "maxLen" : 0,
            "minLen" : 0,
            "distinct" : None,
            "distinctValue" : None,
            "nonUniqueRow": [],
            "type" : None,
            "cleanedCol" : [],
            "quarantine": None
        }
        #('a', '1', '1', 'gg')
        DataP_library._updateDataInfo(colInfo, 0)
        DataP_library._updateColType(colInfo)
        DataP_library._updateQuarantine(colInfo, 0, "number")
        self.assertEqual(colInfo.get("cleanedCol"), ['1', '1'])
        self.assertEqual(colInfo.get("quarantine"), "'row 3': 'gg'")

    def test_updateDistinct(self):
        colInfo = {
            "size" : 0,
            "number" : 0,
            "integer" : 0,
            "boolean" : 0,
            "string" : 0,
            "null" : 0,
            "nullRow": [],
            "positive" : 0,
            "negativeRow" : [],
            "maxLen" : 0,
            "minLen" : 0,
            "distinct" : None,
            "distinctValue" : None,
            "nonUniqueRow": [],
            "type" : None,
            "cleanedCol" : [],
            "quarantine": None
        }
        DataP_library._updateDistinct(colInfo, 0)
        self.assertEqual(colInfo.get("nonUniqueRow"), [2])
        self.assertEqual(colInfo.get("distinctValue"), ['1', 'gg'])

if __name__ == '__main__':
    unittest.main()
