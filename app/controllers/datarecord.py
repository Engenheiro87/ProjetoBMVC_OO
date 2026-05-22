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
                self.__user_accounts = [UserAccount(**data) for data in user_data] # unpack dictionary and give as arguments for user creation.
        except FileNotFoundError:
            with open("app/controllers/db/user_accounts.json", "w", encoding="utf-8") as arquivo_json:
                json.dump([], arquivo_json, indent=4);
            return self.read();
    
    def book(self, user:UserAccount):
        self.__user_accounts.append(user);
        with open("app/controllers/db/user_accounts.json", "w", encoding="utf-8") as arquivo_json:
            user_data = [self.zip_data(user_account) for user_account in self.__user_accounts];
            json.dump(user_data, arquivo_json, indent=4);

    def zip_data(self, user:UserAccount)->dict:
        return {
            "name": user.name,
            "password": user.password,
            "email": user.email,
            "gender": user.gender,
            "accountID":user.accountID,
        };
    
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

    def checkUser(self, email:str, password:str):
        for session_id, UserAccount in self.__authenticated_users.items():
            if UserAccount.compare(email, password):
                return session_id;
        for user in self.__user_accounts:
            if user.compare(email, password):
                session_id = str(uuid.uuid4()); # Id de sessão único
                self.__authenticated_users[session_id]=user;
                return session_id;

    def get_user(self, email:str, password:str)->UserAccount:
        for user in self.__user_accounts:
            if user.compare(email, password)!=None:
                return user;

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