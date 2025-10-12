#Модуль для предобработки данных, обработки пропущенных значений и формирования отчета
import pandas as pd


class DataProcessor:
    #Класс для предобработки данных

    @staticmethod
    def check_missing_values(df: pd.DataFrame) -> pd.Series:
        
        #Возвращает количество пропущенных значений в каждом столбце
       
        return df.isnull().sum()

    @staticmethod
    def generate_missing_values_report(df: pd.DataFrame) -> pd.DataFrame:
        
        #Создает отчет по пропущенным значениям
        
        missing_counts = df.isnull().sum()
        missing_percent = (missing_counts / len(df)) * 100

        report = pd.DataFrame({
            "missing_count": missing_counts,
            "missing_percent": missing_percent
        })
        return report[report["missing_count"] > 0].sort_values(
            by="missing_percent",
            ascending=False
        )

    @staticmethod
    def fill_missing_values(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
        
        # Заполняет пропущенные значения стратегией:        
        df_filled = df.copy()                                     # создание копии DataFrame 

        for column in df_filled.columns:
            if df_filled[column].isnull().sum() == 0:
                continue

            if strategy == "fillna":                              # fillna: заполнение ''
                value = df_filled[column].fillna('')    
            elif strategy == "ffill":                             # ffill: методы заполнения вперед
                value = df_filled[column].ffill()[0]            
            elif strategy == "mode":                              # mode: наиболее частое значение
                value = df_filled[column].mode()[0] 
            elif strategy == "median":                            # median: медиана
                value = df_filled[column].median()
            elif strategy == "mean":                              # mean: среднее значение
                value = df_filled[column].mean()
            else:
                raise ValueError("Неподдерживаемая стратегия заполнения пропусков.")

            df_filled[column] = df_filled[column].fillna(value)
        print ("Пропуски заполнены методом " + strategy)
        return df_filled