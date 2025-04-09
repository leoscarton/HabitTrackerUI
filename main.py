import pandas as pd
import numpy as np
import sys
import habits_gui
from PySide6.QtWidgets import QApplication


def register_habits(habits_file):
    with open(habits_file, 'r') as hf:
        df = pd.read_csv(hf, sep=';')
        df.dropna(inplace=True, axis=0)

        return df

if __name__ == "__main__":
    # Register habits from a CSV file
    habits_file = 'habit_df_file.csv'
    df = register_habits(habits_file)

    app = QApplication(sys.argv)
    window = habits_gui.MainWindow()
    window.show()

    app.exec()