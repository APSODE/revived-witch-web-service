from typing import List, Dict



class ItemEquipmentData:
    def __init__(self,
                 name: str,
                 grade: str,
                 owner: str = None,
                 equip_point: int = None,
                 status: Dict[str, int] = None,
                 equip_type: str = "other",
                 is_chest: bool = False,
                 is_exclusive: bool = False,
                 is_limited: bool = False
                 ):
        
        
        
        self._name = name
        self._grade = grade
        self._equip_type = equip_type
        self._is_limited = is_limited
        self._is_chest = is_chest
        self._is_exclusive = is_exclusive

        if owner is None:
            self._owner = ""
        else:
            self._owner = owner

        if equip_point is None:
            self._equip_point = 0
        else:
            self._equip_point = equip_point

        if status is None:
            self._status = {}
        else:
            self._status = status



    @property
    def ItemEquipName(self) -> str:
        return self._name

    @property
    def ItemEquipGrade(self) -> str:
        return self._grade

    @property
    def ItemEquipPoint(self) -> int:
        return self._equip_point

    @property
    def ItemEquipStatus(self) -> Dict[str, int]:
        return self._status

    @property
    def ItemEquipType(self) -> str:
        return self._equip_type

    @property
    def IsLimited(self) -> bool:
        return self._is_limited

    @property
    def IsChest(self) -> bool:
        return self._is_chest

    @property
    def IsExclusive(self) -> bool:
        return self._is_exclusive

    def GetAllItemEquipmentData(self) -> dict:
        RT_DICT = {
            "name": self._name,
            "grade": self._grade,
            "owner": self._owner,
            "equip_point": self._equip_point,
            "status": self._status,
            "equip_type": self._equip_type,
            "is_chest": self._is_chest,
            "is_exclusive": self._is_exclusive,
            "is_limited": self._is_limited
        }

        return RT_DICT

    def __repr__(self):
        RT_STR = f"\n=================================\n" \
                 f"equip_name : {self._name}\n" \
                 f"equip_grade : {self._grade}\n" \
                 f"equip_owner : {self._owner}\n" \
                 f"equip_point : {self._equip_point}\n" \
                 f"equip_status : {self._status}\n" \
                 f"equip_type : {self._equip_type}\n" \
                 f"is_chest : {self._is_chest}\n" \
                 f"is_exclusive : {self._is_exclusive}\n" \
                 f"is_limited : {self._is_limited}\n" \
                 f"\n=================================\n"

        return RT_STR


class ItemEquipment:
    @staticmethod
    def SerializeData(target_data: dict) -> ItemEquipmentData:
        if "name" not in target_data.keys():
            raise KeyError("장비 오브젝트를 생성하기 위해서는 Dict데이터에 'name'이라는 키값이 존재하여야 합니다.")

        if "grade" not in target_data.keys():
            raise KeyError("장비 오브젝트를 생성하기 위해서는 Dict데이터에 'grade'이라는 키값이 존재하여야 합니다.")

        if "owner" not in target_data.keys():
            raise KeyError("장비 오브젝트를 생성하기 위해서는 Dict데이터에 'owner'이라는 키값이 존재하여야 합니다.")

        if "equip_point" not in target_data.keys():
            raise KeyError("장비 오브젝트를 생성하기 위해서는 Dict데이터에 'equip_point'이라는 키값이 존재하여야 합니다.")

        if "status" not in target_data.keys():
            raise KeyError("장비 오브젝트를 생성하기 위해서는 Dict데이터에 'status'이라는 키값이 존재하여야 합니다.")

        if "equip_type" not in target_data.keys():
            raise KeyError("장비 오브젝트를 생성하기 위해서는 Dict데이터에 'equip_type'이라는 키값이 존재하여야 합니다.")

        if "is_chest" not in target_data.keys():
            raise KeyError("장비 오브젝트를 생성하기 위해서는 Dict데이터에 'is_chest'이라는 키값이 존재하여야 합니다.")

        if "is_exclusive" not in target_data.keys():
            raise KeyError("장비 오브젝트를 생성하기 위해서는 Dict데이터에 'is_exclusive'이라는 키값이 존재하여야 합니다.")

        if "is_limited" not in target_data.keys():
            raise KeyError("장비 오브젝트를 생성하기 위해서는 Dict데이터에 'is_limited'이라는 키값이 존재하여야 합니다.")

        equipment_data_object = ItemEquipmentData(
            name = target_data.get("name"),
            grade = target_data.get("grade"),
            equip_point = target_data.get("equip_point"),
            status = target_data.get("status"),
            equip_type= target_data.get("equip_type"),
            is_chest = target_data.get("is_chest"),
            is_exclusive = target_data.get("is_exclusive"),
            is_limited = target_data.get("is_limited")
        )

        return equipment_data_object


