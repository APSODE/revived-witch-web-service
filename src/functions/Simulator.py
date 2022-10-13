from database.DataBaseController import DataBaseController
import json
from bson import json_util

class Simulator:
    def __init__(self, banner_name: str):
        self.database_controller = DataBaseController("Development_Database")
        self._SIMULATE_BANNER_DATA = self.database_controller.FindDatas(
            collection_name = "GachaBanner",
            query = {"banner_name": banner_name},
            find_one = True
        )

    def _SelectGrade(self):
        pass

    def Test(self):
        with open("TEST_DATA.json", "w") as WRITE_PROFILE:
            result = self._SIMULATE_BANNER_DATA
            json_data = json.dumps(result, default = json_util.default)
            json.dump(json.loads(json_data), WRITE_PROFILE, indent = 4)

    def SimulateGacha(self):
        pass


if __name__ == "__main__":

    gacha_simulator = Simulator(banner_name = "영혼 소환")
    gacha_simulator.Test()
