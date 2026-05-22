class UserAccount:
    def __init__(self, name:str, password:str, email:str, gender:str):
        self.name = name;
        self.password = password;
        self.email = email;
        self.gender = gender;
    
    def __str__(self):
        return f"{self.name} | {self.password} | {self.email}";

    def compare(self, email:str, password:str)->UserAccount|None:
        if email == self.email and password == self.password:
            return self;