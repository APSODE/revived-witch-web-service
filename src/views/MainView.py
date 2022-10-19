from flask import Blueprint, render_template, redirect, url_for


BP = Blueprint("Main", __name__,
               url_prefix = "/main",
               template_folder = "../templates",
               static_folder = "../static"
               )

@BP.route("/")
def RevivedWitch_Main():
    return render_template("Frame/RevivedWitch_WebService_BaseFrame.html")


