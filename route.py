from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file, post
from bottle import redirect, template, response
from colorama import init, Fore, Style;

app = Bottle()
ctl = Application()


init(autoreset=True);
#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route("/")
@app.route('/home')
def home(info=None):
    if not ctl.LOGGED_USER:
        return redirect("/login");
    return profile();# TEMPORARY

@app.route("/pagina", methods=['GET'])
@app.route("/pagina/<username>", methods=["GET"])
def action_pagina(username=None):
    return ctl.render("pagina", username);

#SIGN UP
@app.route("/signup", method="GET")
def signup(note=None):
    return ctl.render("signup", note);

@app.route("/signed_up", method="POST")
def do_signup():
    name = request.forms.get("username_box");
    email = request.forms.get("email_box");
    password = request.forms.get("password_box");
    gender = request.forms.get("gender");
    result = ctl.get_service("UserService").register_user(name=name, email=email, password=password, gender=gender);
    if result == False:
        return signup(note="This user already exists, please try another combination.");
    ctl.do_logout();#Makes sure you're not redirected back to home in an already logged in account.
    redirect("/login");

#LOG IN
@app.route("/login", method="GET")
def login(message=None):
    if ctl.LOGGED_USER:
        return redirect("/home");
    return ctl.render("login", message);

@app.route("/logged_in", method="POST")
def do_login():
    email = request.forms.get("email_box");
    password = request.forms.get("password_box");
    sucess, user_warn = ctl.do_login(email, password);
    if sucess == False:
        return login(message=user_warn);
    redirect("/profile");

@app.route("/logout", method="GET")
def logout():
    ctl.do_logout();
    return redirect("/login");

#PROFILE
@app.route("/profile", method="GET")
def profile(user=None):
    user = user or ctl.LOGGED_USER;
    if user==None:
        return redirect("/login");
    return ctl.render("profile", user);

# OLD

@app.route("/portal", method="POST")
def action_portal():
    username = request.forms.get("username");
    password = request.forms.get("password");
    session_id, username = ctl.authenticate_user(username, password);
    if session_id:
        response.set_cookie("session_id", session_id, httponly=True, secure=True, max_age=3600);
        redirect(f"/pagina/{username}");

@app.route("/logout_old", method="POST")
def logout_old():
    ctl.logout_user();
    response.delete_cookie("session_id");
    redirect("/portal");
#-----------------------------------------------------------------------------
# Suas rotas aqui:



#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)
