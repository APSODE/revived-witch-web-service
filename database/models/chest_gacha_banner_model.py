from typing import List, Dict
from database.models.gacha_equip_model import ItemEquipmentData


class ChestGachaBannerData:
    def __init__(
            self,
            banner_name: str,
            banner_type: str,
            stack_info: dict = None,
            pick_up_data: dict = None,
            probability: dict = None,
            summonable_items: dict = None

    ):
        self._banner_name = banner_name
        self._banner_type = banner_type

        if stack_info is not None:
            self._stack_info = stack_info
        else:
            self._stack_info = {
                "half": 0,
                "full": 0
            }

        if pick_up_data is not None:
            self._pick_up_data = pick_up_data
        else:
            self._pick_up_data = {
                "active": False,
                "pick_up_item_name": ""
            }

        if probability is not None:
            self._probability = probability

        else:
            self._probability = {
                "weapon": 33,
                "armor": 33,
                "accessory": 33
            }

        if summonable_items is not None:
            self._summonable_items = summonable_items
        else:
            ie_data_object = ItemEquipmentData(
                name = "고급 룬",
                grade = "legendary"
            )
            dummy_item_data = ie_data_object.GetAllItemEquipmentData()
            self._summonable_items = {
                "weapon": [dummy_item_data],
                "armor": [dummy_item_data],
                "accessory": [dummy_item_data]
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
    def SummonableItems(self) -> Dict[str, List[dict]]:
        return self._summonable_items

    def GetAllBannerData(self) -> dict:
        RT_DICT = {
            "banner_name": self._banner_name,
            "banner_type": self._banner_type,
            "stack_info": self._stack_info,
            "pick_up_data": self._pick_up_data,
            "probability": self._probability,
            "summonable_items": self._summonable_items
        }

        return RT_DICT

    def __repr__(self):
        RT_STR = f"\n=================================\n" \
                 f"banner_name : {self._banner_name}\n" \
                 f"banner_type : {self._banner_type}\n" \
                 f"stack_info : {self._stack_info}\n" \
                 f"pick_up_data: {self._pick_up_data}\n" \
                 f"probability: {self._probability}\n" \
                 f"summonable_items : {self._summonable_items}\n" \
                 f"\n=================================\n"

        return RT_STR

class ChestGachaBanner:
    @staticmethod
    def SerializeData(target_data: dict) -> ChestGachaBannerData:
        return ChestGachaBannerData(
            banner_name = target_data.get("banner_name"),
            banner_type = target_data.get("banner_type"),
            stack_info = target_data.get("stack_info"),
            pick_up_data = target_data.get("pick_up_data"),
            probability = target_data.get("probability"),
            summonable_items = target_data.get("summonable_items")
        )
