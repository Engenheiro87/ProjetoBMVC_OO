from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file, post, error, abort;
from bottle import redirect, template, response
from colorama import init, Fore, Style;
from uuid import uuid4;

app = Bottle()
ctl = Application()


init(autoreset=True);
#-----------------------------------------------------------------------------
# Rotas:

# ERRORS
@app.error(404)
@app.error(500)
def error_page(error):
    return ctl.render("error", parameter={"status_line":vars(error)["_status_line"], "body":vars(error)["body"]});


@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route("/")
@app.route('/home')
def home(info=None):
    if not ctl.is_authenticated():
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
    result, note = ctl.get_service("UserService").register_user(name=name, email=email, password=password, gender=gender, workouts=[], accountID=str(uuid4()));
    if result == False:
        return signup(note=note);
    ctl.do_logout(); # Makes sure you're not redirected back to home in an already logged in account.
    redirect("/login");

#LOG IN
@app.route("/login", method="GET")
def login(message=None):
    if ctl.is_authenticated():
        return redirect("/home");
    return ctl.render("login", message);

@app.route("/logged_in", method="POST")
def do_login():
    email = request.forms.get("email_box");
    password = request.forms.get("password_box");
    sucess, sessionID_warn = ctl.do_login(email, password);
    if sucess == False:
        return login(message=sessionID_warn);
    response.set_cookie("sessionID", sessionID_warn, httponly=True, secure=True, max_age = 15*60);
    redirect("/profile");

@app.route("/logout", method="GET")
def logout():
    ctl.do_logout();
    response.delete_cookie("sessionID");
    return redirect("/login");

#PROFILE
@app.route("/profile", method="GET")
def profile():
    user = ctl.is_authenticated() and ctl.get_session_id();
    if user==False:
        return redirect("/login");
    return ctl.render("profile", user);

# WORKOUT CREATION
@app.route("/workout_creation", method="GET")
def workout_creation():
    if not ctl.is_authenticated():
        return redirect("/login");
    return ctl.render("workout_creation");

@app.route("/create_workout", method="POST")
def create_workout():
    payload = request.json;
    sucess, error = ctl.get_service("WorkoutService").create_workout(ctl.get_session_id(), payload);
    if not sucess:
        print(Fore.RED+f"Error: {error}");
    return {
        "sucess":sucess,
        "error":error or None,
    }

@app.route("/delete_workout", method="POST")
def delete_workout():
    payload = request.json;
    sucess, error = ctl.get_service("WorkoutService").delete_workout(ctl.get_session_id(), payload);
    return {
        "sucess":sucess,
        "error":error
    };

@app.route("/workout_view", method="GET")
@app.route("/workout_view/<workout_id>", method="GET")
def workout_view(workout_id=None):
    if not workout_id:
        print(Fore.RED+"No workout_id given.");
        return redirect("/profile");
    if not ctl.is_authenticated():
        print(Fore.RED+"Nobody logged in.");
        return redirect("/login");
    return ctl.render("workout_view", parameter=workout_id);

@app.route("/mark_workout_done", method="POST")
def mark_exercise_done():
    payload = request.json;
    sucess, error = ctl.get_service("WorkoutService").complete_exercise(ctl.get_session_id(), payload);
    if not sucess:
        print(Fore.RED+f"Error: {error}");
        return redirect("/login");
    return {
        "sucess":sucess,
        "error":error
    };

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
