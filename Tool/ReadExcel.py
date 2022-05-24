import xlrd


class ReadExcel:
    _Sheet = None
    _Excel = None

    def __init__(self, FileName):
        self._Excel = xlrd.open_workbook(FileName)
        self._Sheet = self._Excel.sheets()[0]

    def GetRow(self):
        return self._Sheet.nrows

    def GetRowData(self, Row):
        return self._Sheet.row_values(Row)

    def GetExcelObject(self):
        return self._Excel
