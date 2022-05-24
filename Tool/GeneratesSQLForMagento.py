import hashlib


class GeneratesSQLForMagento:
    _Email = None
    _Password = None

    def __init__(self):
        pass

    def CreateUser(self, Email, Password, is_active=1):
        """
        添加 Magento2.4 內置用戶
        :param Email:
        :param Password:
        :param is_active:
        :return:
        """
        self._Email = Email
        self._Password = Password

        # customer_entity 表
        Columns = {
            "website_id": 1,
            "email": Email,
            "group_id": 1,
            "store_id": 1,
            "is_active": is_active,
            "disable_auto_group_change": 0,
            "created_in": "English",
            "firstname": "New",
            "lastname": "User",
            "password_hash": self._GetHashPassword(),
            "failures_num": 0
        }

        return GeneratesSQLForMagento._GetSQLInsert("customer_entity", Columns)

    @staticmethod
    def CreateLoginUser(Name, Phone, Email):
        """
        添加登入用戶的資料 Mo_customer_entity 表
        :return: 
        """
        Columns = {
            "entity_id": "@EntityId",
            "Name": Name,
            "Phone": Phone,
            "Email": Email,
        }

        return GeneratesSQLForMagento._GetSQLInsert("Mo_customer_entity", Columns)

    @staticmethod
    def CreateMerchant(Name, Address, Phone):
        """
        添加商戶信息 `marketplace_userdata` 表
        :return:
        """
        Columns = {
            "is_seller": "1",
            "seller_id": "@EntityId",
            "tw_active": "0",
            "fb_active": "0",
            "gplus_active": "0",
            "youtube_active": "0",
            "vimeo_active": "0",
            "instagram_active": "0",
            "pinterest_active": "0",
            "moleskine_active": "0",
            "shop_url": Name.replace("@", ""),
            "shop_title": Name.replace("@", ""),
            "company_locality": Address,
            "store_id": "1",
            "contact_number": Phone,
            "admin_notification": "0",
            "company_latitude": "22.323973",
            "company_longitude": "114.118063"
        }
        return GeneratesSQLForMagento._GetSQLInsert("marketplace_userdata", Columns)

    @staticmethod
    def CreateType(Type):
        """
        添加類別到商家中
        :param Type:
        :return:
        """
        SQL = f"SELECT @TypeID:=id FROM `MerchantType` WHERE `Name` = '{Type}';"

        Columns = {
            "entity_id": "@EntityId",
            "MerchantType_id": "@TypeID"
        }
        SQL += GeneratesSQLForMagento._GetSQLInsert("MerchantType_entity", Columns)
        return SQL

    @staticmethod
    def SQLSetEntityId(Email):
        """
        設置EntityId
        方便後續的操作
        e.g Del or Add
        :param Email:
        :return:
        """
        SQL = f"SELECT @EntityId:=entity_id FROM `customer_entity` WHERE `email`='{Email}';"
        return SQL

    @staticmethod
    def DelUser():
        """
        刪除Magento2.4 系統內置的customer_entity表
        :return:
        """
        SQL = f"DELETE FROM `customer_entity` WHERE `entity_id`= @EntityId;"
        return SQL

    @staticmethod
    def DelLoginUser():
        """
        刪除自寫登入插件 Mo_customer_entity 表
        :return:
        """
        SQL = "DELETE FROM `Mo_customer_entity` WHERE `entity_id`= @EntityId;"
        return SQL

    @staticmethod
    def DelMerchant():
        """
        刪除多商戶插件內的商戶資料 marketplace_userdata 表
        :return:
        """
        SQL = "DELETE FROM `marketplace_userdata` WHERE `seller_id`= @EntityId;"
        return SQL

    @staticmethod
    def DelMerchantType():
        """
        删除商户类别 MerchantType_entity表
        :return:
        """
        SQL = "DELETE FROM `MerchantType_entity` WHERE `entity_id`=@EntityId;"
        return SQL

    @staticmethod
    def UpdateMerchant(lat, lng):
        """
        marketplace_userdata

        company_latitude
        company_longitude
        商戶修改坐標
        :return:
        """
        Update = {
            "company_latitude": lat,
            "company_longitude": lng
        }

        WHERE = {
            "seller_id": "@EntityId"
        }

        return GeneratesSQLForMagento._GetSQLUpdate('marketplace_userdata', Update, WHERE)

    @staticmethod
    def _GetSQLInsert(Table: str, Columns: dict):
        """
        給予要添加的Column
        傳出mysql 添加語句中的Columns
        :param Columns:
        :param Table: 表名
        :return:
        """
        SQL = f"INSERT IGNORE INTO `{Table}`"

        ColumnSQL = "("
        ValueSQL = "("
        for Key, Value in Columns.items():
            ColumnSQL += f"`{Key}`,"
            Value = GeneratesSQLForMagento._String(Value)
            if "@" in str(Value) and ".com" not in str(Value):
                ValueSQL += f"{Value},"
            else:
                ValueSQL += f"'{Value}',"

        SQL += f"{ColumnSQL[:-1]}) VALUES {ValueSQL[:-1]});"
        return SQL

    @staticmethod
    def _GetSQLUpdate(Table: str, Update: dict, WHERE: dict):
        """
        傳回mysql更新語句
        :param Table:
        :param Update:
        :param WHERE:
        :return:
        """
        SQL = f"UPDATE `{Table}` SET"

        UpdateSQL = ""
        for Key, Value in Update.items():
            UpdateSQL += f"`{Key}`='{Value}',"

        WhereSQL = ""
        for Key, Value in WHERE.items():
            Value = GeneratesSQLForMagento._String(Value)

            if "@" in str(Value) and ".com" not in str(Value):
                WhereSQL += f"`{Key}`={Value},"
            else:
                WhereSQL += f"`{Key}`='{Value}',"

        return f"{SQL} {UpdateSQL[:-1]} WHERE {WhereSQL[:-1]};"

    def _GetHashPassword(self):
        """
        给予Hash后的密码字串
        :return:
        """
        m = hashlib.md5()
        m.update(self._Password.encode("utf8"))
        return m.hexdigest() + "::0"

    @staticmethod
    def _String(s):
        """
        字符串轉譯
        :param s:
        :return:
        """
        return str(s).replace("'", "\\'")
