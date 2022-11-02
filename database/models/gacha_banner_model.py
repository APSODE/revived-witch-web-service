from typing import List, Dict

class BannerData:
    def __init__(
            self,
            banner_name: str,
            banner_type: str,
            stack_info: dict = None,
            pick_up_data: dict = None,
            probability: dict = None,
            summonable_dolls: dict = None

    ):
        self._banner_name = banner_name
        self._banner_type = banner_type

        if stack_info is not None:
            self._stack_info = stack_info
        else:
            self._stack_info = {
                "half": 80,
                "full": 160
            }

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

        if summonable_dolls is not None:
            self._summonable_dolls = summonable_dolls
        else:
            witch_data = {
                "NAME": "마녀",
                "GRADE": "SR",
                "ELEMENT": "Aether",
                "DOLL_CLASS": "Witch",
                "LIMITED": False
            }
            self._summonable_dolls = {
                "UR": [witch_data],
                "SSR": [witch_data],
                "SR": [witch_data],
                "R": [witch_data]
            }







    @property
    def BannerName(self) -> str:
        return self._banner_name

    @property
    def BannerType(self) -> str:
        return self._banner_type

    @property
    def StackInfo(self) -> dict:
        return self._stack_info

    @property
    def PickUpData(self) -> dict:
        """
        return dict는 2가지의 key-value를 가진다.\n
        first key-value | active - <bool>\n
        second key-value | pick_up_doll_name - <str>\n
        :return:
        """
        return self._pick_up_data

    @property
    def Probability(self) -> dict:
        return self._probability

    @property
    def SummonableDolls(self) -> Dict[str, List[dict]]:
        return self._summonable_dolls

    def GetAllBannerData(self) -> dict:
        RT_DICT = {
            "BANNER_NAME": self._banner_name,
            "BANNER_TYPE": self._banner_type,
            "STACK_INFO": self._stack_info,
            "PICK_UP_DATA": self._pick_up_data,
            "PROBABILITY": self._probability,
            "SUMMONABLE_DOLLS": self._summonable_dolls
        }

        return RT_DICT

    def __repr__(self):
        RT_STR = f"\n=================================\n" \
                 f"BANNER_NAME : {self._banner_name}\n" \
                 f"BANNER_TYPE : {self._banner_type}\n" \
                 f"STACK_INFO : {self._stack_info}\n" \
                 f"PICK_UP_DATA: {self._pick_up_data}\n" \
                 f"PROBABILITY: {self._probability}\n" \
                 f"SUMMONABLE_DOLLS : {self._summonable_dolls}\n" \
                 f"\n=================================\n"

        return RT_STR


class Banner:
    @staticmethod
    def SerializeData(target_data: dict) -> BannerData:
        return BannerData(
            banner_name=target_data.get("BANNER_NAME"),
            banner_type=target_data.get("BANNER_TYPE"),
            stack_info=target_data.get("STACK_INFO"),
            pick_up_data=target_data.get("PICK_UP_DATA"),
            probability=target_data.get("PROBABILITY"),
            summonable_dolls=target_data.get("SUMMONABLE_DOLLS")
        )
