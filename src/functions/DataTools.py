import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from database.models.gacha_doll_model import DollData
from database.DataBaseController import DataBaseController




class DataTools:
    def __init__(self):
        self._RW_DATABASE_SITE_URL = "https://revivedwitch.kloenlansfiel.com/ko/characters"


    def _GetSiteData_HTML(self) -> BeautifulSoup:
        return BeautifulSoup(
            requests.get(url = self._RW_DATABASE_SITE_URL).text,
            "html.parser"
        )

    def _QueryGradeSelecotr(self, default_query: dict, grade: str) -> dict:

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

    def CreateGachaBannerData(self, element: str = None, dream: str = None, limited: str = None) -> [dict]:
        database_controller = DataBaseController(db_name = "Development_Database")
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

    def AddNewDoll(self, DOLL_DTO: DollData) -> bool:
        database_controller = DataBaseController("Development_Database")
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






if __name__ == "__main__":
    pass


