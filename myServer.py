from flask import Flask

print("Starting script:" + __name__)
app = Flask(__name__)


@app.route("/")
def hello():
    return "hello world"


@app.route("/test")
def test():
    return "hello world this is test"
