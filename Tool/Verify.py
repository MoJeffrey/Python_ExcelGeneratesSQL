class Verify:

    @staticmethod
    def VerifyData(Name, Type, Address, Phone, TypeList: dict = None):
        """
        驗證數據的正確性
        避免生成的SQL 出錯
        :return:
        """
        if TypeList is None:
            TypeList = []
        IsOK, Msg = Verify.VerifyName(Name)
        if not IsOK:
            return IsOK, Msg

        # IsOK, Msg = Verify.VerifyType(Type, TypeList)
        # if not IsOK:
        #     return IsOK, Msg

        IsOK, Msg = Verify.VerifyAddress(Address)
        if not IsOK:
            return IsOK, Msg

        IsOK, Msg = Verify.VerifyPhone(Phone)
        if not IsOK:
            return IsOK, Msg
        return True, ""

    @staticmethod
    def VerifyName(Name):
        """
        驗證名稱
        :return:
        """
        if Name == "":
            return False, "名稱不可為空"

        return True, ""

    @staticmethod
    def VerifyType(Type, TypeList):
        """
        驗證類別
        :param Type:
        :param TypeList:
        :return:
        """
        if Type is []:
            return False, "類別不可為空"

        for Item in Type:
            if Item not in list(TypeList.keys()):
                return False, "該類別不存在"

        return True, ""

    @staticmethod
    def VerifyAddress(Address):
        """
        驗證地址
        :param Address:
        :return:
        """
        if Address == "":
            return False, "地址不可為空"

        return True, ""

    @staticmethod
    def VerifyPhone(Phone):
        """
        驗證手機號碼
        :param Phone:
        :return:
        """
        if Phone == "":
            return False, "手機號碼不可為空"

        Phone = Phone.replace(" ", "").replace("+852", "").replace(".", "")
        if not Phone.isdigit():
            return False, "電話不可包涵非數字字符"

        return True, ""
