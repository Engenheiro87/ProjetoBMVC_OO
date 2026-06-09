class UserAccount:
    def __init__(self, data:dict):
        self.name = data["name"];
        self.password = data["password"];
        self.email = data["email"];
        self.gender = data["gender"];
        self.__salt = data["salt"];
        self.__accountID = data["accountID"];
        self.__workouts = data.get("workouts", []);
    
    def __str__(self):
        return f"""
User: {self.name};
Password: {self.password};
Email: {self.email};
Gender: {self.gender};
AccountID: {self.accountID};
Workouts: {self.workouts};
Workout1: {self.workouts[0]};
"""

    def compare(self, email:str, password:str)->UserAccount|None:
        if email == self.email and password == self.password:
            return self;

    @property
    def salt(self):
        return self.__salt;

    @property
    def accountID(self)->str:
        return self.__accountID;

    @property
    def workouts(self)->list:
        return self.__workouts;

    def add_workout(self, workout):
        self.__workouts.append(workout);
    
    def remove_workout(self, workout_id:str):
        self.__workouts = [workout for workout in self.__workouts if workout.unique_id != workout_id];

    def pack_workouts(self)->list:
        return [workout.pack() for workout in self.__workouts];

    def get_workout_from_id(self, workout_id:str):
        for workout in self.__workouts:
            if workout.unique_id == workout_id:
                return workout;

    def pack(self):
        return {
            "name":self.name,
            "password":self.password,
            "salt":self.salt,
            "email":self.email,
            "gender":self.gender,
            "accountID":self.__accountID,
            "workouts":self.pack_workouts()
        };

    def get_workouts_by_day(self, day_number)->list:
        return [workout for workout in self.__workouts if day_number in workout.days];
