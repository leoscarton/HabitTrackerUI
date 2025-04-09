import pandas as pd
import numpy as np
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
import sys

class Habit:
    def __init__(self, name:str, type:str, freq:int = 7, check:bool = False):
        self.name = name
        self.type = type
        self.week_frequency = freq
        self.check = check

    def __repr__(self):
        return f"Habit Data: Name = {self.name}, Type = {self.type}, Weekly Frequency = {self.week_frequency}, Done? = {'Yes' if self.check else 'No'}"

    def change_name(self, new_name:str):
        assert new_name is not None and (len(new_name) > 0), "New name must not be empty."
        assert new_name != self.name, "New name must be different from the current name."
        
        self.name = new_name

class HabitGroup():
    def __init__(self, name:str, habits:list[Habit] = []):
        self.name = name
        self.habits = habits

    def __repr__(self):
        return f"Habit Group: Name = {self.name}, Habits = {self.habits}"
    
    def change_group_name(self, new_name:str):
        assert isinstance(new_name, str), "New name must be a string."
        assert new_name is not None and (len(new_name) > 0), "New name must not be empty."
        assert new_name != self.name, "New name must be different from the current name."
        
        self.name = new_name

    def add_habit(self, habit:Habit):
        assert habit.name not in [h.name for h in self.habits], "Habit name already exists in the group."
        assert habit is not None, "Added object must not be empty."
        assert len(habit.name) > 0, "Added object must have a valid name."
        assert habit.type == self.name, "Habit type must match the group name."

        self.habits.append(habit)

    def remove_habit(self, habit:Habit):
        self.habits.remove(habit)

def register_habits(habits_file):
    with open(habits_file, 'r') as hf:
        pass

print("It is working.")