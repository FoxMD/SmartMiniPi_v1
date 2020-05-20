from flask import Flask, render_template, request

print("Starting script:" + __name__)
app = Flask(__name__)


@app.route("/")
def hello():
    items = ["Item 1", "Item 2", "Item 3"]

    return render_template("start.html", head="myHeader", items=items)


@app.route("/test")
def test():
    args = request.args
    name = args.get("name")
    print(name)
    return render_template("site1.html", param1=name)
