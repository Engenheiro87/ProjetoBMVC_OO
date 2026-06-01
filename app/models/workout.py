from uuid import uuid4;
from abc import ABC, abstractmethod;
from copy import deepcopy;

class Workout:
    LIBRARY = {
        "A" : {
            "ref":"PUSH",
            "class": "Chest/Triceps/Abdomen",
            "thumb":"https://images.pexels.com/photos/5327553/pexels-photo-5327553.jpeg",
            "color":"green",
        },
        "B" : {
            "ref":"PULL",
            "class": "Back/Biceps/Shoulders",
            "thumb":"https://images.pexels.com/photos/10440731/pexels-photo-10440731.jpeg",
            "color":"blue",
        },
        "C" : {
            "ref":"LEG",
            "class": "Legs/Quadriceps",
            "thumb":"https://images.pexels.com/photos/14673249/pexels-photo-14673249.jpeg",
            "color":"orange",
        },
        "M":{
            "ref":"MIX",
            "class": "Mixed",
            "thumb":"https://images.pexels.com/photos/5878683/pexels-photo-5878683.jpeg",
            "color":"red",
        }
    }
    def __init__(self, workout_class:str, creatorID:str, exercises:list, days:list):
        self.workout_class = workout_class;
        self.info = Workout.LIBRARY.get(workout_class);
        self.__creatorID = creatorID;
        self.__exercises = exercises;
        self.__days = days;
    
    def __str__(self):
        return f"""
Workout Class: {self.workout_class};
Class: {self.info["class"]};
CreatorID: {self.creatorID};
Exercises: {self.exercises};
Exercise1: {self.exercises[0]}

"""

    @property
    def creatorID(self)->str:
        return self.__creatorID;

    @property
    def exercises(self):
        return self.__exercises;

    @property
    def days(self):
        return self.__days;

    def get_exercise(self, uniqueID:str)->ExerciseUser:
        for exercise in self.__exercises:
            if exercise.unique_id == uniqueID:
                return exercise;

    def pack(self)->dict:
        return {
            "workout_class":self.workout_class,
            "creatorID":self.__creatorID,
            "days":self.__days,
            "exercises":[exercise.pack() for exercise in self.__exercises],
        };


class Exercise(ABC):
    def __init__(self, info:dict):
        self.display_name = info["display_name"] or "Untitled Exercise";
        self.__exercise_id = info["exercise_id"];
        self.__reps = info["reps"];
        self.__info = deepcopy(info);
        self.__class = Exercise.get_class(self.__exercise_id);
    
    def __str__(self):
        return f"""
Exercise: {self.display_name};
ExerciseID = {self.exercise_id};
Reps: {self.reps};
Info: {self.info};
"""
    
    @staticmethod
    def get_class(exercise_id)->str:
        for wclass, winfo in Workout.LIBRARY.items():
            if winfo["ref"] in exercise_id:
                return wclass;

    @property
    def info(self):
        return self.__info;

    @property
    def exercise_class(self):
        return self.__class;

    @property
    def exercise_type(self):
        return self.__info.get("exercise_type", "UD");

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

    @property
    def description(self):
        return self.__info.get("desc", "No description available.");

    

class ExerciseTemplate(Exercise):
    def __init__(self, info:dict):
        super().__init__(info);

    def get_info(self, info_name:str)->any:
        return self.info.get(info_name, None);

    def get_info_copy(self):
        return deepcopy(self.info);

class ExerciseUser(Exercise):
    def __init__(self, info:dict, unique_id:str, custom_info=None):
        if custom_info:
            for key, value in custom_info.items():
                info[key]=value;
        super().__init__(info);
        self.__unique_id = unique_id;
    
    @property
    def unique_id(self):
        return self.__unique_id;

    def increment_reps(self, increment:int):
        self.reps+=increment;

    def set_reps(self, new_value:int):
        self.reps = new_value;
    
    def pack(self)->dict:
        return {
            "unique_id":self.__unique_id,
            "exercise_id":self.exercise_id,
            "info":{
                "reps":self.reps,
            },
        };

    @classmethod
    def from_template(cls, template:ExerciseTemplate, uniqueID:str, custom_info:dict=None)->ExerciseUser:
        return cls(template.get_info_copy(), uniqueID, custom_info);
