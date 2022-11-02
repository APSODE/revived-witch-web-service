import os
import time

from flask import Blueprint, redirect, render_template, url_for, session, request, jsonify
from urllib.parse import quote

from src.functions.DataTools import DataTools
from src.functions.ImageTools import ImageTools
from src.functions.Simulator import Simulator
import base64
import uuid


BP = Blueprint("Simulator", __name__,
               url_prefix = "/simulator",
               template_folder = "../templates",
               static_folder = "../static"
               )


@BP.route("/", methods = ["GET", "POST"])
def Simulator_Main():
    if request.method == "GET":
        if session.get("banner") != session.get("bf_banner"):
            print(f"current banner : {session.get('banner')}")
            print(f"before banner : {session.get('bf_banner')}")

            print("gacha_count 값 초기화 진행")
            session["gacha_count"] = 0
            session["gacha_count_half"] = 0
            session["gacha_count_full"] = 0
        return render_template("Simulator/Simulator.html", result_img = None)
    else:
        banner_name = session.get("banner")
        if "gacha_count" not in session.keys():
            print("gacha_count의 값을 10으로 지정")
            session["gacha_count"] = 10
            session["gacha_count_half"] = 10
            session["gacha_count_full"] = 10
        else:
            print("gacha_count의 값을 10을 추가")
            session["gacha_count"] += 10
            session["gacha_count_half"] += 10
            session["gacha_count_full"] += 10
            print(f"gacha_count : {session.get('gacha_count')}")

        simulator = Simulator(
            banner_name = "영혼 소환" if banner_name is None else banner_name
        )
        current_banner_data = DataTools.GetBannerDataByBannerName(banner_name = banner_name)
        print(f"is pickup banner? : {current_banner_data.PickUpData.get('active')}")
        # gacha_result_doll_list = simulator.SimulatePickUpGacha(
        #     session=session
        # )

        gacha_result_doll_list = simulator.SimulateGacha()
        # if current_banner_data.PickUpData.get("active"):
        #     gacha_result_doll_list = simulator.SimulatePickUpGacha(
        #         session = session
        #     )
        #
        # else:
        #     gacha_result_doll_list = simulator.SimulateGacha()




        session["gacha_result_list"] = {}
        response_use_data = {}
        for doll_data_idx in range(len(gacha_result_doll_list)):
            doll_data = gacha_result_doll_list[doll_data_idx]
            gacha_num = doll_data_idx + 1
            session[f"{gacha_num}"] = doll_data.GetAllDollData()
            response_use_data[f"{gacha_num}"] = doll_data.GetAllDollData()


        IT = ImageTools()
        gacha_result_img = IT.MergeGachaBgImage(doll_object_list=gacha_result_doll_list)
        img_name = uuid.uuid4()

        # img_save_dir = os.path.dirname(os.path.dirname())
        from app import BASE_DIR
        img_save_dir = BASE_DIR + f"/static/img/gacha/result/{img_name}.png"
        f_time = time.perf_counter()
        gacha_result_img.save(img_save_dir)
        s_time = time.perf_counter()

        print(f"gacha_result_img.save() 소요시간 : {s_time - f_time}s")
        # encoded_gacha_result_img = base64.b64encode(gacha_result_img.tobytes()).decode()
        return_data = {
            "src": f"../static/img/gacha/result/{img_name}.png",
            "name": f"{img_name}",
            "result": response_use_data,
            "current_gacha_amount": session.get("gacha_count")
        }
        return jsonify(result_data = return_data)


@BP.route("/soul")
def Simulator_Main_Soul():
    session["bf_banner"] = session.get("banner")
    session["banner"] = f"영혼 소환"

    return redirect(url_for("Simulator.Simulator_Main"))


@BP.route("/mercury")
def Simulator_Main_Mercury():
    session["bf_banner"] = session.get("banner")
    session["banner"] = f"수은 원소 소환"

    return redirect(url_for("Simulator.Simulator_Main"))


@BP.route("/brimstone")
def Simulator_Main_Brimstone():
    session["bf_banner"] = session.get("banner")
    session["banner"] = f"유황 원소 소환"

    return redirect(url_for("Simulator.Simulator_Main"))


@BP.route("/saltstone")
def Simulator_Main_Saltstone():
    session["bf_banner"] = session.get("banner")
    session["banner"] = f"염석 원소 소환"

    return redirect(url_for("Simulator.Simulator_Main"))


@BP.route("/dream")
def Simulator_Main_Dream():
    session["bf_banner"] = session.get("banner")
    session["banner"] = f"꿈의 소환"

    return redirect(url_for("Simulator.Simulator_Main"))

@BP.route("/stack_clear")
def Simulator_Main_StackClear():
    session["gacha_count"] = 0
    session["gacha_count_half"] = 0
    session["gacha_count_full"] = 0

    return redirect(url_for("Simulator.Simulator_Main"))
# @BP.route("/<img_file_bin>")
# def Simulator_Main_s(img_file_bin = None):
#     return render_template("Simulator/Simulator.html", img_file_bin = img_file_bin)

# @BP.route("/", methods = ["POST"])
# def Simulator_Run():
# #
#     simulator = Simulator(
#         banner_name = "영혼 소환"
#     )
#     data = request.get_json()
#     print(data)
#     print(type(data))
#
#     gacha_result_doll_list = simulator.SimulateGacha()
#     IT = ImageTools()
#     gacha_result_img = IT.MergeGachaBgImage(doll_object_list = gacha_result_doll_list)
#     encoded_gacha_result_img = base64.b64encode(gacha_result_img.tobytes()).decode("ascii")
#     return_data = {
#         "src": quote(encoded_gacha_result_img)
#     }
#
#     return jsonify(result_data = return_data)
#     # return jsonify(result = "success", rdata = return_data)
#     # return f'<img src="data:image/png;base64,{encoded_gacha_result_img}">'
#
# @BP.route("/simulate_run")
# def Test():
#     simulator = Simulator(
#         banner_name = "영혼 소환"
#     )
#     # data = request.get_json()
#     # print(data)
#     # print(type(data))
#
#     gacha_result_doll_list = simulator.SimulateGacha()
#     IT = ImageTools()
#     gacha_result_img = IT.MergeGachaBgImage(doll_object_list=gacha_result_doll_list)
#     encoded_gacha_result_img = base64.b64encode(gacha_result_img.tobytes())
#
#     # return render_template("Simulator/Simulator.html", result_img = encoded_gacha_result_img)
#     return redirect(url_for("Simulator.Simulator_Main"), result_img = encoded_gacha_result_img)
