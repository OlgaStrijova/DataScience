import psycopg2
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Подключение к БД postgres
conn = psycopg2.connect(
    dbname="postgres", 
    user="olga",       # логин
    password="olga",   # пароль
    host="localhost",
    port="5433"
)
conn.autocommit = True
cursor = conn.cursor()

# Создаем новую базу данных
cursor.execute("DROP DATABASE IF EXISTS ds_db;")
cursor.execute("CREATE DATABASE ds_db;")
cursor.close()
conn.close()
print ("База данных успешно создана")

# Подключение к созданной БД 
conn = psycopg2.connect(
    dbname="ds_db",    # имя созданной базы
    user="olga",       # логин
    password="olga",   # пароль
    host="localhost",
    port="5433"
)
cursor = conn.cursor()

# Создание схемы
cursor.execute("CREATE SCHEMA IF NOT EXISTS ds_hw3;")
conn.commit()

# Создание таблицы
cursor.execute("""
CREATE TABLE IF NOT EXISTS ds_hw3.loans (
    Loan_ID text null,
    Gender TEXT null,
    Married TEXT null,
    Dependents TEXT null,
    Education TEXT null,
    Self_Employed  TEXT null,
    ApplicantIncome NUMERIC null,
    CoapplicantIncome NUMERIC null,
    LoanAmount NUMERIC null,
    Loan_Amount_Term NUMERIC null,
    Credit_History NUMERIC null,
    Property_Area text  null
);
""")
conn.commit()
print ("Таблица успешно создана")


# Загружаем CSV
# df = pd.read_csv("loan-test.csv")
df = pd.read_csv("D:\\Data Science_1\\Data-Science\\HW_3\\loan-test.csv", na_values=["", "NULL"])

# Преобразуем NaN в None, чтобы psycopg2 корректно передал NULL в PostgreSQL
df = df.where(pd.notnull(df), None)

# Записываем в PostgreSQL
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO ds_hw3.loans (
            Loan_ID, Gender, Married, Dependents, Education, Self_Employed,
            ApplicantIncome, CoapplicantIncome, LoanAmount,
            Loan_Amount_Term, Credit_History, Property_Area
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, tuple(row))
conn.commit()
print ("Данные записаны в PostgreSQL")

#  Все заявки женатых мужчин
cursor.execute("""
SELECT Loan_ID, ApplicantIncome, LoanAmount
FROM ds_hw3.loans
WHERE Gender = 'Male' AND Married = 'Yes';
""")
print("Заявки женатых мужчин:") 
print(cursor.fetchall())

# Заявки с высоким доходом
cursor.execute("""
SELECT Loan_ID, ApplicantIncome, LoanAmount
FROM ds_hw3.loans
WHERE ApplicantIncome > 10000;
""")
print("Заявки с высоким доходом:") 
print(cursor.fetchall())

# Средний доход 
cursor.execute("SELECT AVG(ApplicantIncome) FROM ds_hw3.loans;")
print("Средний доход заявителей:", cursor.fetchone()[0])

# Количество кредитов по регионам
cursor.execute("""
SELECT Property_Area, COUNT(*) 
FROM ds_hw3.loans
GROUP BY Property_Area;
""")
print("Количество кредитов по регионам:")
print(cursor.fetchall())

# Средняя сумма кредита по образованию
cursor.execute("""
SELECT Education, AVG(LoanAmount)
FROM ds_hw3.loans
GROUP BY Education;
""")
print("Средняя сумма кредита по образованию:")
print(cursor.fetchall())

# Загружаем данные из базы обратно в DataFrame
query = """SELECT Loan_ID, Gender, Married, Dependents, Education, Self_Employed,
            ApplicantIncome, CoapplicantIncome, LoanAmount,
            Loan_Amount_Term, Credit_History, Property_Area FROM ds_hw3.loans;
        """
df_db = pd.read_sql(query, conn)

# Закрываем подключение, так как данные уже в DataFrame
conn.close() 

# Настройка стиля для графиков
sns.set_style("whitegrid")
plt.figure(figsize=(16, 6))

# Визуализация 1: Распределение суммы кредита по образованию   
plt.subplot(1, 2, 1)
sns.boxplot(x="education", y="loanamount", data=df_db)
plt.title("Распределение суммы кредита по образованию")
plt.xlabel("Образование")
plt.ylabel("Сумма кредита (LoanAmount)")

# Визуализация 2: Количество заявок по типу недвижимости   
plt.subplot(1, 2, 2)
sns.countplot(x="property_area", hue="married", data=df_db, palette="mako")
plt.title("Количество заявок по типу недвижимости и семейному положению")
plt.xlabel("Тип недвижимости (Property_Area)")
plt.ylabel("Количество заявок")
plt.legend(title="Семейное положение", loc="upper right")
plt.tight_layout()
plt.show()

# Визуализация 3: Гистограмма комбинированного дохода
# Создадим новый признак для более глубокого анализа
df_db["totalincome"] = df_db["applicantincome"] + df_db["coapplicantincome"]

plt.figure(figsize=(8, 5))
sns.histplot(df_db["totalincome"], bins=15, kde=True, color="indianred")
plt.title("Распределение общего дохода заявителей (Applicant + Coapplicant)")
plt.xlabel("Общий доход (TotalIncome)")
plt.ylabel("Частота")
plt.show()


# Визуализация 4: Средняя сумма кредита по регионам 
print("Средняя сумма кредита по регионам")
avg_loan = (
    df.groupby("Property_Area")["LoanAmount"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(6, 4))
sns.barplot(data=avg_loan, x="Property_Area", y="LoanAmount")
plt.title("Средняя сумма кредита по регионам")
plt.show()

# Визуализация 5: Корреляция числовых признаков   
print("Корреляция числовых признаков")
plt.figure(figsize=(8,6))
sns.heatmap(df_db.corr(numeric_only=True), annot=True, cmap="Blues")
plt.title("Корреляция числовых признаков")
plt.show()
