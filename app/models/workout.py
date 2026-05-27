from uuid import uuid4;
from abc import ABC, abstractmethod;
from copy import deepcopy;

class Workout:
    LIBRARY = {
        "A" : {
            "class": "Chest/Triceps/Abdomen",
            "thumb":"https://images.pexels.com/photos/5327553/pexels-photo-5327553.jpeg",
            "color":"green",
        },
        "B" : {
            "class": "Back/Biceps/Shoulders",
            "thumb":"https://images.pexels.com/photos/10440731/pexels-photo-10440731.jpeg",
            "color":"blue",
        },
        "C" : {
            "class": "Legs/Quadriceps",
            "thumb":"https://images.pexels.com/photos/14673249/pexels-photo-14673249.jpeg",
            "color":"orange",
        },
    }
    def __init__(self, workout_class:str, creatorID:str, exercises:list):
        self.workout_class = workout_class;
        self.info = Workout.LIBRARY.get(workout_class);
        self.__creatorID = creatorID;
        self.__exercises = [ExerciseUser(**exercise_data) for exercise_data in exercises];

    @property
    def creatorID(self)->str:
        return self.__creatorID;

    @property
    def exercises(self):
        return self.__exercises;

    def get_exercise(self, uniqueID:str)->ExerciseUser:
        for exercise in self.__exercises:
            if exercise.unique_id == uniqueID:
                return exercise;

class Exercise(ABC):
    def __init__(self, info:dict):
        self.display_name = info["display_name"] or "Untitled Exercise";
        self.__exercise_id = info["exercise_id"];
        self.__reps = info["reps"];
        self.__info = deepcopy(info);
    
    @property
    def info(self):
        return self.__info;

    @property
    def exercise_id(self):
        return self.__exercise_id;

    @exercise_id.setter
    def exercise_id(self, value:str):
        self.__exercise_id = value;

    @property
    def reps(self):
        return self.__reps;

    @reps.setter
    def reps(self, value:int):
        self.__reps = value;

class ExerciseTemplate(Exercise):
    def __init__(self, info:dict):
        super().__init__(info);

    def get_info(self, info_name:str)->any:
        return self.__info.get(info_name, None);

    def get_info_copy(self):
        return deepcopy(self.__info);

class ExerciseUser(Exercise):
    def __init__(self, info:dict, unique_id:str):
        super().__init__(info);
        self.__unique_id = unique_id;
    
    @property
    def unique_id(self):
        return self.__unique_id;

    def increment_reps(self, increment:int):
        self.reps+=increment;

    def set_reps(self, new_value:int):
        self.reps = new_value;

    @classmethod
    def from_template(cls, template:ExerciseTemplate, uniqueID:str)->ExerciseUser:
        return cls(template.get_info_copy(), uniqueID);
