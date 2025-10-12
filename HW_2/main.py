import pandas as pd
from data_loader import DataLoader
from data_processing import DataProcessor
from data_visualization import DataVisualizer


def main():
    # Загрузка данных
    loader = DataLoader()
    df = loader.load_csv("D:\\Data Science_1\\DS_examples\\HW_2\\financial_market_daily.csv")

    # Проверка что данные загружены    
    df.describe()
    print("Размер данных:", df.shape)
    print("Колонки:", df.columns.tolist())
    print(df.head())
   

    # Проверка пропущенных значений
    processor = DataProcessor()
    missing_report = processor.generate_missing_values_report(df)
    print("Отчет по пропущенным значениям:")
    print(missing_report)

    # # Заполнение пропусков конкретным значением 
    df_filled = processor.fill_missing_values(df, strategy="ffill")       # fillna: заполнение конкретным значением

    # Визуализация данных
    df['Date'] = pd.to_datetime(df['Date'])                               # Преобразование 'Date' в формат даты

    visualizer = DataVisualizer()

    # Линейный график: Тренд выручки с течением времени
    visualizer.add_line_plot(
        name="Revenue_Trend",
        df=df,
        x_column="Date",
        y_column="AI_Revenue_USD_Mn"
    )

    # Диаграмма рассеяния: Влияние затрат на R&D на выручку от ИИ
    visualizer.add_scatter_plot(
        name="RnD_vs_Revenue",
        df=df,
        x_column="R&D_Spending_USD_Mn",
        y_column="AI_Revenue_USD_Mn"
    )

    #  Гистограмма: Распределение темпов роста
    visualizer.add_histogram(
        name="Growth_Distribution",
        df=df,
        column="AI_Revenue_Growth_%"
    )

    # Отображение графиков 
    visualizer.show_visualization("Revenue_Trend")
    visualizer.show_visualization("RnD_vs_Revenue")
    visualizer.show_visualization("Growth_Distribution")

    #  Демонстрация удаления (график не будет показан, если его удалить)
    # visualizer.remove_visualization("Revenue_Trend")
    # print("График 'Revenue_Trend' удален из контейнера.")


if __name__ == "__main__":
    main()