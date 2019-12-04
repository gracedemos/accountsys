from flask import Flask, request, render_template, redirect, make_response
import json
import masspass
import numpy as np
import os

mp = masspass.masspass()
app = Flask(__name__)
auth_list = np.array([])

@app.route("/", methods = ["GET"])
def home():
    authentication = request.cookies.get("authentication")
    auth = 0
    for i in range(len(auth_list)):
        if(auth_list[i] == authentication):
            auth = 1
    if(auth == 1):
        return render_template("home.html")
    else:
        return redirect("/signin")
        
@app.route("/signin", methods = ["GET"])
def signin():
        return render_template("signin.html")
        
@app.route("/register", methods = ["GET"])
def register():
        return render_template("register.html")
        
@app.route("/register/submit", methods = ["POST"])
def register_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        acc = mp.prep(username, password)
        m_res = mp.add(acc)
        mp.finalize()
        if(m_res == "Addition Successful"):
            return redirect("/signin")
        else:
            return render_template("taken.html")
            
@app.route("/signin/submit", methods = ["POST"])
def signin_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        data = {"user": username, "pass": password}
        verify = mp.verify(data)
        if(verify == "Password Verified"):
                response = make_response(redirect("/"))
                auth = os.urandom(16).hex()
                global auth_list
                auth_list = np.append(auth_list, auth)
                response.set_cookie("authentication", auth)
                return response
        elif(verify == "Password Could Not Be Verified"):
                return redirect("/signin")
                
if(__name__ == "__main__"):
    app.run(host = "0.0.0.0", port = 80)