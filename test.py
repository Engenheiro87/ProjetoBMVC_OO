class User:
    def __init__(self, name:str):
        self.__name = name;

    @property
    def name(self):
        return self.__name;

    @name.setter
    def name(self, new_value):
        return False;

user1 = User("Henrique");
print(user1.name);
print(user1.Name = "Michael Jackson");
