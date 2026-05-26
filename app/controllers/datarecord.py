from app.models.user_account import UserAccount
from app.models.workout import ExerciseTemplate, Workout;
import json;
import uuid;

class DataRecord():
    """Banco de dados JSON para o recurso Usuários"""

    def __init__(self):
        self.__user_accounts= [] # banco (json)
        self.__authenticated_users = {};

        self.__exercises = [];
        self.read();
        
    def read(self):
        try:
            # READING USERS
            with open("app/controllers/db/user_accounts.json", "r", encoding="utf-8") as arquivo_json:
                user_data = json.load(arquivo_json)
                self.__user_accounts = [UserAccount(self.read_user_data(data)) for data in user_data] # unpack dictionary and give as arguments for user creation.

            # READING EXERCISES
            with open("app/controllers/db/exercises.json", "r", encoding="utf-8") as exercises_json:
                exercise_data = json.load(exercises_json);
                self.__exercises = {data["exercise_id"]:ExerciseTemplate(data) for data in exercise_data};

        except FileNotFoundError:
            with open("app/controllers/db/user_accounts.json", "w", encoding="utf-8") as arquivo_json:
                json.dump([], arquivo_json, indent=4);
            return self.read();

    # EXERCISE METHODS
    def get_exercise_template(self, exercise_id:str)->ExerciseTemplate|None:
        return self.__exercises.get(exercise_id, None);

    # USER METHODS

    def read_user_data(self, data:dict)->dict:
        treated_data = {};
        for key, value in data.items():
            # Exceptions
            if key == "workouts":
                treated_data.update({"workouts":[Workout(**workout_data) for workout_data in data["workouts"]]})
                continue;
            treated_data[key] = value;
        return treated_data;
    
    def book(self, user:UserAccount):
        self.__user_accounts.append(user);
        with open("app/controllers/db/user_accounts.json", "w", encoding="utf-8") as arquivo_json:
            user_data = [self.zip_data(user_account) for user_account in self.__user_accounts];
            json.dump(user_data, arquivo_json, indent=4);

    def zip_data(self, user:UserAccount)->dict:
        """
        Takes care of how the user's data will be saved (allowing the creation of private attributes)
        """
        return {
            "name": user.name,
            "password": user.password,
            "email": user.email,
            "gender": user.gender,
            "accountID":user.accountID,
            "workouts":user.workouts,
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