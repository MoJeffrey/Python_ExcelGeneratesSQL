import json

import requests


class GoogleMap:
    _Address = None
    _lat = None
    _lng = None

    def __init__(self, Address):
        self._Address = Address
        self._Search()
        pass

    def _Search(self):
        """
        根據地址搜索相關坐標
        :return:
        """
        URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
        Key = "AIzaSyB3xovzODcvJn4K_r6XHClToK--x2b2Uf4"
        fields = "geometry"
        inputtype = "textquery"

        URL += f"key={Key}&"
        URL += f"fields={fields}&"
        URL += f"inputtype={inputtype}&"
        URL += f"input={self._Address}&"

        response = requests.get(URL).text
        Data = json.loads(response)
        print(f"查詢地址：{self._Address}")
        print(Data)
        if Data['status'] == "ZERO_RESULTS":
            self._lat = "22.323973"
            self._lng = "114.118063"
        else:
            Data = Data['candidates'][0]['geometry']
            self._lat = Data['location']['lat']
            self._lng = Data['location']['lng']

    def GetCoordinate(self):
        return self._lat, self._lng


if __name__ == '__main__':
    GoogleMap("油麻地彌敦道577號高氏大樓6樓B號舖")
