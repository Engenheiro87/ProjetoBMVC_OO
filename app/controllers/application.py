from bottle import template, redirect, request;
from app.controllers.datarecord import DataRecord;


class Application():

    def __init__(self):
        self.pages = {
            "pagina":self.pagina,
            "portal":self.portal,
        };
        self.__model = DataRecord();
        self.__current_loginusername = None;
        self.__current_username = None;

    def render(self,page, parameter=None):# parameter=username
       content = self.pages.get(page, self.helper)
       if parameter:   
            return content(parameter);
       else:
            return content();
           
    def get_session_id(self):
        return request.get_cookie("session_id");

    def helper(self):
        return template('app/views/html/index');

    def portal(self, message=None):
        return template("app/views/html/portal", message=message);


    
    def pagina(self, username=None):
        if self.is_authenticated(username):
            session_id = self.get_session_id();
            user = self.__model.getCurrentUser(session_id);
            return template("app/views/html/pagina", current_user=user, transfered=True, data=user);
        else:
            return self.portal();
    
    def is_authenticated(self, username):
        session_id = self.get_session_id();
        current_username = self.__model.getUserName(session_id);
        return username==current_username;

    def user_exists(self, username, password)->bool:
        return self.__model.checkUser(username, password)!=None;

    def authenticate_user(self, username, password):
        session_id = self.__model.checkUser(username, password);
        if session_id:
            self.logout_user();
            self.__current_username = self.__model.getUserName(session_id);
            return session_id, username;
        return None;

    def logout_user(self):
        self.__current_username = None;
        session_id = self.get_session_id();
        if session_id:
            self.__model.logout(session_id);