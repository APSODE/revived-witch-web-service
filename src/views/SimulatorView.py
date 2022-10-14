from flask import Blueprint
from src.functions.Simulator import Simulator


BP = Blueprint("Simulator", __name__, url_prefix = "/simulator")

@BP.route("/")
def Simulator_Main():
    return "Simulator"

@BP.route("/run_simulate")
def Simulator_Run():
    simulator = Simulator(
        banner_name = "한정 소환"
    )
    RT_STR = ""
    RESULT = simulator.SimulateGacha()
    RT_STR += f"\n================가챠 결과===============\n"
    count = 1
    for R in RESULT:
        RT_STR += f"{R}\n"
        count += 1
    RT_STR += f"\n================가챠 결과===============\n"
    return RT_STR