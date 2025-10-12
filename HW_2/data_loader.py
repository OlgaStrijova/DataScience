# Модуль для загрузки данных из различных источников (CSV, JSON, API)
import os
import json
import pandas as pd
import requests


class DataLoader:
    """Класс для загрузки данных из различных источников"""

    @staticmethod
    def load_csv(file_path: str, **kwargs) -> pd.DataFrame:
        #Загружает данные из CSV файла
        try:             
             return pd.read_csv(file_path, **kwargs)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {file_path} не найден")
      

# class DataLoader:
#     """Класс для загрузки данных из csv file"""

#     @staticmethod
#     def load_csv(file_path: str, **kwargs) -> pd.DataFrame:
#         try:
#             return pd.read_csv(file_path, **kwargs)
#         except FileNotFoundError:
#             raise FileNotFoundError(f"Файл {file_path} не найден")
#         except Exception as e:
#             raise Exception(f"Ошибка при загрузке CSV: {str(e)}")



    @staticmethod
    def load_json(file_path: str) -> pd.DataFrame:
        #Загружает данные из JSON файла
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return pd.DataFrame(data)

    @staticmethod
    def load_from_api(url: str, params: dict = None) -> pd.DataFrame:
        #Загружает данные из API
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return pd.DataFrame(response.json())
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка при запросе к API: {e}")
