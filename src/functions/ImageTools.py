import time

from random import *
from PIL import Image


from database.models.gacha_doll_model import DollData, Doll
from database.models.gacha_equip_model import ItemEquipmentData, ItemEquipment
from src.functions.DataTools import DataTools
import os


class ImageTools:
    def __init__(self):
        self._img_file_dir = ".\\static\\img\\"

    @staticmethod
    def MergeGachaBgImage(doll_object_list: [DollData]) -> Image:
        f_time = time.perf_counter()
        WORK_STATUS = True
        pos = [100, 0]
        from app import BASE_DIR
        gacha_background_image = Image.open(BASE_DIR + f"/static/img/gacha/background/gacha_background.png")
        for doll_object_idx in range(len(doll_object_list)):
            doll_object = doll_object_list[doll_object_idx]
            doll_num = doll_object_idx + 1
            doll_image = Image.open(BASE_DIR + f"/static/img/gacha/doll/{doll_object.Name}.png")
            doll_image = doll_image.resize((220, 703))
            if doll_num % 2 == 0:
                gacha_background_image.paste(doll_image, (pos[0], pos[1]), doll_image)
            else:
                gacha_background_image.paste(doll_image, (pos[0], pos[1] + 60), doll_image)
            pos[0] += 140
        s_time = time.perf_counter()

        print(f"MergeGachaBgImage 소요시간 : {s_time - f_time}s")
        return gacha_background_image
        # gacha_background_image.save("gacha_result_test.png")


    def MergeGachaImage(self, doll_object: DollData) -> bool:
        WORK_STATUS = True
        # """{ "NAME": self._NAME, "GRADE": self._GRADE, "ELEMENT": self._ELEMENT, "DOLL_CLASS": self._DOLL_CLASS, "LIMITED": self._LIMITED}"""
        try:
            doll_data = doll_object.GetAllDollData()

            doll_name = doll_data.get("NAME")

            doll_grade: str = doll_data.get("GRADE")
            doll_grade = doll_grade.lower()

            # doll_element = doll_data.get("ELEMENT")
            # doll_class = doll_data.get("DOLL_CLASS")
            # doll_limited = doll_data.get("LIMITED")


            grade_frame = Image.open(self._img_file_dir + f"gacha\\frame\\{doll_grade}_frame.png")
            frame_dot_img = Image.open(self._img_file_dir + "gacha\\frame\\frame_dot_img.png")
            doll_img = Image.open(self._img_file_dir + f"doll\\{doll_name}.png")
            grade_icon = Image.open(self._img_file_dir + f"gacha\\grade_icon\\{doll_grade}_icon.png")

            grade_frame.paste(doll_img, (81, 99), doll_img)
            grade_frame.paste(frame_dot_img, (87, 128), frame_dot_img)
            grade_frame.paste(grade_icon, (55, 633), grade_icon)
            # frame_dot_img.paste(grade_frame, (87, 131))
            grade_frame.save(self._img_file_dir + f"gacha\\doll\\{doll_name}.png")

        except:
            WORK_STATUS = False

        finally:
            return WORK_STATUS

    def MergeItemGachaBgImage(self, item_object: ItemEquipmentData = None) -> Image:
        from app import BASE_DIR
        item_dir = BASE_DIR + "/static/img/gacha/status_window/completion/"
        item_icon_dir = BASE_DIR + f"/static/img/item/equipment/chest/" \
                                        f"{item_object.ItemEquipGrade}/{item_object.ItemEquipPoint}/{item_object.ItemEquipType}/"
        bg_frame = Image.open(BASE_DIR + "/static/img/gacha/background/gacha_background_chest.png")
        item_image = Image.open(item_dir + item_object.ItemEquipName + ".png")
        item_icon_image = Image.open(item_icon_dir + item_object.ItemEquipName + ".png")

        # item_icon_image = item_icon_image.resize((400, 400))

        item_image = item_image.resize((440, 662))
        # bg_frame.paste(item_image, (1120, 29), item_image)
        # bg_frame.paste(item_icon_image, (400, 260), item_icon_image)

        bg_frame.paste(item_image, (1220, 29), item_image)
        bg_frame.paste(item_icon_image, (680, 260), item_icon_image)

        return bg_frame

    def MergeEquipFrameImage(self, equipment_object: ItemEquipmentData, type: str, directory: str = None) -> bool:
        WORK_STATUS = True
        try:
            equipment_name = equipment_object.ItemEquipName
            equipment_grade = equipment_object.ItemEquipGrade

            grade_frame = Image.open(self._img_file_dir + f"item\\equipment\\frame\\{equipment_grade}.png")
            if directory is not None:
                equipment_image = Image.open(self._img_file_dir + f"item\\equipment\\item\\{type}\\{directory}\\{equipment_name}.png")
            else:
                equipment_image = Image.open(self._img_file_dir + f"item\\equipment\\item\\{type}\\{equipment_name}.png")

            grade_frame.paste(equipment_image, (0, 0), equipment_image)

            grade_frame.save(self._img_file_dir + f"gacha\\{type}\\{equipment_name}.png")

        except Exception as MSG:
            WORK_STATUS = False
            print(MSG)

        finally:
            return WORK_STATUS


    def ImageNameChanger_Doll(self):
        IMG_NAME_STR = "루안,하은,파르페,아세라타,플레어,카밀리안,코타나,유년 아카샤,데비 다나,필레노시스,에티엥,아모레,아마나미 공주,린샤,샤논,카프라,안젤린,카시스 ,타카시,타마(4돌일러),아발렌 (4돌일러),타마(중복),아케론테(4돌),메타모포스(4돌),난나르,스반흐비트,아이돌 포크로어,옥타비아,미쿠,크로쉐,아우렐리아,아카샤,네메시,칼레도니아,포크로어,아발렌,파카네,프리뮬라,녹투르나,체르니,디시오스,엘라,미코토,굴베이그,케테스,바이올라,캐서린,키폰,유루구,세라냐,타마,아르카나,이리스,아케론테,우스피아,다나,메타모포스,시네티아,셔플,루즈,투오넬,유타야,아르디시아,노른,아빌,아마나미,루안,유이,라 크리마,안& 네로,하은(중복),파르페(중복),마야우엘,미나이어,마터웨이브,샤르,루다,힐다,페이,모티머,스이게츠,심브리엣,나샤,아네모네"
        IMG_NAME_LIST = IMG_NAME_STR.split(",")
        FILE_LIST = os.listdir(self._img_file_dir + "doll\\")
        for FILE_INDEX in range(FILE_LIST.__len__()):
            if FILE_LIST.__len__() == IMG_NAME_LIST.__len__():
                FILE = FILE_LIST[FILE_INDEX]
                NAME = IMG_NAME_LIST[FILE_INDEX]
                try:
                    os.rename(self._img_file_dir + "doll\\" + FILE, self._img_file_dir + "doll\\" + NAME + ".png")
                except:
                    os.rename(self._img_file_dir + "doll\\" + FILE, self._img_file_dir + "doll\\" + NAME + "1" + ".png")
            else:
                print("갯수가 다릅니다")
                break

    def ImageNameChanger_Item(self, name_list: list = None, item_type: str = "equipment", directory: str = "chest"):
        name_idx = 0
        if name_list == None:
            IMG_NAME_LIST = [
                "매혹_극야의 녹투르나",
                "화정의 장막_나샤",
                "파수꾼의 거울_난나르",
                "루미너스_다넬림",
                "영원의 수호_데비 다나",
                "고통의 가시_라판",
                "소생_린샤",
                "반짝이는 얼음_릴리아",
                "패러독스_마터웨이브",
                "이면의 가면_메타모포스",
                "창월_미나이어",
                "악의_밤의 아네모네",
                "베어 바턴_밤의 투오넬",
                "심야의 박쥐_베스티",
                "망각_산화",
                "원죄의 발현_샤르",
                "비상_세라냐",
                "얼어붙은 불꽃_스반흐비트",
                "배너티_심브리엣",
                "바다의 소리_아르디시아",
                "가릉빈_아마나미 공주",
                "임월천_아마나미",
                "평온한 꿈_아발렌",
                "생령_아세라타",
                "선율의 메아리_아이돌 포크로어",
                "별의 의지_아카샤",
                "페이탈 트랩_안젤린",
                "몽환의 꿈_에티엥",
                "행운의 하늘_엘라",
                "의식의 검_유년 아카샤",
                "구원의 빛_이사벨라",
                "신의 울음_카무이",
                "면액관_카밀리안",
                "플레임 스톰_카시스",
                "듀나이세겔_칼레도니아",
                "홀리 스웨어_캐서린",
                "신의 결재_코타나",
                "펄 오이스터_타카시",
                "유연한 선율_포크로어",
                "영광의 부적_영광의 부적",
                "시간의 원점_필레노시스",
                "환영의 열쇠_하은",
                "알현_노른",
                "붉은 소원_녹투르나",
                "약속의 지팡이_마야우엘",
                "인멸_셔플",
                "영원의 굴레_시네티아",
                "기만의 카드_아르카나",
                "화익의 진혼_아케론테",
                "바실리스크의 혼_우스피아",
                "종결의 소리_키폰"
            ]
            image_file_list = os.listdir(self._img_file_dir + "item\\equipment\\buffer\\")
        else:
            IMG_NAME_LIST = name_list
            image_file_list = os.listdir(self._img_file_dir + f"item\\{item_type}\\buffer\\")


        if image_file_list.__len__() == IMG_NAME_LIST.__len__():
            for exclusive_equip_image_file in image_file_list:
                os.rename(self._img_file_dir + f"item\\{item_type}\\buffer\\" + exclusive_equip_image_file, self._img_file_dir + f"item\\{item_type}\\{directory}\\" + IMG_NAME_LIST[name_idx] + ".png")
                name_idx += 1
        else:
            print(f"\n갯수가 다릅니다\n이미지 갯수 : {image_file_list.__len__()}개\n이미지 파일 이름의 갯수 : {IMG_NAME_LIST.__len__()}개")



    def CreateDollGachaResultImg(self):
        """모든 이미지파일 재합성 이므로 이미지 추가시에 사용하지 말것"""
        # database_controller = DataBaseController(db_name="Development_Database")
        from app import database_controller
        for doll_img_file in os.listdir(self._img_file_dir + "doll\\"):
            doll_img_file_name = doll_img_file.split(".")[0]
            if "(" in doll_img_file_name:
                doll_img_file_name = doll_img_file_name.split("(")[0]

            if doll_img_file_name[-1] == " ":
                doll_img_file_name = doll_img_file_name[:-1]

            query = {"NAME": doll_img_file_name}
            try:
                target_doll_data = Doll.SerializeData(
                    target_data = DataTools.DatabaseDollDataSerializer(
                        database_doll_data = database_controller.FindDatas(
                            collection_name = "Doll",
                            query = query,
                            find_one = True
                        )
                    )
                )
                self.MergeGachaImage(doll_object = target_doll_data)
            except:
                print(f"{query} : 인형 에러 발생")

    def ImageFileExistChecker(self) -> None:
        # database_controller = DataBaseController(db_name = "Development_Database")
        from app import database_controller
        doll_img_file_list = []
        for doll_img_file in os.listdir(self._img_file_dir + "doll\\"):
            doll_img_file_name = doll_img_file.split(".")[0]
            if "(" in doll_img_file_name:
                doll_img_file_name = doll_img_file_name.split("(")[0]

            if doll_img_file_name[-1] == " ":
                doll_img_file_name = doll_img_file_name[:-1]

            doll_img_file_list.append(doll_img_file_name)
        print("\n")
        for database_doll_data in database_controller.FindDatas(collection_name = "Doll"):
            doll_data_object = Doll.SerializeData(
                target_data = DataTools.DatabaseDollDataSerializer(
                    database_doll_data = database_doll_data
                )
            )
            if doll_data_object.Name not in doll_img_file_list:
                print(f"{doll_data_object.Name} 인형의 이미지 파일이 존재하지 않습니다.")


if __name__ == "__main__":
    pass


