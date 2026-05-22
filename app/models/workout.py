class Workout:
    LIBRARY = {
        "A" : {
            "class": "Chest/Triceps/Abdomen",
            "thumb":"https://images.pexels.com/photos/5327536/pexels-photo-5327536.jpeg?_gl=1*ki6fkp*_ga*Mzk3Mzc4MDg5LjE3Nzg4ODkwNzA.*_ga_8JE65Q40S6*czE3Nzk0NDY1ODgkbzIkZzEkdDE3Nzk0NDY2MzMkajE1JGwwJGgw",
            "color":"green",
        },
        "B" : {
            "class": "Back/Biceps/Shoulders",
            "thumb":"https://images.pexels.com/photos/5327536/pexels-photo-5327536.jpeg?_gl=1*ki6fkp*_ga*Mzk3Mzc4MDg5LjE3Nzg4ODkwNzA.*_ga_8JE65Q40S6*czE3Nzk0NDY1ODgkbzIkZzEkdDE3Nzk0NDY2MzMkajE1JGwwJGgw",
            "color":"blue",
        },
        "C" : {
            "class": "Legs/Quadriceps",
            "thumb":"https://images.pexels.com/photos/5327536/pexels-photo-5327536.jpeg?_gl=1*ki6fkp*_ga*Mzk3Mzc4MDg5LjE3Nzg4ODkwNzA.*_ga_8JE65Q40S6*czE3Nzk0NDY1ODgkbzIkZzEkdDE3Nzk0NDY2MzMkajE1JGwwJGgw",
            "color":"orange",
        },
    }
    def __init__(self, workout_class:str, creatorID:str):
        self.workout_class = workout_class;
        self.__creatorID = creatorID;

    @property
    def creatorID(self)->str:
        return self.__creatorID;

class Exercise:
    pass;