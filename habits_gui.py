from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMainWindow, QTableView, QHeaderView, QLineEdit
from PySide6.QtWidgets import QFormLayout, QLabel, QComboBox, QSpinBox, QMessageBox
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

##########################################################################
                        # CSVHandler Class
        # Separate class for handling CSV operations
##########################################################################
class CSVHandler:
    def __init__(self, filename:str = "habits.csv", df:pd.DataFrame = None, columns:list = None):
        self._filename = filename
        self._columns = columns or ['Name', 'Type', 'Weekly Frequency', 'Instances']
        if df is not None:
            self._dataframe = df
        else:
            self._dataframe = pd.DataFrame(columns=self._columns)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename:str):
        assert filename.endswith('.csv'), "Filename must end with .csv"   
        self._filename = filename
    
    @property
    def dataframe(self):
        return self._dataframe
    
    @dataframe.setter
    def dataframe(self, df:pd.DataFrame):
        assert isinstance(df, pd.DataFrame), "Data must be a pandas DataFrame."
        self._dataframe = df
    
    def save_to_csv(self):
        if not self._filename.endswith('.csv'):
            raise ValueError("Filename must end with .csv")
        if self._dataframe.empty:
            print("DataFrame is empty. Nothing to save.")
            return
        self._dataframe.to_csv(self._filename, index=False, encoding='utf-8')

    def load_from_csv(self):
        try:
            self._dataframe = pd.read_csv(self._filename, encoding='utf-8')
        except FileNotFoundError:
            print(f"File {self._filename} not found. Creating a new one.")
            self._dataframe = pd.DataFrame(columns=['Name', 'Type', 'Weekly Frequency', 'Instances'])
        except Exception as e:
            logging.error(f"An error occurred while loading the file '{self._filename}': {e}")
        

##########################################################################
            # Habit, HabitInstance, and HabitTable Classes
##########################################################################

class Habit():
    def __init__(self, name:str, type:str, freq:int = 7, instances:int = 0):
        self._name = name
        self._type = type
        self._week_frequency = freq
        self._instances = instances

    def __repr__(self):
        return f"Habit Data:\n Name: {self._name}\n Type: {self._type}\n Weekly Frequency: {self._week_frequency}\n Instances: {self._instances}"

    #Name
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name:str):
        assert new_name is not None and (len(new_name) > 0), "New name must not be empty."
        assert new_name != self._name, "New name must be different from the current name."
        
        self._name = new_name

    #Type
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, new_type:str):
        assert new_type is not None and (len(new_type) > 0), "New type must not be empty."
        assert new_type != self._type, "New type must be different from the current type."
        
        self._type = new_type

    #Frequency   
    @property
    def week_frequency(self):
        return self._week_frequency
    
    @week_frequency.setter
    def change_frequency(self, new_freq:int):
        assert isinstance(new_freq, int), "New frequency must be an integer."
        assert new_freq > 0, "New frequency must be greater than zero."
        assert new_freq != self._week_frequency, "New frequency must be different from the current frequency."
        
        self._week_frequency = new_freq

    #Instances
    @property
    def instances(self):
        return self._instances
    
    @instances.setter
    def change_instances(self, new_instances:int):
        assert isinstance(new_instances, int), "New instances must be an integer."
        assert new_instances >= 0, "New instances must be greater than or equal to zero."
        
        self._instances = new_instances

  #  def increment_instances(self):
  #      self._instances += 1

    def alter_habit(self, new_name:str = None, new_type:str = None, new_freq:int = None, new_instances:int = None):
        if new_name is not None:
            self.name(new_name)
        if new_type is not None:
            self.type(new_type)
        if new_freq is not None:
            self.week_frequency(new_freq)
        if new_instances is not None:
            self.instances(new_instances)


class HabitInstance():
    def __init__(self, habit:Habit, date:str, check:bool = False):
        self._habit = habit
        self._date = pd.to_datetime(date)
        self._check = check

    @property
    def date(self):
        date_string = self._date.strftime("%d/%m/%Y")
        return date_string

    @property
    def habit(self):
        return self._habit.__repr__()

    def __repr__(self):
        return f"Habit Instance Data:\n Habit: {self.habit}\n Date: {self.date_string}\n Done?: {'Yes' if self._check else 'No'}"

    @property
    def check(self):
        return self._check
    
    @check.setter
    def change_check(self, new_check:bool):
        assert isinstance(new_check, bool), "New check must be a boolean."        
        self._check = new_check
        
class HabitTable(QAbstractTableModel):
    def __init__(self, habits:list=[], parent=None, csv_handler:CSVHandler = None):
        super().__init__(parent)
        if not all(isinstance(habit, Habit) for habit in habits):
            raise ValueError("All elements must be instances of the Habit class.")
        self._habits = habits
        self._csv_handler = csv_handler if csv_handler else CSVHandler()

        self._habit_dataframe = pd.DataFrame({
            'Name': [habit.name for habit in habits],
            'Type': [habit.type for habit in habits],
            'Weekly Frequency': [habit.week_frequency for habit in habits],
            'Instances': [habit.instances for habit in habits]
        })

    @property
    def habits(self):
        for habit in self._habits:
            print(habit.__repr__())
    
    @property
    def habit_dataframe(self):
        return self._habit_dataframe
    
    def update_dataframe(self):
        self._habit_dataframe = pd.DataFrame({
            'Name': [habit.name for habit in self._habits],
            'Type': [habit.type for habit in self._habits],
            'Weekly Frequency': [habit.week_frequency for habit in self._habits],
            'Instances': [habit.instances for habit in self._habits]
        })
        self.save_df_to_csv(self._csv_handler.filename)
        #logging.info("Habit DataFrame updated and saved to CSV.")
        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return self._habit_dataframe.shape[0]

    def columnCount(self, parent=None):
        return self._habit_dataframe.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            value = self._habit_dataframe.iloc[index.row(), index.column()]
            return str(value)
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._habit_dataframe.columns[section]
            else:
                return str(section+1)
        return None
    
    def save_df_to_csv(self, filename:str):
        if self._csv_handler:
            self._csv_handler.filename = filename
            self._csv_handler.dataframe = self._habit_dataframe
            self._csv_handler.save_to_csv()
        else:
            raise ValueError("CSVHandler is not initialized.")

    def load_df_from_csv(self, filename:str):
        if self._csv_handler:
            self._csv_handler.filename = filename
            self._csv_handler.load_from_csv()
            self._habit_dataframe = self._csv_handler.dataframe
            self.update_dataframe()
        else:
            raise ValueError("CSVHandler is not initialized.")

##########################################################################
                        # MainWindow Class
##########################################################################

class MainWindow(QMainWindow):
    def __init__(self, habit_list:list=[], habit_instance_list:list=[], parent=None):        
        super().__init__()
        self.setWindowTitle("Habit Tracker by Leonardo Scarton")
        self.setGeometry(100, 100, 800, 600)

        self._layout = QVBoxLayout()

        self._habit_table = HabitTable(habit_list)
        self._habit_window = HabitWindow(parent=self, habit_table=self._habit_table)
        self._habit_instance_table = HabitInstanceTable(habit_instance_list)
        self._habit_instance_window = HabitInstanceWindow(parent=self, habit_instance_table=self._habit_instance_table)

        self._habit_window.hide()
        self._habit_instance_window.hide()

        self.container_start = QWidget()
        self.container_start.setLayout(self._layout)
        self.setCentralWidget(self.container_start)

        self.container_habit_table = QWidget()
        self.container_habit_table.setLayout(self._habit_window.layout())
        self._layout.addWidget(self.container_habit_table)
        self.container_habit_table.hide()

        self.container_habit_instance_table = QWidget()
        self.container_habit_instance_table.setLayout(self._habit_instance_window.layout())
        self._layout.addWidget(self.container_habit_instance_table)
        self.container_habit_instance_table.hide()

        self._start_button = QPushButton("Start")
        self._start_button.clicked.connect(self.start_click)
        self._layout.addWidget(self._start_button)

    def start_click(self):
        self._start_button.hide()
        #self.setCentralWidget(self._habit_window)
        self.container_habit_table.show()


##########################################################################
            # HabitWindow and AddHabitWindow Classes
##########################################################################

class HabitWindow(QWidget):
    def __init__(self, habit_table:HabitTable, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 800, 600)

        self._habit_table = habit_table

        layout = QVBoxLayout()

        table_view = QTableView()
        table_view.setModel(self._habit_table)
        header = table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        #self._habit_table.habit_dataframe()

        layout.addWidget(table_view)

        self.setLayout(layout)

        button_layout = QHBoxLayout()

        button_add = QPushButton("Add New Habit")
        button_add.clicked.connect(self.add_click)

        button_change_window = QPushButton("Habit Instances")
        button_change_window.clicked.connect(self.change_window_click)

        button_layout.addWidget(button_add)
        button_layout.addWidget(button_change_window)
        layout.addLayout(button_layout)

    def add_click(self):
        print("Button clicked!")
        add_habit_window = AddHabitWindow(parent=self)
        add_habit_window.show()
    
    def change_window_click(self):
        print("Change window button clicked!")
        self.parent().container_habit_table.hide()
        #self.parent().setCentralWidget(self.parent()._habit_instance_window)
        self.parent().container_habit_instance_table.show()

class AddHabitWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 400, 200)
        self.setWindowTitle("Add New Habit")

        layout = QFormLayout()

        self._habit_name_line = QLineEdit()
        self._habit_type_line = QLineEdit()
        self._weekly_freq_line = QSpinBox()

        layout.addRow(QLabel("Habit Name:"), self._habit_name_line)
        layout.addRow(QLabel("Habit Type:"), self._habit_type_line)
        layout.addRow(QLabel("Weekly Frequency:"), self._weekly_freq_line)

        enter_button = QPushButton("Enter")
        enter_button.clicked.connect(self.enter_habit)
        layout.addRow(enter_button)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        layout.addRow(cancel_button)

        container_start = QWidget()
        container_start.setLayout(layout)
        self.setCentralWidget(container_start)

    def close(self):
        super().close()

    def enter_habit(self):
        name = self._habit_name_line.text()
        type_ = self._habit_type_line.text()
        freq = self._weekly_freq_line.value()

        if not name or not type_:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        new_habit = Habit(name, type_, freq)
        self.parent()._habit_table._habits.append(new_habit)
        self.parent()._habit_table.update_dataframe()

        self.close()

class HabitInstanceTable(QAbstractTableModel):
    def __init__(self, habit_instances:list=[], parent=None, csv_handler:CSVHandler = None):
        super().__init__(parent)
        if not all(isinstance(instance, HabitInstance) for instance in habit_instances):
            raise ValueError("All elements must be instances of the HabitInstance class.")
        self._habit_instances = habit_instances
        self._csv_handler = csv_handler if csv_handler else CSVHandler()

        self._habit_instance_dataframe = pd.DataFrame({
            'Habit': [instance.habit() for instance in habit_instances],
            'Date': [instance.date_string() for instance in habit_instances],
            'Done?': [instance._check for instance in habit_instances]
        })

    def rowCount(self, parent=None):
        return self._habit_instance_dataframe.shape[0]

    def columnCount(self, parent=None):
        return self._habit_instance_dataframe.shape[1]

    def dataframe(self):
        return self._habit_instance_dataframe

    def update_dataframe(self):
        self._habit_instance_dataframe = pd.DataFrame({
            'Habit': [instance.habit for instance in self._habit_instances],
            'Date': [instance.date for instance in self._habit_instances],
            'Done?': [instance.check for instance in self._habit_instances]
        })
        self.layoutChanged.emit()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            value = self._habit_instance_dataframe.iloc[index.row(), index.column()]
            return str(value)
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._habit_instance_dataframe.columns[section]
            else:
                return str(section+1)
        return None

    def save_df_to_csv(self, filename:str):
        if self._csv_handler:
            self._csv_handler.filename = filename
            self._csv_handler.dataframe = self._habit_instance_dataframe
            self._csv_handler.save_to_csv()
        else:
            raise ValueError("CSVHandler is not initialized.")
        
    def load_df_from_csv(self, filename:str):
        if self._csv_handler:
            self._csv_handler.filename = filename
            self._csv_handler.load_from_csv()
            self._habit_instance_dataframe = self._csv_handler.dataframe
            self.update_dataframe()
        else:
            raise ValueError("CSVHandler is not initialized.")

##########################################################################
        # HabitInstanceWindow and AddHabitInstanceWindow Classes
##########################################################################

class HabitInstanceWindow(QWidget):
    def __init__(self, habit_instance_table:HabitInstanceTable, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 800, 600)

        self._habit_instance_table = habit_instance_table

        layout = QVBoxLayout()

        table_view = QTableView()
        table_view.setModel(self._habit_instance_table)
        header = table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self._habit_instance_table.dataframe()

        layout.addWidget(table_view)

        self.setLayout(layout)

        button_layout = QHBoxLayout()

        button_add = QPushButton("Add New Habit Instance")
        button_add.clicked.connect(self.add_click)

        button_change_window = QPushButton("Habit List")
        button_change_window.clicked.connect(self.change_window_click)

        button_layout.addWidget(button_add)
        button_layout.addWidget(button_change_window)
        layout.addLayout(button_layout)

    def add_click(self):
        add_habit_instance_window = AddHabitInstanceWindow(parent=self)
        add_habit_instance_window.show()
    
    def change_window_click(self):
        self.parent().container_habit_instance_table.hide()
        #self.parent().setCentralWidget(self.parent()._habit_window)
        self.parent().container_habit_table.show()

class AddHabitInstanceWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 400, 200)
        self.setWindowTitle("Habit Instances")

        layout = QFormLayout(self)

        self._habit_instance_line = QLineEdit()
        self._date_line = QLineEdit()
        self._check_box = QComboBox()
        self._check_box.addItems(["Yes", "No"])

        layout.addRow(QLabel("Habit Instance:"), self._habit_instance_line)
        layout.addRow(QLabel("Date:"), self._date_line)
        layout.addRow(QLabel("Done?"), self._check_box)

        enter_button = QPushButton("Enter")
        enter_button.clicked.connect(self.enter_habit_instance)
        layout.addRow(enter_button)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        layout.addRow(cancel_button)

        container_start = QWidget()
        container_start.setLayout(layout)
        self.setCentralWidget(container_start)
    
    def enter_habit_instance(self):
        habit_name = self._habit_instance_line.text()
        date = self._date_line.text()
        check = self._check_box.currentText() == "Yes"

        if not habit_name or not date:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        new_habit_instance = HabitInstance(habit_name, date, check)
        self.parent()._habit_instance_table._habit_instances.append(new_habit_instance)
        self.parent()._habit_instance_table.update_dataframe()

        self.close()

##########################################################################
                        # DataWindow Classes
##########################################################################

class DataWindow(QMainWindow):
    # Preencher posteriormente, ainda não coloquei nada aqui
    def __init__(self, habit_table:HabitTable, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle("Habit Data")

        layout = QVBoxLayout()

        table_view = QTableView()
        table_view.setModel(habit_table)
        header = table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(table_view)

        container_start = QWidget()
        container_start.setLayout(layout)
        self.setCentralWidget(container_start)