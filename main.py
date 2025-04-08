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



def register_habits(habits_file):
    with open(habits_file, 'r') as hf:
        pass