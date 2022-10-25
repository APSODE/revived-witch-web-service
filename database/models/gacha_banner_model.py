class BannerData:
    def __init__(self, banner_name: str, pick_up_data: dict = None, probability: dict = None):
        self._banner_name = banner_name

        if pick_up_data is not None:
            self._pick_up_data = pick_up_data
        else:
            self._pick_up_data = {
                "active": False,
                "target": ""
            }

        if probability is not None:
            self._probability = probability

        else:
            self._probability = {
                "UR": 2,
                "SSR": 8,
                "SR": 40,
                "R": 50
            }

    @property
    def BannerName(self) -> str:
        return self._banner_name

    @property
    def PickUpData(self) -> dict:
        return self._pick_up_data

    @property
    def Probability(self) -> dict:
        return self._probability

    def GetAllBannerData(self) -> dict:
        RT_DICT = {
            "BANNER_NAME": self._banner_name,
            "PICK_UP_DATA": self._pick_up_data,
            "PROBABILITY": self._probability
        }

        return RT_DICT

    def __repr__(self):
        RT_STR = f"\n=================================\n" \
                 f"BANNER_NAME : {self._banner_name}\n" \
                 f"PICK_UP_DATA: {self._pick_up_data}\n" \
                 f"PROBABILITY: {self._probability}\n" \
                 f"\n=================================\n"

        return RT_STR


class Banner:
    @staticmethod
    def SerializeData(target_data: dict) -> BannerData:
        return BannerData(
            banner_name=target_data.get("BANNER_NAME"),
            pick_up_data=target_data.get("PICK_UP_DATA"),
            probability=target_data.get("PROBABILITY")
        )
