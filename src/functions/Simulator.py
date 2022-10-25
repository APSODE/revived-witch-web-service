import json
import time
from random import *

from bson import json_util

from database.models.gacha_banner_model import BannerData
from database.models.gacha_doll_model import DollData
from src.functions.DataTools import DataTools


class Simulator:
    def __init__(self, banner_name: str):
        from app import database_controller
        self.database_controller = database_controller
        self._SIMULATE_BANNER_DATA = self.database_controller.FindDatas(
            collection_name = "GachaBanner",
            query = {"banner_name": banner_name},
            find_one = True
        )
        self._SIMULATE_GACHA_LIST = []

    def _SelectGrade(self):
        pass

    def Test(self):
        with open("TEST_DATA.json", "w") as WRITE_PROFILE:
            result = self._SIMULATE_BANNER_DATA
            json_data = json.dumps(result, default = json_util.default)
            json.dump(json.loads(json_data), WRITE_PROFILE, indent = 4)

    def SimulateGacha(self) -> [DollData]:
        f_time = time.perf_counter()
        GACHA_RESULT_LIST = []
        gacha_probability = self._SIMULATE_BANNER_DATA.get("probability")
        summonable_dolls = self._SIMULATE_BANNER_DATA.get("summonable_doll")
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

    def SimulatePickUpGacha(self, banner_data: BannerData, current_gacha_count: int) -> [DollData]:
        banner_pickup_data = banner_data.PickUpData
        banner_probability = banner_data.Probability

        if banner_pickup_data.get("active"):
            pickup_doll_data = DataTools.GetDollDataByDollName(doll_name = banner_pickup_data.get("target"))




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
