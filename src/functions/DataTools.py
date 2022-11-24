import json
import os
import copy
import requests

from bs4 import BeautifulSoup
from typing import Dict, List

from database.DataBaseController import DataBaseController
from database.models.gacha_doll_model import DollData, Doll
from database.models.gacha_banner_model import BannerData, Banner
from database.models.gacha_equip_model import ItemEquipmentData, ItemEquipment


class BannerDataTypeError(Exception):
    def __init__(self, error_msg):
        self._error_msg = error_msg

    def __str__(self):
        return self._error_msg



class DataTools:
    def __init__(self):
        self._RW_DATABASE_SITE_URL = "https://revivedwitch.kloenlansfiel.com/ko/characters"


    def _GetSiteData_HTML(self) -> BeautifulSoup:
        return BeautifulSoup(
            requests.get(url = self._RW_DATABASE_SITE_URL).text,
            "html.parser"
        )

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

            DOLL_DATA_LIST.append(DOLL_DATA_DTO)

        return DOLL_DATA_LIST

    def CreateAllDollData(self, collection_name: str) -> bool:
        WORK_STATUS = True
        try:
            for doll_data_object in self.GetData_DOLL():
                from app import database_controller
                database_controller.AddDataToDataBase(
                    collection_name = collection_name,
                    add_data = [doll_data_object.GetAllDollData()]
                )

        except Exception as MSG:
            WORK_STATUS = False
            print(MSG)
        finally:
            return WORK_STATUS

    @staticmethod
    def _CreateBannerStackInfo(banner_type: str) -> dict:
        stack_info = {
            "half": 80,
            "full": 160
        }

        if banner_type in ["element", "soul", "exclusive"]:
            stack_info["full"] = 80

        return stack_info

    @staticmethod
    def _CreateBannerProbabilityInfo(banner_type: str) -> dict:
        if banner_type == "exclusive":
            probability_data = {
                "exclusive": 5,
                "legendary": 3,
                "unique": 42,
                "other": 50
            }
        elif banner_type == "chest":
            probability_data = {
                "weapon": 33,
                "armor": 33,
                "accessory": 33
            }
        else:
            probability_data = {
                "UR": 2,
                "SSR": 8,
                "SR": 40,
                "R": 50
            }

        return probability_data

    @staticmethod
    def _QueryElementSelector(base_query: dict, banner_type: str, banner_element_data: str, grade_data: str) -> None:
        if banner_type == "element":
            if grade_data in ["SR", "R"]:
                element_query = {
                    "ELEMENT": {
                        "$ne": "Aether"
                    }
                }

            else:
                element_query = {
                    "ELEMENT": {
                        "$eq": banner_element_data
                    }
                }

        else:
            element_query = {
                "ELEMENT": {
                    "$ne": "Aether"
                }
            }

        base_query["$and"].append(element_query)

    @staticmethod
    def _QueryLimitedSelector(base_query: dict, banner_type: str, pick_up_data: dict) -> None:
        pick_up_doll_name = pick_up_data.get("pick_up_doll_name")


        if banner_type == "limited":
            limited_query = {
                "$or": [
                    {
                        "NAME": {
                            "$eq": pick_up_doll_name
                        }
                    },
                    {
                        "LIMITED": {
                            "$eq": False
                        }
                    }
                ]
            }

        else:
            limited_query = {
                "LIMITED": {
                    "$eq": False
                }
            }

        base_query["$and"].append(limited_query)

    @staticmethod
    def _QueryAnemoneSelecotr(base_query: dict, banner_type: str):
        if banner_type != "soul":
            anemone_query = {
                "NAME": {
                    "$ne": "아네모네"
                }
            }

            base_query["$and"].append(anemone_query)

        else:
            pass

    @staticmethod
    def _QueryGradeSelector(base_query: dict, grade_data: str):
        grade_query = {
            "GRADE": {
                "$eq": grade_data
            }
        }

        base_query["$and"].append(grade_query)

    @staticmethod
    def CreateGachaBannerQuery(banner_data: dict) -> dict:
        """
        banner_data dict는 형태가 정해져 있으며 이를 따라야 한다.\n
        banner_type -> ["element", "dream", "limited", "soul"] 4개 중 한가지 값\n
        banner_element_data -> ["All", "Brimstone", "Saltstone", "Mercury"] 4개 중 한가지 값\n
        banner_name: <str>\n
        pick_up_data: {"active": <bool>, "pick_up_doll_name": <str>}\n
        *pick_up_doll_name은 activate가 False이면 None으로 전달\n
        이렇게 4가지 값을 포함한 dict를 전달하여야 한다.\n
        미전달시 기본값인 "soul"로 작동하여 영혼소환의 배너를 생성한다.\n\n
        :param banner_data: dict
        :return:
        """

        banner_data_keys = banner_data.keys()
        if "banner_type" not in banner_data_keys or "pick_up_data" not in banner_data_keys or "banner_element_data" not in banner_data_keys:
            banner_type = "soul"
            banner_name = "영혼 소환"
            banner_element_data = "All"
            pick_up_data = {
                "active": False,
                "pick_up_doll_name": None
            }

        else:
            banner_type = banner_data.get("banner_type")
            banner_name = banner_data.get("banner_name")
            banner_element_data = banner_data.get("banner_element_data")
            pick_up_data = banner_data.get("pick_up_data")

        base_query = {
            "$and": [
                {
                    "NAME": {
                        "$ne": "유이"
                    }
                }
            ]
        }

        summonable_doll_dict = {
            "UR": None,
            "SSR": None,
            "SR": None,
            "R": None
        }

        for grade in summonable_doll_dict.keys():
            query_buffer = copy.deepcopy(base_query)

            DataTools._QueryLimitedSelector(
                base_query=query_buffer,
                banner_type=banner_type,
                pick_up_data=pick_up_data
            )

            DataTools._QueryAnemoneSelecotr(
                base_query=query_buffer,
                banner_type=banner_type
            )

            DataTools._QueryElementSelector(
                base_query=query_buffer,
                banner_type=banner_type,
                banner_element_data=banner_element_data,
                grade_data=grade
            )

            DataTools._QueryGradeSelector(
                base_query=query_buffer,
                grade_data=grade
            )

            # from app import database_controller
            summonable_doll_dict[grade] = query_buffer

        gacha_banner_data = {
            "banner_name": banner_name,
            "banner_type": banner_type,
            "stack_info": DataTools._CreateBannerStackInfo(banner_type=banner_type),
            "pick_up": pick_up_data,
            "summonable_doll": summonable_doll_dict,
            "probability": DataTools._CreateBannerProbabilityInfo(banner_type=banner_type)
        }

        return gacha_banner_data

    def CreateGachaBannerData(self, banner_data: dict, collection_name: str = None) -> None:
        """
        banner_data dict는 형태가 정해져 있으며 이를 따라야 한다.\n
        banner_type -> ["element", "dream", "limited", "soul"] 4개 중 한가지 값\n
        banner_element_data -> ["All", "Brimstone", "Saltstone", "Mercury"] 4개 중 한가지 값\n
        banner_name: <str>\n
        pick_up_data: {"active": <bool>, "pick_up_doll_name": <str>}\n
        *pick_up_doll_name은 activate가 False이면 None으로 전달\n
        이렇게 4가지 값을 포함한 dict를 전달하여야 한다.\n
        미전달시 기본값인 "soul"로 작동하여 영혼소환의 배너를 생성한다.\n\n
        :param banner_data: dict
        :return:
        """

        banner_data_keys = banner_data.keys()
        if "banner_type" not in banner_data_keys or "pick_up_data" not in banner_data_keys or "banner_element_data" not in banner_data_keys:
            banner_type = "soul"
            banner_name = "영혼 소환"
            banner_element_data = "All"
            pick_up_data = {
                "active": False,
                "pick_up_doll_name": None
            }

        else:
            banner_type = banner_data.get("banner_type")
            banner_name = banner_data.get("banner_name")
            banner_element_data = banner_data.get("banner_element_data")
            pick_up_data = banner_data.get("pick_up_data")

        base_query = {
            "$and": [
                {
                    "NAME": {
                        "$ne": "유이"
                    }
                }
            ]
        }

        summonable_doll_dict = {
            "UR": None,
            "SSR": None,
            "SR": None,
            "R": None
        }

        for grade in summonable_doll_dict.keys():
            query_buffer = copy.deepcopy(base_query)

            self._QueryLimitedSelector(
                base_query = query_buffer,
                banner_type = banner_type,
                pick_up_data = pick_up_data
            )

            self._QueryAnemoneSelecotr(
                base_query = query_buffer,
                banner_type = banner_type
            )

            self._QueryElementSelector(
                base_query = query_buffer,
                banner_type = banner_type,
                banner_element_data = banner_element_data,
                grade_data = grade
            )

            self._QueryGradeSelector(
                base_query = query_buffer,
                grade_data = grade
            )

            from app import database_controller
            summonable_doll_dict[grade] = database_controller.FindDatas(
                collection_name = "Doll",
                query = query_buffer
            )

        gacha_banner_data = {
            "banner_name": banner_name,
            "banner_type": banner_type,
            "stack_info": self._CreateBannerStackInfo(banner_type = banner_type),
            "pick_up": pick_up_data,
            "summonable_doll": summonable_doll_dict,
            "probability": DataTools._CreateBannerProbabilityInfo(banner_type = banner_type)
        }

        from app import database_controller
        database_controller.AddDataToDataBase(
            collection_name = "GachaBanner" if collection_name is None else collection_name,
            add_data = [gacha_banner_data]
        )

    def CreateAllGachaBanner(self, collection_name: str = None):
        for elem in ["Brimstone", "Saltstone", "Mercury", "Aether"]:
            if elem == "Brimstone":
                name = "유황"

            elif elem == "Saltstone":
                name = "염석"

            elif elem == "Mercury":
                name = "수은"

            else:
                name = "영혼"


            banner_data = {
                "banner_type": "soul" if elem == "Aether" else "element",
                "banner_element_data": elem,
                "banner_name": f"{name} 소환" if elem == "Aether" else f"{name} 원소 소환",
                "pick_up_data": {
                    "active": False,
                    "pick_up_doll_name": None
                }
            }

            self.CreateGachaBannerData(banner_data = banner_data, collection_name = collection_name)

    @staticmethod
    def _CreateChestItemData() -> List[dict]:
        from app import BASE_DIR
        chest_item_dir = BASE_DIR + f"\\static\\img\\item\\equipment\\chest\\"

        # item_data = {
        #     "legendary": {
        #         "690": [],
        #         "740": []
        #     },
        #     "unique": {
        #         "640": []
        #     }
        # }

        item_data = []

        for item_grade in ["legendary", "unique"]:
            equip_point_list = ["740", "690"] if item_grade == "legendary" else ["640"]
            for equip_point in equip_point_list:
                for equip_type in ["weapon", "armor", "accessory"]:
                    equipment_dir = chest_item_dir + f"{item_grade}\\{equip_point}\\{equip_type}\\"
                    for item_name in os.listdir(equipment_dir):
                        equipment_data = ItemEquipmentData(
                            name = item_name.split(".")[0],
                            grade = item_grade,
                            equip_point = int(equip_point),
                            equip_type = equip_type,
                            is_chest = True if item_grade == "legendary" else False
                        )

                        # item_data[item_grade][equip_point].append(equipment_data.GetAllEquipData())
                        item_data.append(equipment_data.GetAllItemEquipmentData())

        return item_data

    @staticmethod
    def _CreateExclusiveItemData() -> List[dict]:
        from app import BASE_DIR
        exclusive_item_dir = BASE_DIR + f"\\static\\img\\item\\equipment\\exclusive\\"

        # item_data = {
        #     "limited": [],
        #     "unlimited": []
        # }

        item_data = []

        exclusive_list = ["limited", "unlimited"]

        for is_limited in exclusive_list:
            equip_point_item_dir = exclusive_item_dir + f"{is_limited}\\"

            for item_name in os.listdir(equip_point_item_dir):
                equipment_data = ItemEquipmentData(
                    name = item_name.split(".")[0].split("_")[0],
                    grade = "exclusive",
                    owner = item_name.split(".")[0].split("_")[1],
                    equip_point = 0,
                    equip_type = "exclusive",
                    is_exclusive = True,
                    is_limited = True if is_limited == "limited" else False
                )

                # item_data[is_limited].append(equipment_data.GetAllEquipData())
                item_data.append(equipment_data.GetAllItemEquipmentData())

        return item_data

    @staticmethod
    def _CreateOtherItemData() -> List[dict]:
        from app import BASE_DIR
        other_item_dir = BASE_DIR + f"\\static\\img\\item\\other\\"

        # item_data = {
        #     "legendary": [],
        #     "unique": [],
        #     "epic": [],
        #     "rare": []
        # }
        item_data = []

        # for item_grade in item_data.keys():
        for item_grade in ["legendary", "unique", "epic", "rare"]:
            for item_name in os.listdir(other_item_dir + item_grade + "\\"):
                other_item_data = ItemEquipmentData(
                    name = item_name.split(".")[0],
                    grade = item_grade,
                    owner = ""
                )

                item_data.append(other_item_data.GetAllItemEquipmentData())

        return item_data

    @staticmethod
    def CreateAllEquipmentData(use_database_controller: DataBaseController = None, collection_name: str = None) -> None:
        """
        equipment_data Dict는 Equipment의 Data Transfer Object의 \n
        GetAllEquipData메소드를 이용하여 값을 전달하여야 한다.\n
        collection_name은 db에 사용할 collection_name을 지정하는 것으로\n
        수동지정을 원하면 값을 입력하여 사용하고, \n
        고정값을 사용하려면 파라미터를 전달하지 않으면 된다.\n
        :param equipment_data: EquipData.GetAllEquipData()
        :param collection_name: str
        :return None:
        """
        if use_database_controller is None:
            from app import database_controller
        else:
            database_controller = use_database_controller
        for data in [DataTools._CreateChestItemData(), DataTools._CreateExclusiveItemData()]:
            database_controller.AddDataToDataBase(
                collection_name = collection_name if collection_name is not None else "Equipment",
                add_data = data
            )

    @staticmethod
    def CreateAllOtherItemData(use_database_controller: DataBaseController = None, collection_name: str = None) -> None:
        if use_database_controller is None:
            from app import database_controller
        else:
            database_controller = use_database_controller
        for data in [DataTools._CreateOtherItemData()]:
            database_controller.AddDataToDataBase(
                collection_name = collection_name if collection_name is not None else "OtherItem",
                add_data = data
            )

    @staticmethod
    def _QueryChestItemSelector(banner_type: str) -> dict:
        if banner_type == "chest":
            return {
                "$and": [
                    {
                        "is_chest": {
                            "$eq": True
                        }
                    },
                    {
                        "grade": {
                            "$eq": "legendary"
                        }
                    }
                ]
            }
        else:
            return {
                "$and": [
                    {
                        "is_exclusive": {
                            "$eq": True
                        }
                    }
                ]
            }

    @staticmethod
    def _QueryItemTypeSelector(base_query: dict, banner_type: str, item_type: str) -> None:
        if banner_type == "chest":
            equip_type_query = {
                "equip_type": {
                    "$eq": item_type
                }
            }

            base_query["$and"].append(equip_type_query)
            print(base_query)
        elif banner_type == "exclusive":
            pass

    @staticmethod
    def CreateItemGachaBannerData(
            banner_data: dict,
            use_database_controller: DataBaseController = None,
            collection_name: str = None) -> None:
        """
        banner_data는 형식이 정해져 있으며 이를 따라야한다.
        banner_data는 banner_name, banner_type, pick_up_data이 3가지의 키값을 필수로 가지고 있어야 한다.\n
        banner_name : str\n
        banner_type : str -> ["exclusive", "chest"] 이 두 가지중 선택\n
        pick_up_data : dict -> {"active": <bool>, "pick_up_item_name": <str>}\n
        :param banner_data:
        :param use_database_controller:
        :param collection_name:
        :return:
        """

        banner_name = banner_data.get("banner_name")
        banner_type = banner_data.get("banner_type")
        pick_up_data = banner_data.get("pick_up_data")

        # summonable_items = use_database_controller.FindDatas(
        #     collection_name = "Equipment",
        #     query = DataTools._QueryChestItemSelector(banner_type = banner_type)
        # )

        summonable_items = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }

        base_query = DataTools._QueryChestItemSelector(banner_type = banner_type)

        for equip_type in summonable_items.keys():
            query_buffer = copy.deepcopy(base_query)

            DataTools._QueryItemTypeSelector(
                banner_type = banner_type,
                base_query = query_buffer,
                item_type = equip_type
            )

            summonable_items[equip_type] = use_database_controller.FindDatas(
                collection_name = "Equipment",
                query = query_buffer
            )



        new_banner_data = {
            "banner_name": banner_name,
            "banner_type": banner_type,
            "pick_up_data": pick_up_data,
            "stack_info": DataTools._CreateBannerStackInfo(banner_type = banner_type),
            "summonable_items": summonable_items,
            "probability": DataTools._CreateBannerProbabilityInfo(banner_type = banner_type)
        }

        if banner_type == "chest":
            new_banner_data["stack_info"]["half"] = 0
            new_banner_data["stack_info"]["full"] = 0

        use_database_controller.AddDataToDataBase(collection_name = collection_name, add_data = [new_banner_data])



    @staticmethod
    def FuncTestCall():
        print(DataTools._CreateOtherItemData())

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
        if database_doll_data is None:
            raise ValueError("db데이터를 시리얼라이즈 하기 위해서는 파라미터로 전달받은 값이 None이 되면 안됩니다.")

        RT_DICT = {
            "NAME": database_doll_data.get("NAME"),
            "GRADE": database_doll_data.get("GRADE"),
            "ELEMENT": database_doll_data.get("ELEMENT"),
            "DOLL_CLASS": database_doll_data.get("DOLL_CLASS"),
            "LIMITED": database_doll_data.get("LIMITED")
        }

        return RT_DICT

    @staticmethod
    def DatabaseBannerDataSerializer(database_banner_data: dict) -> dict:
        if database_banner_data is None:
            raise BannerDataTypeError("db데이터를 시리얼라이즈 하기 위해서는 파라미터로 전달받은 값이 None이 되면 안됩니다.")

        if "summonable_items" in database_banner_data.keys():
            raise BannerDataTypeError("입력받은 database_banner_data는 ChestGachaBanner데이터 입니다.")


        RT_DICT = {
            # "BANNER_NAME": database_banner_data.get("BANNER_NAME"),
            # "BANNER_TYPE": database_banner_data.get("BANNER_TYPE"),
            # "STACK_INFO": database_banner_data.get("STACK_INFO"),
            # "PICK_UP_DATA": database_banner_data.get("PICK_UP_DATA"),
            # "PROBABILITY": database_banner_data.get("PROBABILITY"),
            # "SUMMONABLE_DOLLS": database_banner_data.get("SUMMONABLE_DOLLS")
            "BANNER_NAME": database_banner_data.get("banner_name"),
            "BANNER_TYPE": database_banner_data.get("banner_type"),
            "STACK_INFO": database_banner_data.get("stack_info"),
            "PICK_UP_DATA": database_banner_data.get("pick_up"),
            "PROBABILITY": database_banner_data.get("probability"),
            "SUMMONABLE_DOLLS": database_banner_data.get("summonable_doll")
        }
        # print(f"RT_DICT : {RT_DICT}")

        return RT_DICT

    @staticmethod
    def DatabaseChestGachaBannerDataSerializer(database_banner_data: dict):
        RT_DICT = {
            "banner_name": database_banner_data.get("banner_name"),
            "banner_type": database_banner_data.get("banner_type"),
            "stack_info": database_banner_data.get("stack_info"),
            "pick_up_data": database_banner_data.get("pick_up_data"),
            "probability": database_banner_data.get("probability"),
            "summonable_items": database_banner_data.get("summonable_dolls")
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
            target_data = DataTools.DatabaseBannerDataSerializer(
                database_banner_data = banner_db_data
            )
        )

        return banner_object

    @staticmethod
    def GetItemDataByItemName(item_name: str, use_database_controller: DataBaseController = None) -> ItemEquipmentData:
        if use_database_controller is None:
            from app import database_controller
        else:
            database_controller = use_database_controller

        item_find_query = {"name": item_name}


        item_db_data = database_controller.FindDatas(
            collection_name = "Equipment",
            query = item_find_query,
            find_one = True
        )

        if item_db_data is None:
            item_db_data = database_controller.FindDatas(
                collection_name = "OtherItem",
                query = item_find_query,
                find_one = True
            )

        item_object = ItemEquipment.SerializeData(
            target_data = item_db_data
        )

        return item_object

if __name__ == "__main__":
    # DataTools.SaveDataInLocalFile()

    pass


