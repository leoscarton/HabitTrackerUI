from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMainWindow, QTableView
import pandas as pd
import numpy as np

class Habit():
    def __init__(self, name:str, type:str, freq:int = 7, check:bool = False):
        self._name = name
        self._type = type
        self._week_frequency = freq
        self._check = check

    def __repr__(self):
        return f"Habit Data: Name = {self._name}, Type = {self._type}, Weekly Frequency = {self._week_frequency}, Done? = {'Yes' if self._check else 'No'}"

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

    def change_check(self, new_check:bool):
        assert isinstance(new_check, bool), "New check must be a boolean."
        assert new_check != self._check, "New check must be different from the current check."
        
        self._check = new_check
    
    def alter_habit(self, new_name:str = None, new_type:str = None, new_freq:int = None, new_check:bool = None):
        if new_name is not None:
            self.change_name(new_name)
        if new_type is not None:
            self.change_type(new_type)
        if new_freq is not None:
            self.change_frequency(new_freq)
        if new_check is not None:
            self.change_check(new_check)
    
    def get_name(self):
        return self._name
    
    def get_type(self):
        return self._type
    
    def get_frequency(self):
        return self._week_frequency
    
    def get_check(self):
        return self._check

'''
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
'''
        
class HabitTable(QAbstractTableModel):
    def __init__(self, df: pd.DataFrame, parent=None):
        super().__init__(parent)
        self._habits = df.copy()

    def rowCount(self):
        return self._habits.shape[0]

    def columnCount(self):
        return self._habits.shape[1]
    
    def getData(self):
        return self._habits.copy()

class MainWindow(QMainWindow):
    def __init__(self, df: pd.DataFrame = pd.DataFrame(columns=["Habit", "Type", "Frequency", "Done"])):        
        super().__init__()
        self.setWindowTitle("Habit Tracker by Leonardo Scarton")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

#        button = QPushButton("Click Me")
#        button.clicked.connect(self.start_click)
#        layout.addWidget(button)

        model = HabitTable(df)
        table_view = QTableView()
        table_view.setModel(model)
        layout.addWidget(table_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


#    def start_click(self):
#        print("Button clicked!")