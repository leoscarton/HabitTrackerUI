import pandas as pd
import numpy as np
from habits_gui import HabitTable, HabitInstanceTable

#Preencher, arquivo para análise de dados

def table_to_df(table):
    assert isinstance(table, (HabitTable, HabitInstanceTable)), "Invalid table type"
    df = table.get_dataframe()
    return df

def plot_habit(df:pd.DataFrame):
    pass

def calculate_habit_stats(df:pd.DataFrame, habit_name:str):
    """
    Calculate statistics for a habit DataFrame.
    """
    if habit_name not in df['habit_name'].values:
        raise ValueError(f"Habit '{habit_name}' not found in DataFrame.")
    habit_df = df[df['Habit'] == habit_name]
    stats = {
        'habit': habit_name,
        'instances': len(habit_df),
        'completed_instances': habit_df['Done?'].sum(),
        'completion_rate': habit_df['Done?'].mean() * 100,
        #'average_duration': habit_df['duration'].mean() if 'duration' in habit_df.columns else None,
        #'average_streak': habit_df['streak'].mean() if 'streak' in habit_df.columns else None
    }
    return stats

def show_habit_stats(df:pd.DataFrame, habit_name:str):
    """
    Display statistics for a specific habit.
    """
    stats = calculate_habit_stats(df, habit_name)
    print(f"Statistics for habit '{stats['habit']}':")
    print(f"  Instances: {stats['instances']}")
    print(f"  Completed Instances: {stats['completed_instances']}")
    print(f"  Completion Rate: {stats['completion_rate']:.2f}%")
    #print(f"  Average Duration: {stats['average_duration']:.2f} minutes" if stats['average_duration'] is not None else "  Average Duration: N/A")
    #print(f"  Average Streak: {stats['average_streak']:.2f} days" if stats['average_streak'] is not None else "  Average Streak: N/A")