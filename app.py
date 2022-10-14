from flask import Flask
from src.views import SimulatorView, MainView

app = Flask(__name__)
app.register_blueprint(SimulatorView.BP)
app.register_blueprint(MainView.BP)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(port = 30119, debug = True)

