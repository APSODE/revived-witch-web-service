


class DollData:
    def __init__(self, NAME: str, GRADE: str, ELEMENT: str, DOLL_CLASS: str, LIMITED: bool):
        self._NAME = NAME
        self._GRADE = GRADE
        self._ELEMENT = ELEMENT
        self._DOLL_CLASS = DOLL_CLASS
        self._LIMITED = LIMITED


    @property
    def Name(self) -> str:
        return self._NAME

    @property
    def Grade(self) -> str:
        return self._GRADE

    @property
    def Element(self) -> str:
        return self._ELEMENT

    @property
    def DollClass(self) -> str:
        return self._DOLL_CLASS

    @property
    def IsLimited(self) -> bool:
        return self._LIMITED


    def GetAllDollData(self) -> dict:
        """
        :return : RT_DATA = {
            "NAME": self._NAME,
            "GRADE": self._GRADE,
            "ELEMENT": self._ELEMENT,
            "DOLL_CLASS": self._DOLL_CLASS,
            "LIMITED": self._LIMITED
        }
        """
        RT_DATA = {
            "NAME": self._NAME,
            "GRADE": self._GRADE,
            "ELEMENT": self._ELEMENT,
            "DOLL_CLASS": self._DOLL_CLASS,
            "LIMITED": self._LIMITED
        }

        return RT_DATA


    def __repr__(self):
        RT_STR = f"\n=================================\n" \
                 f"NAME : {self._NAME}\n" \
                 f"GRADE: {self._GRADE}\n" \
                 f"ELEMENT: {self._ELEMENT}\n" \
                 f"DOLL_CLASS: {self._DOLL_CLASS}\n" \
                 f"LIMITED: {self._LIMITED}\n" \
                 f"\n=================================\n"

        return RT_STR


class Doll:
    @staticmethod
    def SerializeData(target_data: dict) -> DollData:
        return DollData(
            NAME = target_data.get("NAME"),
            GRADE = target_data.get("GRADE"),
            ELEMENT = target_data.get("ELEMENT"),
            DOLL_CLASS = target_data.get("DOLL_CLASS"),
            LIMITED = target_data.get("LIMITED")
        )
