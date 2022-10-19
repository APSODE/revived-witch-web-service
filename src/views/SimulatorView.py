import os
import time

from flask import Blueprint, redirect, render_template, url_for, session, request, jsonify
from urllib.parse import quote
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
        return render_template("Simulator/Simulator.html", result_img = None)
    else:
        banner = session.get("banner")
        simulator = Simulator(
            banner_name = "영혼 소환" if banner is None else banner
        )

        gacha_result_doll_list = simulator.SimulateGacha()
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
        img_save_dir = BASE_DIR + f"\\static\\img\\result\\{img_name}.png"
        f_time = time.perf_counter()
        gacha_result_img.save(img_save_dir)
        s_time = time.perf_counter()

        print(f"gacha_result_img.save() 소요시간 : {s_time - f_time}s")
        # encoded_gacha_result_img = base64.b64encode(gacha_result_img.tobytes()).decode()
        return_data = {
            "src": f"../static/img/result/{img_name}.png",
            "name": f"{img_name}",
            "result": response_use_data
        }
        return jsonify(result_data = return_data)

@BP.route("/soul")
def Simulator_Main_Soul():
    session["banner"] = f"영혼 소환"
    return redirect(url_for("Simulator.Simulator_Main"))

@BP.route("/mercury")
def Simulator_Main_Mercury():
    session["banner"] = f"수은 원소 소환"
    return redirect(url_for("Simulator.Simulator_Main"))

@BP.route("/brimstone")
def Simulator_Main_Brimstone():
    session["banner"] = f"유황 원소 소환"
    return redirect(url_for("Simulator.Simulator_Main"))

@BP.route("/saltstone")
def Simulator_Main_Saltstone():
    session["banner"] = f"염석 원소 소환"
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