from flask import Flask,render_template,redirect,url_for,request,session, send_file
from flask_cors import CORS, cross_origin
from supabase import create_client, Client
import pycryp
import markdown
import json,os,random
from datetime import timedelta
import cv2
import qrcode
import numpy as np
import sys
import time

app = Flask(__name__)
CORS(app, origins="https://projectzeta.vercel.app")
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days=30)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route('/')
def index():
    session['isLoggedin'] = False
    return render_template("landing/index.html")


@app.route('/login',methods=["POST","GET"])
def login():
    try:
        if session['isLoggedin']==True:
            print("Logged in", flush=True)
            return redirect("/level")
        else:
            print("Not Logged in", flush=True)
            return render_template("login/index.html")
    except:
        print("Not Logged in", flush=True)
        return render_template("login/index.html")

@app.route('/auth',methods=["POST","GET"])

def auth():
    data = request.form
    username = data["username"]
    password = data["password"]

    password_data = supabase.table("user").select("password").eq("username", username).execute()
    password_data = password_data.data[0]["password"].encode()

    try:
        if password==pycryp.decrypt(password_data, password).decode():
            session["isLoggedin"] = True
            session["user"] = username
            print("Correct", flush=True)
            return redirect("/level")
    except:
        print("Incorrect", flush=True)
        return render_template("login/index.html")

@app.route('/reg',methods=["POST","GET"])
def reg():
    return render_template("reg/index.html")

@app.route('/new_user',methods=["POST"])

def new_user():
    data = request.form
    username = data["username"]
    print(username, flush=True)
    email = data["email"]
    password = data["password"]
    confirm_password = data["confirm_password"]
    if password == confirm_password:
        try:
            print("Creating User", flush=True)
            password = pycryp.encrypt(password, password).decode()
            data = supabase.table("user").insert({"username": username, "email": email, "password": password}).execute()
            progress = supabase.table("progress").insert({"username": username, "current_level": 1, "password_set": random.randint(1, 5)}).execute()
            session["isLoggedin"] = True
            session["user"] = username
            return redirect(url_for("login"))
        except Exception as e:
            return redirect(url_for("reg"))
    else:
        return render_template("reg/index.html")


@app.route('/level')

def route():
    if session["isLoggedin"]:
        current_user = session["user"]
        current_level = supabase.table("progress").select("current_level").eq("username", current_user).execute()
        current_level = current_level.data[0]["current_level"]
        password_set = supabase.table("progress").select("password_set").eq("username", current_user).execute()
        password_set = password_set.data[0]["password_set"]
        f = open("password.json", "r")
        f_ = open("hint.json", "r")
        hints = json.load(f_)
        hint = hints[str(current_level)]
        passwords = json.load(f)
        password = passwords[str(password_set)]
        return render_template("levels/{}/index.html".format(current_level),password=password,level=current_level,hint=hint)
    else:
        return redirect(url_for("login"))

@app.route('/increment',methods=["POST"])

def increment():
    if session["isLoggedin"]:
        try:
            data = request.form
            password = data["password"]
            password = password.lower()
            print(password, flush=True)
            f = open("password.json")
            passwords = json.load(f)
            correct_password = supabase.table("progress").select("password_set").eq("username", session["user"]).execute()
            correct_password = correct_password.data[0]["password_set"]
            current_level = supabase.table("progress").select("current_level").eq("username", session["user"]).execute()
            current_level = current_level.data[0]["current_level"]
            print(passwords[str(correct_password)][current_level], flush=True)
            if password == passwords[str(correct_password)][current_level]:
                current_user = session["user"]
                current_level = supabase.table("progress").select("current_level").eq("username", current_user).execute()
                current_level = current_level.data[0]["current_level"]
                supabase.table("progress").update({"current_level": current_level+1}).eq("username", current_user).execute()
                current_user = session["user"]
                current_level = supabase.table("progress").select("current_level").eq("username", current_user).execute()
                current_level = current_level.data[0]["current_level"]
                password_set = supabase.table("progress").select("password_set").eq("username", current_user).execute()
                password_set = password_set.data[0]["password_set"]
                f = open("password.json", "r")
                f_ = open("hint.json", "r")
                hints = json.load(f_)
                hint = hints[str(current_level)]
                passwords = json.load(f)
                password = passwords[str(password_set)]
                return render_template("levels/{}/index.html".format(current_level),password=password,level=current_level,hint=hint)
            else:
                    return redirect(url_for("login"))
        except:
                return redirect(url_for("login"))

@app.route('/edit')

def edit():
    return render_template("update.html")

@app.route('/update',methods=["POST"])

def update():
    data = request.form
    password = data["password"]
    level = data["level"]
    text = data["text"]
    f=open("templates/levels/{}/index.html".format(level),"w")
    text = markdown.markdown(text)
    new_text = "{% include 'base.html' %}\n"
    new_text = new_text + text
    f.write(new_text)
    f.close()
    return render_template("landing/index.html")


@app.route('/certificate')

def certificate():
    name = session["user"]
    print(name, flush=True)
    link = "https://sepolia.etherscan.io/tx/0xed31901130e1c5ed53744075a855d323f6051373ac0e395e3609b79fdcfdfce6"
    template = cv2.imread('static/certi.jpg')
    text = name
    if template is None:
        return render_template("404.html")
    text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)
    text_x = (template.shape[1] - text_size[0]) // 2
    text_y = (template.shape[0] + text_size[1]) // 2 - 150
    cv2.putText(template, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)
    qr_img = qrcode.make(link)
    qr_img = np.array(qr_img.convert('RGB'))
    qr_img = cv2.cvtColor(qr_img, cv2.COLOR_RGB2BGR)
    qr_img = cv2.resize(qr_img, (200, 200))
    qr_x = template.shape[1] - qr_img.shape[1] - 100
    qr_y = template.shape[0] - qr_img.shape[0] - 50 
    template[qr_y:qr_y + qr_img.shape[0], qr_x:qr_x + qr_img.shape[1]] = qr_img
    cv2.imwrite('static/certificate.jpg', template)
    return send_file('static/certificate.jpg', as_attachment=True)

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

if __name__ == '__main__':
    app.run()