from bottle import template, redirect, request;
from app.controllers.datarecord import DataRecord;
from colorama import init, Fore, Style
from uuid import uuid4;

from app.models.user_account import UserAccount;
from app.models.workout import Workout, ExerciseUser;

init(autoreset=True);
class Application():

    def __init__(self):
        self.pages = {
            "signup":self.signup,
            "login":self.login,
            "profile":self.profile,
            "workout_creation":self.workout_creation,

            # errors
            "error":self.error_call,
        };
        self.__model = DataRecord();
        self.__LOGGED_USER = self.get_session_id();
        self.__authenticated_users = {};

        self.__current_loginusername = None;
        self.__current_username = None;
    
        self.services = {
            "UserService":UserService(data_model=self.__model),
            "WorkoutService":WorkoutService(data_model=self.__model, app=self)
        }

    def get_service(self, service:str):
        return self.services.get(service, None);

    def render(self,page, parameter=None):# parameter=username
       content = self.pages.get(page, self.home)
       if parameter:   
            return content(parameter);
       else:
            return content();
           
    def get_session_id(self):
        return request.get_cookie("sessionID");

    def from_session_id(self, session_id:str)->UserAccount|None:
        return self.__authenticated_users.get(session_id, None);

    # PAGES
    def workout_creation(self):
        return template(
            "app/views/html/workout_creation/work",
            exercise_templates={
                workout_class:self.__model.get_templates_by_class(workout_class) 
                for workout_class in Workout.LIBRARY.keys()
            }
            );

    def error_call(self, payload:dict):
        return template("app/views/html/error", payload=payload);

    def home(self):
        return template('app/views/html/index');

    def signup(self, note=None):
        return template("app/views/html/signup", note=note);

    def login(self, note=None):
        return template("app/views/html/log_in", note=note);

    def profile(self, session_id:str):
        user = self.__authenticated_users[session_id];
        return template(
            "app/views/html/profile_page/profile",
            name=str.capitalize(user.name),
            nick = str.capitalize(user.name.split()[0]),
            workouts = user.workouts,
        )

    def pagina(self, username=None):
        if self.is_authenticated(username):
            session_id = self.get_session_id();
            user = self.__model.getCurrentUser(session_id);
            return template("app/views/html/pagina", current_user=user, transfered=True, data=user);
        else:
            return self.portal();
    

    # OTHER METHODS
    def is_authenticated(self, session_id=None)->bool:
        session_id = session_id or self.get_session_id();
        return session_id in self.__authenticated_users;

    def authenticate_user(self, username, password):
        session_id = self.__model.checkUser(username, password);
        if session_id:
            self.logout_user();
            self.__current_username = self.__model.getUserName(session_id);
            return session_id, username;
        return None;

    def do_login(self, email:str, password:str):
        user:UserAccount = self.__model.get_user(email, password);
        if not user:
            return False, "No account found.";
        session_id = str(uuid4());
        self.__authenticated_users[session_id] = user;
        self.__LOGGED_USER = session_id;
        return True, session_id;

    def do_logout(self):
        session_id = self.get_session_id();
        if session_id in self.__authenticated_users:
            self.__authenticated_users.pop(session_id);
        self.__LOGGED_USER = None;

    def logout_user(self):
        self.__current_username = None;
        session_id = self.get_session_id();
        if session_id:
            self.__model.logout(session_id);

    @property
    def LOGGED_USER(self)->str|None:
        session_id = self.get_session_id();
        return session_id or None;

class UserService:
    def __init__(self, data_model:DataRecord):
        self.__data_model = data_model;

    def register_user(self, **properties):
        if self.__data_model.get_user(properties["email"], properties["password"]):
            return False;
        self.__data_model.book(UserAccount(properties));

class WorkoutService():
    def __init__(self, data_model:DataRecord, app:Application):
        self.__data_model = data_model;
        self.__app = app;

    def create_workout(self, session_id:str, payload:dict):
        user = self.__app.from_session_id(session_id);
        if not user:
            return False, "Couldn't find this user.";
        if not payload:
            return False, "No payload sent.";
        workout_class = self.get_class_from_json(payload["exercises"]);
        workout = self.__data_model.create_workout_from_json(
            {
                "workout_class":workout_class,
                "creatorID":user.accountID,
                "exercises": self.parse_exercise_list(payload["exercises"]),
            }
        );
        user.add_workout(workout);
        self.__data_model.save();
        return True, None;
    
    def parse_exercise_list(self, exercise_dict:dict)->list:
        """
        Transforms from JavaScript JSON into user_accounts JSON format.
        """
        return [{
            "unique_id": exercise_data.get("unique_id", str(uuid4())),
            "exercise_id":exercise_id,
            "info": {
                "reps":exercise_data.get("reps", 12),
            },
        } for exercise_id, exercise_data in exercise_dict.items()
        ];

    def get_class_from_json(self, json_exercises:dict)->str:
        last_type = None;
        for exercise in json_exercises.values():
            my_type = exercise["exercise_type"];
            if not last_type:
                last_type = my_type;
                continue;
            if my_type!=last_type:
                return "M";
        return last_type;