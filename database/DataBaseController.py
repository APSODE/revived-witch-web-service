import os

from pymongo import MongoClient, database
import json


class READ_WRITE:
    @staticmethod
    def READ_JSON(FILE_DIR: str) -> dict:
        """FILE_DIR에는 데이터를 읽어올 JSON데이터 파일 디렉토리를 입력해주세요.

        리턴
        --------
        READ_JSON(FILE_DIR = :func:`JSON_DIR`)\n
        ==> READ_USER_DATA[:func:`"KEY"`]
        """

        with open(f"{FILE_DIR}", "r", encoding = "utf-8") as READ_USER_PROFILE:
            READ_USER_DATA = json.load(READ_USER_PROFILE)
            READ_USER_PROFILE.close()

        return READ_USER_DATA  # READ_USER_DATA타입 = DICT

    @staticmethod
    def WRITE_JSON(FILE_DIR: str, JSON_DATA: dict) -> None:
        with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_USER_PROFILE:
            json.dump(JSON_DATA, WRITE_USER_PROFILE, indent = 4)


class DataBaseController:
    def __init__(self, db_name: str):
        self._account_file_dir = os.path.dirname(os.path.abspath(__file__)) + "\\mongoDB_account.json"
        # self._account = READ_WRITE.READ_JSON(FILE_DIR = self._account_file_dir).get('account')
        self._account = {
            "id": os.environ.get("id"),
            "pw": os.environ.get("pw")
        }
        self._client = MongoClient(f"mongodb+srv://{self._account.get('id')}:{self._account.get('pw')}"
                                   f"@rw-webservice-database.bbsoap3.mongodb.net/?retryWrites=true&w=majority")

        self._database = self._client.get_database(db_name)



    def AddDataToDataBase(self, collection_name: str, add_data: [dict]):
        if add_data.__len__() > 1:
            self._database.get_collection(collection_name).insert_many(add_data)
        else:
            self._database.get_collection(collection_name).insert_one(add_data[0])

    def FindDatas(self, collection_name: str, find_one: bool = False, query: dict = None):
        if find_one:
            return self._database.get_collection(collection_name).find_one(query)
        else:
            return [result for result in self._database.get_collection(collection_name).find(query)]

    @property
    def Database(self) -> database.Database:
        return self._database

if __name__ == "__main__":
    pass
    # DB_CONTROLLER = DataBaseController(db_name = )
    # test_db = DB_CONTROLLER.GetDataBase(db_name = "Test")
    # test_db.Test.insert_one({"TEST1": "TEST"})


