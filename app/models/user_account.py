class UserAccount:
    def __init__(self, data:dict):
        self.name = data["name"];
        self.password = data["password"];
        self.email = data["email"];
        self.gender = data["gender"];
        self.__accountID = data["accountID"];
        self.__workouts = data.get("workouts", []);
    
    def __str__(self):
        return f"{self.name} | {self.password} | {self.email}";

    def compare(self, email:str, password:str)->UserAccount|None:
        if email == self.email and password == self.password:
            return self;

    @property
    def accountID(self)->str:
        return self.__accountID;

    @property
    def workouts(self)->list:
        return self.__workouts;

