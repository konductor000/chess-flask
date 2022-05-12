from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "HELLO"


@app.route('/about')
def about():
    return "ABOUT"


if __name__ == "__main__":
    app.run(debug=True)