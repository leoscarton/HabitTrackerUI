import pandas as pd
import numpy as np
import sys
from habits_gui import MainWindow, Habit, HabitInstance
from PySide6.QtWidgets import QApplication

'''
def register_habits(habits_file):
    habit_list = []
    with open(habits_file, 'r') as hf:
        lines = hf.readlines()
        for line in lines:
            name, type_, freq = line.strip().split(',')
            habit = Habit(name, type_, int(freq))
            habit_list.append(habit)
    
    return habit_list
'''
    
if __name__ == "__main__":
    # Register habits from a CSV file
#    habits_file = 'habits.csv'
#    habit_list = register_habits(habits_file)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()