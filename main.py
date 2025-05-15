import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def graph_top_5_and_least_5(max_5, min_5):
    plt.figure(figsize=(10, 6))
    countries_names = list(max_5['Country name']) + list(min_5['Country name'])
    ladder_scores = list(max_5['Ladder score']) + list(min_5['Ladder score'])
    colors = ['green'] * 5 + ['red'] * 5
    plt.bar(countries_names, ladder_scores, color=colors)
    plt.ylabel('Ladder Score')
    plt.title('Топ-10 стран по уровню счастья с указанием диапазона')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


def graph_ladder_score_distribution_by_regions(df):
    plt.figure(figsize=(15, 8))
    plt.title("Распределение уровня счастья по регионам",
              family='Serif',
              weight='bold',
              size=20)
    sns.kdeplot(
        data=df,
        x='Ladder score',
        hue='Regional indicator',
        fill=True,
        linewidth=2,
        common_norm=False,
        alpha=0.5,
        multiple='layer'
    )
    # Добавляем вертикальную линию среднего значения
    plt.axvline(df['Ladder score'].mean(),
                color='black',
                linestyle='--')
    plt.text(x=df['Ladder score'].mean() - 0.5,
             y=-0.13,
             s='Среднее значение счастья',
             size=8.5)
    plt.xlabel("Уровень счастья",
               fontsize=14,
               labelpad=10,
               color='black')
    plt.ylabel("Плотность распределения",
               fontsize=14,
               labelpad=10,
               color='black')
    plt.show()


def heating_map(corr_matrix):
    target_corr = corr_matrix["Ladder score"].sort_values(ascending=False)
    plt.figure(figsize=(6, 6))
    sns.barplot(x=target_corr.values,
                y=target_corr.index,
                hue=target_corr.index,
                palette="viridis")
    plt.title("Корреляции с Ladder score")
    plt.xlabel("Коэффициент корреляции")
    plt.show()


def life_ladder_of_top_5_countries_and_russia(data, max_5):
    selected = []
    sorted_data = data.sort_values(by='year')
    countries = max_5['Country name'].tolist() + ['Russia']
    for index, row in sorted_data.iterrows():
        countr = row['Country name']
        if countr in countries:
            selected.append([row['Country name'],
                             row['year'],
                             row['Life Ladder']])
    new_df = pd.DataFrame(selected)
    new_df.columns = ['Country name', 'year', 'Life Ladder']
    pivo = new_df.pivot(index='year',
                        columns='Country name',
                        values='Life Ladder')
    pivoted = pivo.interpolate()
    plt.figure(figsize=(10, 6))
    # Для каждой страны рисуем временной ряд
    for country in pivoted.columns:
        plt.plot(pivoted.index, pivoted[country], label=country)

    plt.title('Временные ряды для стран')
    plt.xlabel('Год')
    plt.ylabel('Уровень счастья')
    plt.legend()
    plt.grid(True)
    plt.show()


df = pd.read_csv('world-happiness-report-2024.csv',
                 sep=',', encoding='UTF-8')
data = pd.read_csv('world-happiness-report.csv',
                   sep=',', encoding='UTF-8')

color = ["#f4a6a6", "#f7c9a9", "#fde2a7", "#fff3bf",
         "#b7e3b7", "#a3d5cb", "#aec6ec"]
# sns.palplot(color)   #это чтобы нарисовать палитру цветов

duplicates_country = df[df.duplicated(subset="Country name")]
print('Количество дубликатов:', len(duplicates_country))

print('Пропуски:', df.isnull().sum().sum())

# проверка на выбросы (знаем, что индекс счастья от 0 до 10)
outliers = df[(df['Ladder score'] < 0) | (df['Ladder score'] > 10)]
print('Выбросы:', len(outliers))

# общая информация по таблице
df.info()

max_5 = df.sort_values(by='Ladder score', ascending=False).head(5)
min_5 = df.sort_values(by='Ladder score', ascending=False).tail(5)
print('Топ-5 самых счастливых стран:')
print(max_5[['Country name', 'Ladder score']].to_string(index=False))
print('Топ-5 самых несчастливых стран:')
print(min_5[['Country name', 'Ladder score']].to_string(index=False))

North_America = df[df["Regional indicator"] == "North America and ANZ"]
mean_america = North_America['Ladder score'].mean()
print('Среднее значение уровня счастья в регионе North America and ANZ:',
      mean_america)

factors = [
    'Logged GDP per capita',
    'Social support',
    'Healthy life expectancy',
    'Freedom to make life choices',
    'Generosity',
    'Ladder score'
]
corr_matrix = df[factors].corr()
print('Матрица корелляций')
print(corr_matrix)

print(heating_map(corr_matrix))
print(life_ladder_of_top_5_countries_and_russia(data, max_5))
print(graph_top_5_and_least_5(max_5, min_5))
print(graph_ladder_score_distribution_by_regions(df))




