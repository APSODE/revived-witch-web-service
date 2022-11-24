import json
import time
import sys
from typing import List, Dict, Union, Optional
from random import *

import flask
from bson import json_util

from database.models.gacha_banner_model import BannerData, Banner
from database.models.chest_gacha_banner_model import ChestGachaBannerData, ChestGachaBanner
from database.models.gacha_doll_model import DollData, Doll
from database.models.gacha_equip_model import ItemEquipmentData, ItemEquipment
from src.functions.DataTools import DataTools, BannerDataTypeError


class Simulator:
    def __init__(self, banner_name: str):
        from app import database_controller
        self.database_controller = database_controller
        # self._SIMULATE_BANNER_DATA = self.database_controller.FindDatas(
        #     collection_name = "GachaBanner",
        #     query = {"banner_name": banner_name},
        #     find_one = True
        # )
        self._SIMULATE_BANNER_DATA: Union[BannerData, ChestGachaBannerData]

        try:
            self._SIMULATE_BANNER_DATA = Banner.SerializeData(
                target_data = DataTools.DatabaseBannerDataSerializer(
                    database_banner_data = self.database_controller.FindDatas(
                        collection_name = "GachaBanner",
                        query = {"banner_name": banner_name},
                        find_one = True
                    )
                )
            )
            self.SIMULATOR_BANNET_TYPE = BannerData
        except BannerDataTypeError:
            self._SIMULATE_BANNER_DATA = ChestGachaBanner.SerializeData(
                target_data = self.database_controller.FindDatas(
                    collection_name = "ChestGachaBanner",
                    query = {"banner_name": banner_name},
                    find_one = True
                )
            )
            self.SIMULATOR_BANNET_TYPE = ChestGachaBannerData



        self._SIMULATE_GACHA_LIST = []

    def _GachaStackChecker(self, session: flask.session) -> dict:
        """
        current_stack는 현재의 가챠 스택을 전달 받는다.\n
        banner_type는 현재 시뮬레이트 하고 있는 가챠 배너의 타입을 전달 받는다.\n
        리턴은 Dictionary로 반환되며 이 Dictionary는 2개의 Key-Value를 가진다.\n
        first key-value : half - <bool>\n
        second key-value : full - <bool>\n
        이 두가지 Key는 현재 가챠 스택이 해당 배너의 천장 스택에 도달하였는지를 알려준다.

        :param session: int
        :return:
        """
        current_stack_half = session.get("gacha_stack_half")
        current_stack_full = session.get("gacha_stack_full")

        check_result = {
            "half": False,
            "full": False
        }
        banner_type = self._SIMULATE_BANNER_DATA.BannerType

        if banner_type in ["element", "soul"]:
            if current_stack_half == 80:
                check_result["half"] = True

        elif banner_type in ["dream", "limited"]:
            if current_stack_half == 80:
                check_result["half"] = True

            elif current_stack_full == 160:
                check_result["full"] = True

        return check_result

    def _GachaCeilingChecker(self, gacha_result_list: List[DollData], session: flask.session) -> None:
        # print(f"_GachaCeilingChecker 실행 확인")
        stack_check_result = self._GachaStackChecker(session = session)
        self._SIMULATE_BANNER_DATA: BannerData

        gacha_result_grade_list = [doll_grade.Grade for doll_grade in gacha_result_list]

        if self._SIMULATE_BANNER_DATA.PickUpData.get("active"):
            pick_up_doll_data = DataTools.GetDollDataByDollName(
                doll_name = self._SIMULATE_BANNER_DATA.PickUpData.get("pick_up_doll_name")
            )

            if stack_check_result.get("half"):
                print("반천장 작동")
                if "UR" not in gacha_result_grade_list:
                    del gacha_result_list[-1]

                    gacha_result_list.append(
                        Doll.SerializeData(
                            target_data = DataTools.DatabaseDollDataSerializer(
                                database_doll_data = choice(self._SIMULATE_BANNER_DATA.SummonableDolls.get("UR"))
                            )
                        )
                    )

            elif stack_check_result.get("full"):
                print("찐천장 작동")
                if pick_up_doll_data not in gacha_result_list:
                    del gacha_result_list[-1]

                    gacha_result_list.append(pick_up_doll_data)

            else:
                if "UR" in gacha_result_grade_list:
                    session["gacha_stack_half"] = 0

                if pick_up_doll_data in gacha_result_list:
                    session["gacha_stack_full"] = 0

        else:
            if stack_check_result.get("half"):
                print("반천장 작동")
                if "UR" not in gacha_result_grade_list:
                    del gacha_result_list[-1]

                    gacha_result_list.append(
                        Doll.SerializeData(
                            target_data=DataTools.DatabaseDollDataSerializer(
                                database_doll_data=choice(self._SIMULATE_BANNER_DATA.SummonableDolls.get("UR"))
                            )
                        )
                    )

    def SimulateGacha(self) -> [DollData]:
        f_time = time.perf_counter()
        GACHA_RESULT_LIST = []
        self._SIMULATE_BANNER_DATA: BannerData
        gacha_probability = self._SIMULATE_BANNER_DATA.Probability
        summonable_dolls = self._SIMULATE_BANNER_DATA.SummonableDolls

        for grade in ["UR", "SSR", "SR", "R"]:
            for E in choices(summonable_dolls.get(grade), k = gacha_probability.get(grade)):
                self._SIMULATE_GACHA_LIST.append(E)

        for gacha_result_doll in choices(self._SIMULATE_GACHA_LIST, k = 10):
            gacha_result_doll_obj = DollData(
                NAME = gacha_result_doll.get("NAME"),
                GRADE = gacha_result_doll.get("GRADE"),
                ELEMENT = gacha_result_doll.get("ELEMENT"),
                DOLL_CLASS = gacha_result_doll.get("DOLL_CLASS"),
                LIMITED = gacha_result_doll.get("LIMITED")
            )
            GACHA_RESULT_LIST.append(gacha_result_doll_obj)
        s_time = time.perf_counter()

        print(f"SimulateGacha 소요시간 : {s_time - f_time}s")
        return GACHA_RESULT_LIST

    def SimulatePickUpGacha(self, session: flask.session) -> [DollData]:
        if type(self._SIMULATE_BANNER_DATA) == ChestGachaBannerData:
            raise BannerDataTypeError("인형 가챠 시뮬레이터에 상자 가챠 배너 데이터가 입력되었습니다.")

        GACHA_RESULT_LIST = []
        self._SIMULATE_BANNER_DATA: BannerData
        gacha_probability = self._SIMULATE_BANNER_DATA.Probability
        summonable_dolls = self._SIMULATE_BANNER_DATA.SummonableDolls

        for grade in ["UR", "SSR", "SR", "R"]:
            if self._SIMULATE_BANNER_DATA.PickUpData.get("active"):
                for E in choices(summonable_dolls.get(grade), k = gacha_probability.get(grade) - 1 if grade == "UR" else gacha_probability.get(grade)):
                    self._SIMULATE_GACHA_LIST.append(E)

                if grade == "UR":
                    self._SIMULATE_GACHA_LIST.append(
                        DataTools.GetDollDataByDollName(
                            doll_name = self._SIMULATE_BANNER_DATA.PickUpData.get("pick_up_doll_name")
                        ).GetAllDollData()
                    )

            else:
                for E in choices(summonable_dolls.get(grade), k = gacha_probability.get(grade)):
                    self._SIMULATE_GACHA_LIST.append(E)

        for gacha_result_doll in choices(self._SIMULATE_GACHA_LIST, k = 10):
            gacha_result_doll_object = Doll.SerializeData(
                target_data = DataTools.DatabaseDollDataSerializer(
                    database_doll_data = gacha_result_doll
                )
            )

            GACHA_RESULT_LIST.append(gacha_result_doll_object)

        self._GachaCeilingChecker(gacha_result_list = GACHA_RESULT_LIST, session = session)
        return GACHA_RESULT_LIST

    def SimulateChestGacha(self, session: flask.session = None) -> ItemEquipmentData:

        self._SIMULATE_BANNER_DATA: ChestGachaBannerData
        summonable_items = self._SIMULATE_BANNER_DATA.SummonableItems
        # print(summonable_items)

        random_choice_item_data = choice(summonable_items.get(choice(["weapon", "armor", "accessory"])))

        random_choice_item_object = ItemEquipment.SerializeData(
            target_data = random_choice_item_data
        )

        return random_choice_item_object

    def GradeChecker(self, gacha_result_list: [DollData]) -> dict:
        rt_data = {
            "ur": False,
            "ssr": False
        }

        for doll_data in gacha_result_list:
            doll_data: DollData
            if doll_data.Grade == "UR":
                rt_data["ur"] = True

            elif doll_data.Grade == "SSR":
                rt_data["ssr"] = True
            else:
                pass

        return rt_data


if __name__ == "__main__":
    gacha_simulator = Simulator(banner_name = "영혼 소환")
    gacha_simulator.SimulateGacha()
