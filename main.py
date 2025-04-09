import pandas as pd
import numpy as np
import sys
import habits_gui
from PySide6.QtWidgets import QApplication


def register_habits(habits_file):
    with open(habits_file, 'r') as hf:
        df = pd.read_csv(hf, sep=';')
        df['Done'] = df['Done'].astype(bool)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = habits_gui.MainWindow()
    window.show()

    app.exec()