from flask import Blueprint, redirect, render_template, url_for, request, jsonify



BP = Blueprint("Test", __name__,
               url_prefix = "/test",
               template_folder = "../templates",
               static_folder = "../static",
               )

@BP.route("/dashboard")
def TestDashboard():
    return render_template("TestTemplates/Dashboard_Test.html")

@BP.route("/cover")
def TestCover():
    return render_template("TestTemplates/Cover_Test.html")

@BP.route("/ajax")
def TestAjax():
    return render_template("TestTemplates/Ajax_Test.html")

@BP.route('/ajax', methods=['POST'])
def Ajax():
    data = request.get_json()
    print(data)

    return jsonify(result = "success", result2= data)

@BP.route("/footer")
def TestFooter():
    return render_template("TestTemplates/Footer_Test.html")

@BP.route("/starter")
def TestStarter():
    return render_template("TestTemplates/Starter_Test.html")
