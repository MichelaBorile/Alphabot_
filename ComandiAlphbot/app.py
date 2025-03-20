from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from AlphaBot import AlphaBot
import jwt
import datetime
import sqlite3 as sql

app = Flask(__name__)
global username_global

app = Flask(__name__)

a = AlphaBot()
a.stop()

@app.route("/home", methods=["GET"])
def home():
    global username_global
    if request.cookies.get('accesso_cookie'):
        username_global = request.cookies.get('accesso_cookie')
    return render_template("home.html", username=username_global)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.cookies.get('accesso_cookie'):
        return redirect(url_for("home"))
    else: 
        if request.method == "POST":
            email = request.form["e-mail"]
            password = request.form["password"]
            return validate(email, password)
        return render_template("login.html")


@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        email = request.form["e-mail"]
        password = request.form["password"]
        conn = sql.connect("users.db")
        cur = conn.cursor()
        cur.execute(f"""SELECT 1
                        FROM users
                        WHERE email LIKE '{email}'""")
        user = cur.fetchone()
        if user == None:
            cur.execute(f"""INSERT INTO users (email, password)
                            VALUES ('{email}', '{generate_password_hash(password)}')""")
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        else:
            # utente già esistente
            pass
    return render_template("create_account.html")


@app.route("/logout")
def logout():
    resp = redirect(url_for("login"))
    resp.set_cookie('accesso_cookie', '', expires=0)
    return resp

def validate(username, password):
    global username_global
    conn = sql.connect("users.db")
    cur = conn.cursor()
    cur.execute(f"""SELECT users.password
                    FROM users
                    WHERE email LIKE '{username}'""")
    pswd = cur.fetchone()
    if pswd and check_password_hash(pswd[0], password):
        username_global = username
        resp = redirect(url_for("home"))
        resp.set_cookie('accesso_cookie', username, max_age=60*60*24)
        return resp
    return render_template("login.html", alert="Invalid credentials")

@app.route("/control", methods=["GET", "POST"])
def control():
    if request.method == 'POST':
            if request.form.get('AVANTI') == 'AVANTI':
                print("movimento: avanti")
                a.forward()
            elif request.form.get('INDIETRO') == 'INDIETRO':
                print("movimento: indietro")
                a.backward()
            elif request.form.get('SINISTRA') == 'SINISTRA':
                print("movimento: sinistra")
                a.left()
            elif request.form.get('DESTRA') == 'DESTRA':
                print("movimento: destra")
                a.right()
            elif request.form.get('FERMO') == 'FERMO':
                print("movimento: fermo")
                a.stop()
            else:
                print("Comando sconosciuto")
    return render_template("control.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4444)
