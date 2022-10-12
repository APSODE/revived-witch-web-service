

class Simulator:
    def __init__(self):
        self._SIMULATE_DATA = {
            "GACHA": {
                "DOLL": {
                    "PICKUP": {
                        "ACTIVE": True,
                        "TARGET": "안젤린"
                    },

                    "PROBABILITY": {
                        "UR": 2,
                        "SSR": 8,
                        "SR": 40,
                        "R": 50
                    },

                    "TYPE": "DREAM",

                    "DOLL_DATA": {
                        "UR": [],
                        "SSR": [],
                        "SR": [],
                        "R": []
                    }

                }
            }
        }

    def _SetInitialData(self) -> None:
        pass

    def _SelectGrade(self):
        pass