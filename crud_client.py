import logging

import grpc
import grpc._channel

from flask import Flask, render_template, request, flash, redirect

from __gen_key import gen_key
from crud_services.__service import Service

try:
    SERVICE = Service()
except grpc._channel._InactiveRpcError:
    print("Connection error!")

app = Flask(__name__)
app.secret_key = gen_key()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create", methods=["POST"])
def create():
    response = SERVICE.create(
        key=request.form.get("key"), value=request.form.get("value")
    )
    if response.status_code == 200:
        flash(message="created successfully", category="success")
    else:
        flash(message="key is already existed", category="error")

    return redirect("/")


@app.route("/read", methods=["GET"])
def read():
    response = SERVICE.read(key=request.args.get("key"))
    if response.status_code == 404:
        flash(message="key does not exist!", category="error")
        return redirect("/")
    return response.message


@app.route("/update", methods=["POST", "PUT"])
def update():
    response = SERVICE.update(
        key=request.form.get("key"), value=request.form.get("value")
    )
    if response.status_code == 404:
        flash(message="key does not exist!", category="error")
    else:
        flash(message="updated successfully!", category="success")
    return redirect("/")


@app.route("/delete", methods=["POST", "DELETE"])
def delete():
    response = SERVICE.delete(key=request.form.get("key"))
    if response.status_code == 404:
        flash(message="key does not exist!", category="error")
    else:
        flash(message="deleted successfully!", category="success")
    return redirect("/")


if __name__ == "__main__":

    logging.basicConfig()
    app.run(debug=True)
