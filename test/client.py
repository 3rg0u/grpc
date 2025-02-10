from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template(template_name_or_list="index.html")


# @app.route('/read/<key>')
# def read(key):


if __name__ == "__main__":
    app.run(debug=True)
