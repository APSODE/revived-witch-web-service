from flask import Blueprint, redirect, render_template, url_for, request, jsonify, session



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

@BP.route("/session")
def TestSession():
    return render_template("TestTemplates/Session_Test.html")

@BP.route("/session", methods = ['POST'])
def Session():
    print("호출 확인")
    data = request.get_json()
    session["session_test"] = 1
    return jsonify(result = "success", result2 = {"test": "test"})

@BP.route("/session_clear", methods = ['POST'])
def SessionClear():
    session.clear()
    print("세션 초기화 완료")
    return jsonify(result = "success", result2 = {"test": "test"})
