from Tool.GoogleMap import GoogleMap
from Tool.ReadExcel import ReadExcel
from Tool.GeneratesSQLForMagento import GeneratesSQLForMagento
from Tool.Verify import Verify
from Tool.Analyze import Analyze
from Tool.WriteExcel import WriteExcel

TypeList = {
    "餐廳": "ct",
    "美容": "mr",
    "活動": "hd",
    "獸醫": "sy",
    "寵物食品商店": "sw",
    "寵物用品商店": "yp",
    "好去處": "hqc",
    "寵物課程": "kc",
    "領養及義工": "ly",
    "寵物訓練": "xl",
    "其他寵物服務": "qt"
}
Password = "123456"


def Create():
    File = "data.xlsx"
    NewFile = "NewData.xls"

    MySQLFile = open("Add.sql", "w+", encoding="utf-8")
    ErrorFile = open("Error.log", "w+", encoding="utf-8")

    RE = ReadExcel(File)
    WE = WriteExcel(RE.GetExcelObject(), NewFile)
    WE.AddData(0, 6, "賬號/錯誤提示")
    WE.AddData(0, 7, "密碼")

    GeneratesSQL = GeneratesSQLForMagento()
    for Num in range(1, RE.GetRow()):
        Data = Analyze(RE.GetRowData(Num))
        Phone = Data.GetPhone()
        Name = Data.GetName()
        Address = Data.GetAddress()
        Type = Data.GetType()

        # 手機號不符合規格則0
        IsOK, Msg = Verify.VerifyPhone(Phone)
        if not IsOK:
            Phone = "0"

        # 地址不符合規格則 "暫無地址"
        IsOK, Msg = Verify.VerifyAddress(Address)
        if not IsOK:
            Address = "暫無地址"

        # 取消沒有的類別
        IsOK, Msg = Verify.VerifyType(Type, TypeList)
        if not IsOK:
            Type = Data.AnalyzeType(TypeList)

        IsOK, Msg = Verify.VerifyData(Name, Type, Address, Phone, TypeList)
        if IsOK:
            # 名稱
            if len(Type) >= 1:
                UserName = TypeList[Type[0]] + str(Num).zfill(5)
            else:
                UserName = f"my{str(Num).zfill(5)}"

            # Email
            if Phone == "0":
                Email = UserName + "@User.com"
                Phone = UserName
            else:
                Email = Data.AnalyzePhone() + "@User.com"
                Phone = Data.AnalyzePhone()

            SQL = GeneratesSQL.CreateUser(Email, Password)
            SQL += GeneratesSQL.SQLSetEntityId(Email)
            SQL += GeneratesSQL.CreateLoginUser(UserName, Phone, Email)
            SQL += GeneratesSQL.CreateMerchant(Name, Address, Data.GetPhone())
            for Item in Type:
                SQL += GeneratesSQL.CreateType(Item)

            print(f"# 第{Num + 1}行: {Email}", file=MySQLFile)
            print(SQL, file=MySQLFile)

            WE.AddData(Num, 6, UserName)
            WE.AddData(Num, 7, Password)

        else:
            print(f"# 第{Num + 1}行: {Msg}", file=ErrorFile)
            print(RE.GetRowData(Num), file=ErrorFile)

            WE.AddData(Num, 6, Msg)

    WE.Save()

def Del():
    File = "data.xlsx"
    MySQLFile = open("Del.sql", "w+", encoding="utf-8")
    ErrorFile = open("Error.log", "w+", encoding="utf-8")
    RE = ReadExcel(File)
    GeneratesSQL = GeneratesSQLForMagento()
    for Num in range(1, RE.GetRow()):
        Data = Analyze(RE.GetRowData(Num))
        Phone = Data.GetPhone()
        Name = Data.GetName()
        Address = Data.GetAddress()
        Type = Data.GetType()

        # 手機號不符合規格則0
        IsOK, Msg = Verify.VerifyPhone(Phone)
        if not IsOK:
            Phone = "0"

        # 地址不符合規格則 "暫無地址"
        IsOK, Msg = Verify.VerifyAddress(Address)
        if not IsOK:
            Address = "暫無地址"

        # 取消沒有的類別
        IsOK, Msg = Verify.VerifyType(Type, TypeList)
        if not IsOK:
            Type = Data.AnalyzeType(TypeList)

        IsOK, Msg = Verify.VerifyData(Name, Type, Address, Phone, TypeList)
        if IsOK:
            # 名稱
            if len(Type) >= 1:
                UserName = TypeList[Type[0]] + str(Num).zfill(5)
            else:
                UserName = f"my{str(Num).zfill(5)}"

            # Email
            if Phone == "0":
                Email = UserName + "@User.com"
            else:
                Email = Data.AnalyzePhone() + "@User.com"

            print(f"# 第{Num+1}行: {Email}", file=MySQLFile)
            SQL = GeneratesSQL.SQLSetEntityId(Email)
            SQL += GeneratesSQL.DelMerchantType()
            SQL += GeneratesSQL.DelMerchant()
            SQL += GeneratesSQL.DelLoginUser()
            SQL += GeneratesSQL.DelUser()
            print(SQL, file=MySQLFile)

        else:
            print(f"# 第{Num+1}行: {Msg}", file=ErrorFile)
            print(RE.GetRowData(Num), file=ErrorFile)


def UpdateMap():
    File = "data.xlsx"
    NewFile = "AddressData.xls"
    MySQLFile = open("Update.sql", "w+", encoding="utf-8")
    ErrorFile = open("Error.log", "w+", encoding="utf-8")
    RE = ReadExcel(File)
    WE = WriteExcel(RE.GetExcelObject(), NewFile)
    WE.AddData(0, 6, "lat")
    WE.AddData(0, 7, "lng")

    GeneratesSQL = GeneratesSQLForMagento()
    for Num in range(1, RE.GetRow()):
        Data = Analyze(RE.GetRowData(Num))
        Phone = Data.GetPhone()
        Name = Data.GetName()
        Address = Data.GetAddress()
        Type = Data.GetType()

        # 手機號不符合規格則0
        IsOK, Msg = Verify.VerifyPhone(Phone)
        if not IsOK:
            Phone = "0"

        # 地址不符合規格則 "暫無地址"
        IsOK, Msg = Verify.VerifyAddress(Address)
        if not IsOK:
            Address = "暫無地址"

        # 取消沒有的類別
        IsOK, Msg = Verify.VerifyType(Type, TypeList)
        if not IsOK:
            Type = Data.AnalyzeType(TypeList)

        IsOK, Msg = Verify.VerifyData(Name, Type, Address, Phone, TypeList)
        if IsOK:
            # 名稱
            if len(Type) >= 1:
                UserName = TypeList[Type[0]] + str(Num).zfill(5)
            else:
                UserName = f"my{str(Num).zfill(5)}"

            # Email
            if Phone == "0":
                Email = UserName + "@User.com"
            else:
                Email = Data.AnalyzePhone() + "@User.com"

            print(f"第{Num + 1}行")
            GM = GoogleMap(Address)
            lat, lng = GM.GetCoordinate()
            print(f"# 第{Num + 1}行: {Email}", file=MySQLFile)
            SQL = GeneratesSQL.SQLSetEntityId(Email)
            SQL += GeneratesSQL.UpdateMerchant(lat, lng)
            print(SQL, file=MySQLFile)

            WE.AddData(Num, 6, lat)
            WE.AddData(Num, 7, lng)
        else:
            print(f"# 第{Num + 1}行: {Msg}", file=ErrorFile)
            print(RE.GetRowData(Num), file=ErrorFile)

    WE.Save()


if __name__ == '__main__':
    UpdateMap()
