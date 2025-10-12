# Модуль для визуализации данных, с возможностью добавления и удаления различных графиков
import matplotlib.pyplot as plt
import pandas as pd


class DataVisualizer:
    # Класс для визуализации данных

    def __init__(self):
        self.visualizations = {}

    def add_histogram(self, name: str, df: pd.DataFrame, column: str):
        # Добавляет гистограмму для указанного столбца
        if column not in df.columns:
            raise ValueError(f"Столбец '{column}' отсутствует в DataFrame.")

        fig, ax = plt.subplots()
        df[column].hist(ax=ax)
        ax.set_title(f"Histogram of {column}")
        self.visualizations[name] = fig

    def add_line_plot(self, name: str, df: pd.DataFrame, x_column: str, y_column: str):
        # Добавляет линейный график
        if x_column not in df.columns or y_column not in df.columns:
            raise ValueError("Указанные столбцы отсутствуют в DataFrame.")

        fig, ax = plt.subplots()
        ax.plot(df[x_column], df[y_column])
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title(f"Line Plot: {y_column} vs {x_column}")
        self.visualizations[name] = fig

    def add_scatter_plot(self, name: str, df: pd.DataFrame, x_column: str, y_column: str):
        #Добавляет диаграмму рассеяния
        if x_column not in df.columns or y_column not in df.columns:
            raise ValueError("Указанные столбцы отсутствуют в DataFrame.")

        fig, ax = plt.subplots()
        ax.scatter(df[x_column], df[y_column])
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title(f"Scatter Plot: {y_column} vs {x_column}")
        self.visualizations[name] = fig

    def remove_visualization(self, name: str):
        #Удаляет визуализацию по имени
        if name in self.visualizations:
            del self.visualizations[name]
        else:
            raise KeyError(f"Визуализация '{name}' не найдена.")

    def show_visualization(self, name: str):
        # Отображает визуализацию по имени
        if name not in self.visualizations:
            raise KeyError(f"Визуализация '{name}' не найдена.")
        self.visualizations[name].show()
