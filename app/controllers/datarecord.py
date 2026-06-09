from app.models.user_account import UserAccount
from app.models.workout import ExerciseTemplate, ExerciseUser, Workout;
from app.models.constraints import DAY_FORMAT1;
from datetime import datetime;
from uuid import uuid4;
import json;
import uuid;

class DataRecord():

    """Banco de dados JSON para o recurso Usuários"""

    def __init__(self):
        self.__user_accounts= [] # banco (json)
        self.__authenticated_users = {};

        self.__exercises = {};
        self.read();
        
    def read(self):
        try:
            # READING EXERCISES
            with open("app/controllers/db/exercises.json", "r", encoding="utf-8") as exercises_json:
                exercise_data = json.load(exercises_json);
                self.__exercises = {data["exercise_id"]:ExerciseTemplate(data) for data in exercise_data};

            # READING USERS
            with open("app/controllers/db/user_accounts.json", "r", encoding="utf-8") as arquivo_json:
                user_data = json.load(arquivo_json)
                self.__user_accounts = [UserAccount(self.read_user_data(data)) for data in user_data];

        except FileNotFoundError:
            with open("app/controllers/db/user_accounts.json", "w", encoding="utf-8") as arquivo_json:
                json.dump([], arquivo_json, indent=4);
            return self.read();

    # EXERCISE METHODS
    def get_exercise_template(self, exercise_id:str)->ExerciseTemplate|None:
        return self.__exercises.get(exercise_id, None);

    def get_templates_by_class(self, exercise_class)->ExerciseTemplate:
        return [
            exercise
            for exercise_id, exercise in self.__exercises.items()
            if exercise.exercise_class == exercise_class
        ];


    @property
    def exercise_templates(self)->dict:
        return self.__exercises;

    # WORKOUT METHODS
    def create_workout_from_json(self, json:dict)->Workout:
        return Workout(
            workout_class=json["workout_class"],
            creatorID=json["creatorID"],
            exercises=[
                ExerciseUser.from_template(
                    self.get_exercise_template(exercise["exercise_id"]),
                    exercise["unique_id"],
                    self.convert_to_datetime(exercise.get("last_completed", None)),
                    exercise["info"]
                )
                for exercise in json["exercises"]
            ],
            days = json["days"],
            unique_id= json["unique_id"]
        );

    def delete_workout(self, user:UserAccount, workout_id:str):
        user.remove_workout(workout_id);
        self.save();
    
    # DATE METHODS
    def convert_to_datetime(self, string=None)->datetime|None:
        if not string:
            return;
        return datetime.strptime(string, DAY_FORMAT1);

    # USER METHODS

    def read_user_data(self, data:dict)->dict:
        treated_data = {};
        for key, value in data.items():
            # Exceptions
            if key == "workouts":
                treated_data.update({"workouts":[self.create_workout_from_json(workout_data) for workout_data in data["workouts"]]});
                continue;
            treated_data[key] = value;
        return treated_data;
    
    def book(self, user:UserAccount):
        self.__user_accounts.append(user);
        with open("app/controllers/db/user_accounts.json", "w", encoding="utf-8") as arquivo_json:
            user_data = [self.zip_data(user_account) for user_account in self.__user_accounts];
            json.dump(user_data, arquivo_json, indent=4);

    def save(self):
        with open("app/controllers/db/user_accounts.json", "w", encoding="utf-8") as arquivo_json:
            data = [user.pack() for user in self.__user_accounts];
            json.dump(data, arquivo_json, indent=4);

    def zip_data(self, user:UserAccount)->dict:
        """
        Takes care of how the user's data will be saved (allowing the creation of private attributes)
        """
        return {
            "name": user.name,
            "password": user.password,
            "salt":user.salt,
            "email": user.email,
            "gender": user.gender,
            "accountID":user.accountID,
            "workouts":user.pack_workouts(),
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

    def get_user_from_email(self, email:str)->UserAccount|None:
        for user in self.__user_accounts:
            if user.email == email:
                return user;

    def get_user(self, email:str, password:str)->UserAccount:
        from_email = self.get_user_from_email(email);
        salt = from_email.salt;
        hashed, salt = SecurityService.hash_string(password, salt);
        for user in self.__user_accounts:
            if user.compare(email, hashed)!=None:
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
        
class SecurityService:
    @staticmethod
    def hash_string(string:str, salt:str=None):
        salt = salt or str(uuid4());
        string+=salt;
        hashed = 0;

        for char in string:
            hashed += hashed*31 + ord(char);
        
        return hashed, salt;