import os

from flask import Flask, render_template, redirect

from DataBaseController import DataBaseController
from src.views import SimulatorView, MainView, TestView

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
database_controller = DataBaseController("Development_Database")


app.register_blueprint(SimulatorView.BP)
app.register_blueprint(MainView.BP)
# app.register_blueprint(TestView.BP)

@app.route('/')
def Greeting():
    return render_template("Main/Greeting.html")


if __name__ == '__main__':
    app.secret_key = "RevivedWitch" #UUID 사용예정
    host_dict = {
        "home": "192.168.212.4",
        "school_wifi": "172.16.25.48",
        "school_tethering": "192.168.20.12"
    }
    app.run()
