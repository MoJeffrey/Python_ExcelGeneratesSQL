from xlutils.copy import copy


class WriteExcel:
    _Sheet = None
    _Excel = None
    _Path = None

    def __init__(self, ExcelObject, Path):
        self._Excel = copy(ExcelObject)
        self._Sheet = self._Excel.get_sheet(0)
        self._Path = Path

    def Save(self):
        self._Excel.save(self._Path)
        return

    def AddData(self, x, y, Data):
        self._Sheet.write(x, y, Data)
        return
