from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMainWindow, QTableView
import pandas as pd
import numpy as np

class Habit():
    def __init__(self, name:str, type:str, freq:int = 7):
        self._name = name
        self._type = type
        self._week_frequency = freq

    def __repr__(self):
        return f"Habit Data:\n Name: {self._name}\n Type: {self._type}\n Weekly Frequency: {self._week_frequency}"

    def change_name(self, new_name:str):
        assert new_name is not None and (len(new_name) > 0), "New name must not be empty."
        assert new_name != self._name, "New name must be different from the current name."
        
        self._name = new_name

    def change_type(self, new_type:str):
        assert new_type is not None and (len(new_type) > 0), "New type must not be empty."
        assert new_type != self._type, "New type must be different from the current type."
        
        self._type = new_type
    
    def change_frequency(self, new_freq:int):
        assert isinstance(new_freq, int), "New frequency must be an integer."
        assert new_freq > 0, "New frequency must be greater than zero."
        assert new_freq != self._week_frequency, "New frequency must be different from the current frequency."
        
        self._week_frequency = new_freq
    
    def alter_habit(self, new_name:str = None, new_type:str = None, new_freq:int = None):
        if new_name is not None:
            self.change_name(new_name)
        if new_type is not None:
            self.change_type(new_type)
        if new_freq is not None:
            self.change_frequency(new_freq)
    
    def get_name(self):
        return self._name
    
    def get_type(self):
        return self._type
    
    def get_frequency(self):
        return self._week_frequency

class HabitInstance():
    def __init__(self, habit:Habit, date:str, check:bool = False):
        self._habit = habit
        self._date = pd.to_datetime(date)
        self._check = check

    def get_date_string(self):
        date_string = self._date.strftime("%d/%m/%Y")
        return date_string

    def get_habit(self):
        return self._habit.__repr__()

    def __repr__(self):
        return f"Habit Instance Data:\n Habit: {self.get_habit}\n Date: {self.get_date_string}\n Done?: {'Yes' if self._check else 'No'}"

    def change_check(self, new_check:bool):
        assert isinstance(new_check, bool), "New check must be a boolean."        
        self._check = new_check
        
class HabitTable(QAbstractTableModel):
    def __init__(self, habits:list=[], parent=None):
        super().__init__(parent)
        if not all(isinstance(habit, Habit) for habit in habits):
            raise ValueError("All elements must be instances of the Habit class.")
        self._habits = habits

        self._habit_dataframe = pd.DataFrame({
            'Name': [habit.get_name() for habit in habits],
            'Type': [habit.get_type() for habit in habits],
            'Weekly Frequency': [habit.get_frequency() for habit in habits]
        })

    def get_habits(self):
        for habit in self._habits:
            print(habit.__repr__())

class MainWindow(QMainWindow):
    def __init__(self, habit_list:list=[]):        
        super().__init__()
        self.setWindowTitle("Habit Tracker by Leonardo Scarton")
        self.setGeometry(100, 100, 800, 600)

        self._layout = QVBoxLayout()

        self._habit_table = HabitTable(habit_list)

        container = QWidget()
        container.setLayout(self._layout)
        self.setCentralWidget(container)

        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start_click)
        self._layout.addWidget(start_button)

    def start_click(self):
        print("Start button clicked!")
        habit_window = HabitWindow(parent=self, habit_table=self._habit_table)
        habit_window.show()

class HabitWindow(QWidget):
    def __init__(self, habit_table:HabitTable, parent=None):
        super().__init__(parent)
        #self.setWindowTitle("Habit Tracker by Leonardo Scarton - Habits")
        self.setGeometry(0, 0, 800, 600)

        self._habit_table = habit_table

        layout = QVBoxLayout()

        table_view = QTableView()
        table_view.setModel(self._habit_table)
        layout.addWidget(table_view)

        self.setLayout(layout)

        button_add = QPushButton("Add New Habit")
        button_add.clicked.connect(self.add_click)
        layout.addWidget(button_add)

    def add_click(self):
        print("Button clicked!")