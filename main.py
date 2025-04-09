import pandas as pd
import numpy as np
import sys
from habits_gui import MainWindow
from PySide6.QtWidgets import QApplication
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()