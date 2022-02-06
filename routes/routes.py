from app import app
from flask import render_template, request, redirect

@app.route("/")
def index():
    return render_template("index.html", title="Notebooks")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    # user & pass check  

    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 3 or len(username) > 20:
            return render_template("error.html", redirect="/register", message="Username too short or long")

        password = request.form["password1"]
        password_again = request.form["password2"]

        if len(password) < 4:
            return render_template("error.html", redirect="/register", message="Password too short")

        if password != password_again:
            return render_template("error.html", redirect="/register", message="Passwords dont match")

