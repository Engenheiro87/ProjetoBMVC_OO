from app.models.user_account import UserAccount
import json;
import uuid;

class DataRecord():
    """Banco de dados JSON para o recurso Usuários"""

    def __init__(self):
        self.__user_accounts= [] # banco (json)
        self.__authenticated_users = {};
        self.read();
        
    def read(self):
        try:
            with open("app/controllers/db/user_accounts.json", "r") as arquivo_json:
                user_data = json.load(arquivo_json)
                self.__user_accounts = [UserAccount(**data) for data in user_data]
        except FileNotFoundError:
            self.__user_accounts.append(UserAccount("Guest", "010101", "101010"));
    
    def book(self, username, password):
        new_user = UserAccount(username, password);
        self.__user_accounts.append(new_user);
        with open("app/controllers/db/user_accounts.json", "w") as arquivo_json:
            user_data = [vars(user_account) for user_account in self.__user_accounts];
            json.dump(user_data, arquivo_json);
    
    def getCurrentUser(self, session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id];

    def getUserName(self, session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id].username;

    def getUserSessionId(self, username):
        for session_id in self.__authenticated_users:
            if username== self.__authenticated_users[session_id].username:
                return session_id;

    def checkUser(self, username, password):
        for user in self.__user_accounts:
            if user.username==username and user.password==password:
                session_id = str(uuid.uuid4()); # Id de sessão único
                self.__authenticated_users[session_id]=user;
                return session_id;

    def logout(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id];

    def work_with_parameter(self, parameter):
        try:
            index = int(parameter)  # Convertendo o parâmetro para inteiro
            if index <= self.limit:
                return self.user_accounts[index]
        except (ValueError, IndexError):
            return None  # Tratamento de erro se o índice for inválido