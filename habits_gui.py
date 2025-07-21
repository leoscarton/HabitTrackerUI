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
        # Storing the filename and DataFrame
        self._filename = filename
        self._columns = columns or ['Name', 'Type', 'Weekly Frequency', 'Instances']
        if df is not None:
            self._dataframe = df
        else:
            self._dataframe = pd.DataFrame(columns=self._columns)

    # Setters and getters
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
    
    # Method for saving the DataFrame to a CSV file
    def save_to_csv(self):
        if not self._filename.endswith('.csv'):
            raise ValueError("Filename must end with .csv")
        if self._dataframe.empty:
            print("DataFrame is empty. Nothing to save.")
            return
        self._dataframe.to_csv(self._filename, index=False, encoding='utf-8')

    # Method for loading the DataFrame from a CSV file
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
        # Initializing the variables
        self._name = name
        self._type = type
        self._week_frequency = freq
        self._instances = instances

    # String representation of the Habit class
    def __repr__(self):
        return f"Habit Data:\n Name: {self._name}\n Type: {self._type}\n Weekly Frequency: {self._week_frequency}\n Instances: {self._instances}"

    #Name Setter and Getter
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name:str):
        assert new_name is not None and (len(new_name) > 0), "New name must not be empty."
        assert new_name != self._name, "New name must be different from the current name."
        
        self._name = new_name

    #Type Setter and Getter
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, new_type:str):
        assert new_type is not None and (len(new_type) > 0), "New type must not be empty."
        assert new_type != self._type, "New type must be different from the current type."
        
        self._type = new_type

    #Frequency Setter and Getter 
    @property
    def week_frequency(self):
        return self._week_frequency
    
    @week_frequency.setter
    def change_frequency(self, new_freq:int):
        assert isinstance(new_freq, int), "New frequency must be an integer."
        assert new_freq > 0, "New frequency must be greater than zero."
        assert new_freq != self._week_frequency, "New frequency must be different from the current frequency."
        
        self._week_frequency = new_freq

    #Instances Setter and Getter
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

    # Method to alter the habit's properties
    # Allows changing name, type, frequency, and instances
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
    def __init__(self, habit:Habit, date:str, check:bool = False, out_of_control:bool = False):
        # Initializing the variables
        self._habit = habit
        self._date = pd.to_datetime(date)
        self._check = check
        self._out_of_control = out_of_control

    # Setters and getters
    @property
    def date(self):
        date_string = self._date.strftime("%d/%m/%Y")
        return date_string

    @property
    def habit(self):
        return self._habit.__repr__()

    @property
    def check(self):
        return self._check
    
    @check.setter
    def change_check(self, new_check:bool):
        assert isinstance(new_check, bool), "New check must be a boolean."        
        self._check = new_check

    @property
    def out_of_control(self):
        return self._out_of_control
    
    @out_of_control.setter
    def out_of_control(self, new_out_of_control:bool):
        assert isinstance(new_out_of_control, bool), "New out_of_control must be a boolean."
        self._out_of_control = new_out_of_control

    # String representation of the HabitInstance class
    def __repr__(self):
        return f"Habit Instance Data:\n Habit: {self.habit}\n Date: {self.date_string}\n Done?: {'Yes' if self._check else 'No'}"
          
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

    # Setters and getters
    @property
    def habits(self):
        for habit in self._habits:
            print(habit.__repr__())
    
    @property
    def habit_dataframe(self):
        return self._habit_dataframe
    
    # Method to update the DataFrame based on the habits list
    # This method is called whenever a habit is added, removed, or modified
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

    # Row and Column Count methods
    # These methods are required by the QAbstractTableModel interface
    def rowCount(self, parent=None):
        return self._habit_dataframe.shape[0]

    def columnCount(self, parent=None):
        return self._habit_dataframe.shape[1]

    # Data method to retrieve data for the table view
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            value = self._habit_dataframe.iloc[index.row(), index.column()]
            return str(value)
        return None

    # Header data method to provide headers for the table view
    # This method is called to set the headers for the table view
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._habit_dataframe.columns[section]
            else:
                return str(section+1)
        return None
    
    # Method to save the DataFrame to a CSV file
    # This method uses the CSVHandler class to save the DataFrame
    def save_df_to_csv(self, filename:str):
        if self._csv_handler:
            self._csv_handler.filename = filename
            self._csv_handler.dataframe = self._habit_dataframe
            self._csv_handler.save_to_csv()
        else:
            raise ValueError("CSVHandler is not initialized.")

    # Method to load the DataFrame from a CSV file
    # This method uses the CSVHandler class to load the DataFrame
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
    def __init__(self, habit_list:list=[], habit_instance_list:list=[]): #, parent=None):
        super().__init__()
        
        # Setting up the main window name and dimensions
        self.setWindowTitle("Habit Tracker by Leonardo Scarton")
        self.setGeometry(100, 100, 800, 600)

        # Initializing the vertical layout for the main window
        self._layout = QVBoxLayout()

        # Initializing the HabitTable and HabitInstanceTable with provided lists
        self._habit_table = HabitTable(habit_list)
        self._habit_window = HabitWindow(parent=self, habit_table=self._habit_table)
        self._habit_instance_table = HabitInstanceTable(habit_instance_list)
        self._habit_instance_window = HabitInstanceWindow(parent=self, habit_instance_table=self._habit_instance_table)
        self._data_window = DataWindow(habit_table=self._habit_table, parent=self)

        # Setting up the main layout
        self.container_start = QWidget()
        self.container_start.setLayout(self._layout)
        self.setCentralWidget(self.container_start)

        # Habit Table/Window Container
        self.container_habit_table = QWidget()
        self.container_habit_table.setLayout(self._habit_window.layout())
        self._layout.addWidget(self.container_habit_table)
        self.container_habit_table.hide()

        # Habit Instance Table/Window Container
        self.container_habit_instance_table = QWidget()
        self.container_habit_instance_table.setLayout(self._habit_instance_window.layout())
        self._layout.addWidget(self.container_habit_instance_table)
        self.container_habit_instance_table.hide()

        # Data Window Container
        self.container_data_window = QWidget()
        self.container_data_window.setLayout(self._data_window.layout())
        self._layout.addWidget(self.container_data_window)
        self.container_data_window.hide()

        # Start Button
        self._start_button = QPushButton("Start")
        self._start_button.clicked.connect(self.start_click)
        self._layout.addWidget(self._start_button)

    # Start Button Click Handler
    def start_click(self):
        self._start_button.hide()
        self.container_habit_table.show()


##########################################################################
            # HabitWindow and AddHabitWindow Classes
##########################################################################

class HabitWindow(QWidget):
    def __init__(self, habit_table:HabitTable, parent=None):
        super().__init__(parent)
        # Setting up the HabitWindow dimensions
        self.setGeometry(0, 0, 800, 600)

        # Storing the variables
        self.parent = parent
        self._habit_table = habit_table

        # Initializing the layout for the HabitWindow
        layout = QVBoxLayout()

        table_view = QTableView()
        table_view.setModel(self._habit_table)
        header = table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(table_view)

        self.setLayout(layout)

        button_layout = QHBoxLayout()

        button_add = QPushButton("Add New Habit")
        button_add.clicked.connect(self.add_click)

        button_change_habit_instance_window = QPushButton("Habit Instances")
        button_change_habit_instance_window.clicked.connect(self.change_window_to_habit_instace_window)

        button_change_data_window = QPushButton("Habit Data")
        button_change_data_window.clicked.connect(self.change_window_to_data_window)

        button_layout.addWidget(button_add)
        button_layout.addWidget(button_change_habit_instance_window)
        button_layout.addWidget(button_change_data_window)
        layout.addLayout(button_layout)

    # Add New Habit Button Click Handler
    def add_click(self):
        add_habit_window = AddHabitWindow(parent=self)
        add_habit_window.show()

    # Change Window to Habit Instance Window Handler
    def change_window_to_habit_instace_window(self):
        self.parent.container_habit_table.hide()
        self.parent.container_habit_instance_table.show()

    # Change Window to Data Window Handler
    def change_window_to_data_window(self):
        self.parent.container_habit_table.hide()
        self.parent.container_data_window.show()

class AddHabitWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Setting up the AddHabitWindow dimensions and title
        self.setGeometry(0, 0, 400, 200)
        self.setWindowTitle("Add New Habit")

        # Initializing the layout for the AddHabitWindow
        layout = QFormLayout()

        # Creating input fields for habit name, type, and weekly frequency
        self._habit_name_line = QLineEdit()
        self._habit_type_line = QLineEdit()
        self._weekly_freq_line = QSpinBox()

        # Adding input fields to the layout
        layout.addRow(QLabel("Habit Name:"), self._habit_name_line)
        layout.addRow(QLabel("Habit Type:"), self._habit_type_line)
        layout.addRow(QLabel("Weekly Frequency:"), self._weekly_freq_line)

        # Creating buttons for entering the habit and canceling
        # Enter button will call the enter_habit method 
        enter_button = QPushButton("Enter")
        enter_button.clicked.connect(self.enter_habit)
        layout.addRow(enter_button)

        # Cancel button will close the AddHabitWindow
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        layout.addRow(cancel_button)

        # Setting the layout to a central widget
        container_start = QWidget()
        container_start.setLayout(layout)
        self.setCentralWidget(container_start)

    # Close AddHabitWindow Handler
    def close(self):
        super().close()

    # Enter Habit Button Click Handler
    def enter_habit(self):
        name = self._habit_name_line.text()
        type_ = self._habit_type_line.text()
        freq = self._weekly_freq_line.value()

        if not name or not type_:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        new_habit = Habit(name, type_, freq)
        self.parent._habit_table._habits.append(new_habit)
        self.parent._habit_table.update_dataframe()

        self.close()

class HabitInstanceTable(QAbstractTableModel):
    def __init__(self, habit_instances:list=[], parent=None, csv_handler:CSVHandler = None):
        super().__init__(parent)

        # Initializing the variables
        if not all(isinstance(instance, HabitInstance) for instance in habit_instances):
            raise ValueError("All elements must be instances of the HabitInstance class.")
        self._habit_instances = habit_instances

        self._csv_handler = csv_handler if csv_handler else CSVHandler()

        # Creating a DataFrame to hold the habit instances
        # The DataFrame will have columns for Habit, Date, Done and Conditions Out of Control
        self._habit_instance_dataframe = pd.DataFrame({
            'Habit': [instance.habit for instance in habit_instances],
            'Date': [instance.date_string for instance in habit_instances],
            'Done?': [instance._check for instance in habit_instances],
            'Conditions Out of Control?': [instance._out_of_control for instance in habit_instances]
        })

    # Row and Column Count methods
    # These methods are required by the QAbstractTableModel interface
    def rowCount(self, parent=None):
        return self._habit_instance_dataframe.shape[0]

    def columnCount(self, parent=None):
        return self._habit_instance_dataframe.shape[1]

    # Getter for the habit instances
    @property
    def dataframe(self):
        return self._habit_instance_dataframe

    # Method to update the DataFrame based on the habit instances list
    # This method is called whenever a habit instance is added, removed, or modified
    def update_dataframe(self):
        self._habit_instance_dataframe = pd.DataFrame({
            'Habit': [instance.habit for instance in self._habit_instances],
            'Date': [instance.date for instance in self._habit_instances],
            'Done?': [instance.check for instance in self._habit_instances],
            'Conditions Out of Control?': [instance.out_of_control for instance in self._habit_instances]
        })
        self.layoutChanged.emit()

    # Data method to retrieve data for the table view
    # This method is called to get the data for each cell in the table view
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            value = self._habit_instance_dataframe.iloc[index.row(), index.column()]
            return str(value)
        return None

    # Header data method to provide headers for the table view
    # This method is called to set the headers for the table view
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._habit_instance_dataframe.columns[section]
            else:
                return str(section+1)
        return None

    # Method to save the DataFrame to a CSV file
    # This method uses the CSVHandler class to save the DataFrame
    def save_df_to_csv(self, filename:str):
        if self._csv_handler:
            self._csv_handler.filename = filename
            self._csv_handler.dataframe = self._habit_instance_dataframe
            self._csv_handler.save_to_csv()
        else:
            raise ValueError("CSVHandler is not initialized.")
        
    # Method to load the DataFrame from a CSV file
    # This method uses the CSVHandler class to load the DataFrame
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

        # Setting up the HabitInstanceWindow dimensions
        self.setGeometry(0, 0, 800, 600)

        # Storing the variables
        self.parent = parent
        self._habit_instance_table = habit_instance_table

        # Initializing the layout for the HabitInstanceWindow
        layout = QVBoxLayout()

        # Creating a table view to display the habit instances
        # The table view will use the HabitInstanceTable model
        table_view = QTableView()
        table_view.setModel(self._habit_instance_table)
        header = table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        #self._habit_instance_table.dataframe()

        layout.addWidget(table_view)

        self.setLayout(layout)

        # Adding button layout
        button_layout = QHBoxLayout()

        # Add New Habit Instance Button
        # This button will open the AddHabitInstanceWindow when clicked
        button_add = QPushButton("Add New Habit Instance")
        button_add.clicked.connect(self.add_click)

        # Change Window to Habit Window Button
        button_change_habit_window = QPushButton("Habit List")
        button_change_habit_window.clicked.connect(self.change_window_to_habit_window)

        # Change Window to Data Window Button
        button_change_data_window = QPushButton("Habit Data")
        button_change_data_window.clicked.connect(self.change_window_to_data_window)

        # Adding buttons to the button layout
        button_layout.addWidget(button_add)
        button_layout.addWidget(button_change_habit_window)
        button_layout.addWidget(button_change_data_window)
        layout.addLayout(button_layout)

    # Add New Habit Instance Button Click Handler
    # This method will open the AddHabitInstanceWindow when the button is clicked
    def add_click(self):
        add_habit_instance_window = AddHabitInstanceWindow(parent=self)
        add_habit_instance_window.show()

    # Change Window to Habit Window Handler
    def change_window_to_habit_window(self):
        self.parent.container_habit_instance_table.hide()
        #self.parent().setCentralWidget(self.parent()._habit_window)
        self.parent.container_habit_table.show()
    
    # Change Window to Data Window Handler
    def change_window_to_data_window(self):
        self.parent.container_habit_instance_table.hide()
        self.parent.container_data_window.show()

class AddHabitInstanceWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Setting up the AddHabitInstanceWindow dimensions and title
        self.setGeometry(0, 0, 400, 200)
        self.setWindowTitle("Habit Instances")

        # Initializing the layout for the AddHabitInstanceWindow
        layout = QFormLayout(self)

        # Creating input fields for habit instance name, date, and done status
        # The done status will be a combo box with options "Yes" and "No"
        self._habit_instance_line = QLineEdit()
        self._date_line = QLineEdit()
        self._check_box = QComboBox()
        self._check_box.addItems(["Yes", "No"])
        self._out_of_control_box = QComboBox()
        self._out_of_control_box.addItems(["No", "Yes"])


        # Adding input fields to the layout
        layout.addRow(QLabel("Habit Instance:"), self._habit_instance_line)
        layout.addRow(QLabel("Date:"), self._date_line)
        layout.addRow(QLabel("Done?"), self._check_box)
        layout.addRow(QLabel("Conditions Out of Control?"), self._out_of_control_box)

        # Creating buttons for entering the habit instance and canceling
        # Enter button will call the enter_habit_instance method
        enter_button = QPushButton("Enter")
        enter_button.clicked.connect(self.enter_habit_instance)
        layout.addRow(enter_button)

        # Cancel button will close the AddHabitInstanceWindow
        # This button will not save any changes and will simply close the window
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        layout.addRow(cancel_button)

        # Setting the layout to a central widget
        container_start = QWidget()
        container_start.setLayout(layout)
        self.setCentralWidget(container_start)
    
    # Function to handle the Enter button click and enter a new habit instance
    # This method will create a new HabitInstance object and add it to the habit instance table
    def enter_habit_instance(self):
        habit_name = self._habit_instance_line.text()
        date = self._date_line.text()
        check = self._check_box.currentText() == "Yes"
        out_of_control = self._out_of_control_box.currentText() == "Yes"

        if not habit_name or not date:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        new_habit_instance = HabitInstance(habit_name, date, check, out_of_control)
        self.parent._habit_instance_table._habit_instances.append(new_habit_instance)
        self.parent._habit_instance_table.update_dataframe()

        self.close()

    def close(self):
        super().close()

##########################################################################
                        # DataWindow Classes
##########################################################################

class DataWindow(QMainWindow):
    def __init__(self, habit_table:HabitTable, parent=None):
        super().__init__(parent)

        # Setting up the DataWindow dimensions and title
        self.parent = parent
        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle("Habit Data")

        # Storing the habit table
        self._habit_table = habit_table

        # Initializing the layout for the DataWindow
        layout = QVBoxLayout()

        # Creating a table view to display the habit data
        # The table view will use the HabitTable model
        table_view = QTableView()
        table_view.setModel(self._habit_table)
        header = table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Adding the table view to the layout
        layout.addWidget(table_view)

        # Setting the layout to a central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Adding button layout for changing windows  
        button_layout = QHBoxLayout()

        # Creating buttons for changing to Habit Window
        button_change_habit_window = QPushButton("Habit List")
        button_change_habit_window.clicked.connect(self.change_window_to_habit_window)

        # Creating buttons for changing to Habit Instance Window
        button_change_habit_instance_window = QPushButton("Habit Instances")
        button_change_habit_instance_window.clicked.connect(self.change_window_to_habit_instance_window)

        # Adding buttons to the button layout
        button_layout.addWidget(button_change_habit_window)
        button_layout.addWidget(button_change_habit_instance_window)
        layout.addLayout(button_layout)

    # Change Window to Habit Window Handler
    # This method will hide the DataWindow and show the HabitWindow
    def change_window_to_habit_window(self):
        self.parent.container_data_window.hide()
        self.parent.container_habit_table.show()
    
    # Change Window to Habit Instance Window Handler
    # This method will hide the DataWindow and show the HabitInstanceWindow
    def change_window_to_habit_instance_window(self):
        self.parent.container_data_window.hide()
        self.parent.container_habit_instance_table.show()