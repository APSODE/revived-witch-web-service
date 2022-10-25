# import os

import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from database.models.gacha_doll_model import DollData, Doll
from models.gacha_banner_model import BannerData, Banner


class DataTools:
    def __init__(self):
        self._RW_DATABASE_SITE_URL = "https://revivedwitch.kloenlansfiel.com/ko/characters"


    def _GetSiteData_HTML(self) -> BeautifulSoup:
        return BeautifulSoup(
            requests.get(url = self._RW_DATABASE_SITE_URL).text,
            "html.parser"
        )

    @staticmethod
    def _QueryGradeSelecotr(default_query: dict, grade: str) -> dict:

        for GR in ["UR", "SSR", "SR", "R"]:
            if {"GRADE": GR} in default_query["$and"]:
                default_query["$and"].remove({"GRADE": GR})
            else:
                pass

        default_query["$and"].append({"GRADE": grade})
        print(f"{grade} query : {default_query}\n\n")
        return default_query

    def GetData_DOLL(self) -> [DollData]:
        DOLL_DATA_LIST = []

        DB_SITE_HTML = self._GetSiteData_HTML()
        DOLL_ELEM_LIST = DB_SITE_HTML.select('div[id="characters"] > ul > li')

        for DOLL_ELEM in DOLL_ELEM_LIST:
            DOLL_DATA_DTO = DollData(
                NAME = DOLL_ELEM.attrs.get("data-name"),
                GRADE = DOLL_ELEM.attrs.get("data-rarity"),
                ELEMENT = DOLL_ELEM.attrs.get("data-element"),
                DOLL_CLASS = DOLL_ELEM.attrs.get("data-class"),
                LIMITED = True if DOLL_ELEM.attrs.get("data-tags") == "limited" else False
            )

            DOLL_DATA_LIST.append(DOLL_DATA_DTO.GetAllDollData())

        return DOLL_DATA_LIST

    def CreateAllDollData(self, doll_data_object_list: [DollData], collection_name: str) -> bool:
        WORK_STATUS = True
        try:
            pass
        except:
            pass


    def CreateGachaBannerData(self, element: str = None, dream: str = None, limited: str = None) -> [dict]:
        from app import database_controller
        if element is not None:
            banner_name = f"{element} 원소 소환"
            target_doll = ""

            if element == "염석":
                element_type = "Saltstone"
            elif element == "수은":
                element_type = "Mercury"
            elif element == "유황":
                element_type = "Brimstone"
            else:
                element_type = "Aether"

            query = {
                "$and": [
                    {
                        "ELEMENT": {
                            "$eq": element_type
                        }
                    },
                    {
                        "LIMITED": {
                            "$eq": False
                        }
                    },
                    {
                        "$and": [
                            {
                                "NAME": {
                                    "$ne": "아네모네"
                                }
                            },
                            {
                                "NAME": {
                                    "$ne": "유이"
                                }
                            }
                        ]
                    }
                ]
            }

        elif dream is not None:
            banner_name = "꿈의 소환"
            target_doll = dream
            query = {
                "$and": [
                    {
                        "ELEMENT": {
                            "$ne": "Aether"
                        }
                    },
                    {
                        "LIMITED": {
                            "$eq": False
                        },
                    },
                    {
                        "$and": [
                            {
                                "NAME": {
                                    "$ne": "아네모네"
                                }
                            },
                            {
                                "NAME": {
                                    "$ne": "유이"
                                }
                            }
                        ]
                    }
                ]
            }

        elif limited is not None:
            banner_name = "한정 소환"
            target_doll = limited
            query = {
                "$and": [
                    {
                        "ELEMENT": {
                            "$ne": "Aether"
                        }
                    },
                    {
                        "$and": [
                            {
                                "NAME": {
                                    "$ne": "아네모네"
                                }
                            },
                            {
                                "NAME": {
                                    "$ne": "유이"
                                }
                            }
                        ]
                    },
                    {

                        "$or": [
                            {
                                "NAME": {
                                    "$eq": "세라냐"
                                }
                            },
                            {
                                "LIMITED": {
                                    "$eq": False
                                }
                            }
                        ]
                    }
                ]
            }

        else:
            banner_name = "영혼 소환"
            target_doll = ""
            query = {
                "$and": [
                    {
                        "ELEMENT": {
                            "$ne": "Aether"
                        }
                    },
                    {
                        "LIMITED": {
                            "$eq": False
                        }
                    },
                    {
                        "NAME": {
                            "$ne": "유이"
                        }
                    }
                ]
            }


        gacha_banner_data = {
            "banner_name": banner_name,
            "pick_up": {
                "active": True if dream is not None or limited is not None else False,
                "target": target_doll
            },
            "summonable_doll": {
                "UR": database_controller.FindDatas(
                    collection_name = "Doll",
                    query = self._QueryGradeSelecotr(default_query = query, grade = "UR")
                ),
                "SSR": database_controller.FindDatas(
                    collection_name = "Doll",
                    query = self._QueryGradeSelecotr(default_query = query, grade = "SSR")
                ),
                "SR": database_controller.FindDatas(
                    collection_name = "Doll",
                    query = self._QueryGradeSelecotr(default_query = query, grade = "SR")
                ),
                "R": database_controller.FindDatas(
                    collection_name = "Doll",
                    query = self._QueryGradeSelecotr(default_query = query, grade = "R")
                ),
            },
            "probability": {
                "UR": 2,
                "SSR": 8,
                "SR": 40,
                "R": 50
            }
        }

        database_controller.AddDataToDataBase(collection_name = "GachaBanner", add_data = [gacha_banner_data])

    @staticmethod
    def AddNewDoll(DOLL_DTO: DollData) -> bool:
        from app import database_controller
        error_count = 0
        try:
            database_controller.AddDataToDataBase(
                collection_name = "Doll",
                add_data = [
                    DOLL_DTO.GetAllDollData()
                ]
            )

        except Exception as MSG:
            print("인형 데이터 추가중에 문제 발생")
            print(MSG)
            error_count += 1

        finally:
            if error_count == 0:
                return True
            else:
                return False

    @staticmethod
    def DatabaseDollDataSerializer(database_doll_data: dict) -> dict:
        RT_DICT = {
            "NAME": database_doll_data.get("NAME"),
            "GRADE": database_doll_data.get("GRADE"),
            "ELEMENT": database_doll_data.get("ELEMENT"),
            "DOLL_CLASS": database_doll_data.get("DOLL_CLASS"),
            "LIMITED": database_doll_data.get("LIMITED")
        }

        return RT_DICT

    @staticmethod
    def DatabaseBanneDataSerializer(database_banner_data: dict) -> dict:
        RT_DICT = {
            "BANNER_NAME": database_banner_data.get("BANNER_NAME"),
            "PICK_UP_DATA": database_banner_data.get("PICK_UP_DATA"),
            "PROBABILITY": database_banner_data.get("PROBABILITY")
        }

        return RT_DICT

    @staticmethod
    def GetDollDataByDollName(doll_name: str) -> DollData:
        from app import database_controller
        doll_db_data = database_controller.FindDatas(
            collection_name = "Doll",
            query = {"NAME": doll_name},
            find_one = True
        )

        doll_object = Doll.SerializeData(
            target_data = DataTools.DatabaseDollDataSerializer(
                database_doll_data = doll_db_data
            )
        )

        return doll_object

    @staticmethod
    def GetBannerDataByBannerName(banner_name: str) -> BannerData:
        from app import database_controller
        banner_db_data = database_controller.FindDatas(
            collection_name = "GachaBanner",
            query = {"banner_name": banner_name},
            find_one = True
        )

        banner_object = Banner.SerializeData(
            target_data = DataTools.DatabaseBanneDataSerializer(
                database_banner_data = banner_db_data
            )
        )

        return banner_object
    # @staticmethod
    # def SaveDataInLocalFile(save_file_path: str = None) -> None:
    #     if save_file_path is not None:
    #         pass
    #
    #     rt_json_data = {}
    #
    #     database_controller = DataBaseController(db_name = "Development_Database", use_cloud_db = True)
    #     for collection_name in database_controller.Database.list_collection_names():
    #         db_collection = database_controller.Database.get_collection(collection_name)
    #
    #         rt_json_data[collection_name] = {}
    #         for data in db_collection.find():
    #             rt_json_data[collection_name][]



if __name__ == "__main__":
    # DataTools.SaveDataInLocalFile()

    pass


