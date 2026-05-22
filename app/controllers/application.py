from bottle import template, redirect, request;
from app.controllers.datarecord import DataRecord;
from colorama import init, Fore, Style
from app.models.user_account import UserAccount;
from uuid import uuid4;


init(autoreset=True);
class Application():

    def __init__(self):
        self.pages = {
            "signup":self.signup,
            "login":self.login,
            "profile":self.profile,
        };
        self.__model = DataRecord();
        self.__LOGGED_USER = None;
        self.__authenticated_users = {};

        self.__current_loginusername = None;
        self.__current_username = None;
    
        self.services = {
            "UserService":UserService(data_model=self.__model),
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
        return request.get_cookie("session_id");

    # PAGES
    def home(self):
        return template('app/views/html/index');

    def signup(self, note=None):
        return template("app/views/html/signup", note=note);

    def login(self, note=None):
        return template("app/views/html/log_in", note=note);

    def profile(self, user:UserAccount):
        print("asked to render profile");
        return template(
            "app/views/html/profile_page/profile",
            name=user.name.capitalize(),
            nick = user.name.split()[0],
            workouts = [
                {
                    "class":"Chest/Triceps",
                    "thumb":"https://images.pexels.com/photos/5327536/pexels-photo-5327536.jpeg?_gl=1*ki6fkp*_ga*Mzk3Mzc4MDg5LjE3Nzg4ODkwNzA.*_ga_8JE65Q40S6*czE3Nzk0NDY1ODgkbzIkZzEkdDE3Nzk0NDY2MzMkajE1JGwwJGgw",
                    "color": "orange",
                },
                {
                    "class":"Back/Biceps",
                    "thumb":"https://images.pexels.com/photos/5327536/pexels-photo-5327536.jpeg?_gl=1*ki6fkp*_ga*Mzk3Mzc4MDg5LjE3Nzg4ODkwNzA.*_ga_8JE65Q40S6*czE3Nzk0NDY1ODgkbzIkZzEkdDE3Nzk0NDY2MzMkajE1JGwwJGgw",
                    "color":"blue",
                },
                {
                    "class":"Legs/Quadriceps",
                    "thumb":"https://images.pexels.com/photos/5327536/pexels-photo-5327536.jpeg?_gl=1*ki6fkp*_ga*Mzk3Mzc4MDg5LjE3Nzg4ODkwNzA.*_ga_8JE65Q40S6*czE3Nzk0NDY1ODgkbzIkZzEkdDE3Nzk0NDY2MzMkajE1JGwwJGgw",
                    "color":"green",
                }
            ]
        )

    def pagina(self, username=None):
        if self.is_authenticated(username):
            session_id = self.get_session_id();
            user = self.__model.getCurrentUser(session_id);
            return template("app/views/html/pagina", current_user=user, transfered=True, data=user);
        else:
            return self.portal();
    

    # OTHER METHODS
    def is_authenticated(self, username):
        session_id = self.get_session_id();
        current_username = self.__model.getUserName(session_id);
        return username==current_username;

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
        self.__LOGGED_USER = user;
        return True, user;

    def do_logout(self):
        print(f"logging out {self.__LOGGED_USER!=None}");
        self.__LOGGED_USER = None;

    def logout_user(self):
        self.__current_username = None;
        session_id = self.get_session_id();
        if session_id:
            self.__model.logout(session_id);

    @property
    def LOGGED_USER(self)->UserAccount:
        return self.__LOGGED_USER;

class UserService:
    def __init__(self, data_model:DataRecord):
        self.__data_model = data_model;

    def register_user(self, **properties):
        if self.__data_model.get_user(properties["email"], properties["password"]):
            return False;
        self.__data_model.book(UserAccount(**properties, accountID = str(uuid4())));
