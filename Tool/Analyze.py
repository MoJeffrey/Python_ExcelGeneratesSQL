class Analyze:
    """
    解析數據
    """

    _Data = None
    _Phone = None
    _Name = None
    _Address = None
    _Type = None

    def __init__(self, Data):
        self._Data = Data
        self._Name = str(self._Data[0])
        self._Address = str(self._Data[3])
        self._Phone = str(self._Data[4])
        self._Type = str(self._Data[1])
        self._Type = self._Type.split(" ")
        self._Type = [x for x in self._Type if x != '']
        return

    def GetPhone(self):
        return self._Phone

    def GetName(self):
        return self._Name

    def GetType(self):
        return self._Type

    def GetAddress(self):
        return self._Address

    def AnalyzePhone(self):
        """
        解析電話號
        :return:
        """
        return self._Phone.replace("+852", "").replace(" ", "")[0:8]

    def AnalyzeType(self, TypeList: dict):
        """
        取消沒有的類別
        :param TypeList:
        :return:
        """
        Items = []
        for Item in self._Type:
            if Item in list(TypeList.keys()):
                Items.append(Item)

        return Items
