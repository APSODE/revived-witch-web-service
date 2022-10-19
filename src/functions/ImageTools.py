import time

from PIL import Image


from database.models.gacha_doll_model import DollData, Doll
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
        gacha_background_image = Image.open(BASE_DIR + f"\\static\\img\\gacha\\background\\gacha_background.png")
        for doll_object_idx in range(len(doll_object_list)):
            doll_object = doll_object_list[doll_object_idx]
            doll_num = doll_object_idx + 1
            doll_image = Image.open(BASE_DIR + f"\\static\\img\\gacha\\doll\\{doll_object.Name}.png")
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

    def ImageNameChanger(self):
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


