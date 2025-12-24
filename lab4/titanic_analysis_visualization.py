import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


titanic_df = sns.load_dataset('titanic') # Загрузка датасета Titanic

#  Анализ структуры данных
print("--- Анализ структуры данных ---")
print("\n Типы столбцов:")
print(titanic_df.dtypes)
print("\n Пропущенные значения:")
print(titanic_df.isnull().sum())
print("\n Статистическое описание числовых признаков:")
print(titanic_df.describe())

# Обработка пропущенных значений
titanic_df['age'] = titanic_df['age'].fillna(titanic_df['age'].median())
titanic_df['embarked'] = titanic_df['embarked'].fillna(titanic_df['embarked'].mode()[0])
titanic_df['fare'] = titanic_df['fare'].fillna(titanic_df['fare'].median())

# Группировка данных по полу и классу каюты
print("\n--- Выживаемость по полу и классу каюты ---")
survival_by_sex_class = titanic_df.groupby(['sex', 'class'])['survived'].mean().reset_index()
survival_by_sex_class['survival_rate'] = (survival_by_sex_class['survived'] * 100).round(1)
print(survival_by_sex_class[['sex', 'class', 'survival_rate']])

# cоздание новых признаков
def create_features(df):
    df['age_group'] = pd.cut(df['age'],  # Возрастные группы
                             bins=[0, 18, 30, 50, 100],
                             labels=['child', 'young', 'adult', 'senior'])
    df['family_size'] = df['sibsp'] + df['parch'] # Размер семьи
    return df

titanic_df = create_features(titanic_df)

# комплексная витрина данных
fig = plt.figure(figsize=(16, 12))
fig.suptitle('Анализ данных Titanic', fontsize=16, fontweight='bold')

# тепловая карта
ax1 = plt.subplot(2, 2, 1)
numeric_cols = ['survived', 'pclass', 'age', 'sibsp', 'parch', 'fare']
corr_matrix = titanic_df[numeric_cols].corr()
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax1)
ax1.set_title('Матрица корреляций')
ax1.set_xlabel('Признаки')
ax1.set_ylabel('Признаки')

# Распределение возрастов пассажиров с разбивкой по полу и выживаемости
ax2 = plt.subplot(2, 2, 2)
sns.histplot(data=titanic_df, x='age', hue='survived', 
             kde=True, bins=30, ax=ax2, alpha=0.6)
ax2.set_title('Распределение возрастов по выживаемости')
ax2.set_xlabel('Возраст')
ax2.set_ylabel('Количество пассажиров')
ax2.legend(title='Выжил', labels=['Нет', 'Да'])

# Количество выживших в разрезе класса каюты и порта посадки
ax3 = plt.subplot(2, 2, 3)
survival_counts = titanic_df.groupby(['class', 'embarked', 'survived']).size().unstack()
survival_counts.plot(kind='bar', stacked=True, ax=ax3, color=['#ff6b6b', '#51cf66'])
ax3.set_title('Выживаемость по классу и порту посадки')
ax3.set_xlabel('Класс и порт')
ax3.set_ylabel('Количество пассажиров')
ax3.legend(title='Выжил', labels=['Нет', 'Да'])
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)

# Ящик с усами 
ax4 = plt.subplot(2, 2, 4)
sns.boxplot(data=titanic_df, x='class', y='fare', ax=ax4)
ax4.set_title('Распределение стоимости билета по классам')
ax4.set_xlabel('Класс каюты')
ax4.set_ylabel('Стоимость билета ($)')

plt.tight_layout()
plt.show()

# Интерактивная визуализация 
def create_interactive_dashboard(df):
    """Требование 5: Интерактивная визуализация"""
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle('Интерактивная визуализация Titanic (фильтр: возраст 18-60; все классы)', 
                 fontsize=14, fontweight='bold')
    
    # Применение фильтров
    age_filter = (18, 60)
    class_filter = [1, 2, 3]
    filtered_df = df[
        (df['age'].between(*age_filter)) &
        (df['pclass'].isin(class_filter))
    ].copy()
    
    gs = plt.GridSpec(2, 2, figure=fig) # Сетка для графиков
    
    # График выживаемости по полу
    ax1 = fig.add_subplot(gs[0, 0])
    gender_survival = filtered_df.groupby('sex')['survived'].mean()
    gender_survival.plot(kind='bar', color=['#ff6b6b', '#4d96ff'], ax=ax1)
    ax1.set_title('Выживаемость по полу')
    ax1.set_xlabel('Пол')
    ax1.set_ylabel('Доля выживших')
    ax1.set_ylim(0, 1)
    for i, v in enumerate(gender_survival):
        ax1.text(i, v + 0.02, f'{v:.2%}', ha='center')
    
    # График распределения по классам
    ax2 = fig.add_subplot(gs[0, 1])
    class_counts = filtered_df['pclass'].value_counts().sort_index()
    class_counts.plot(kind='pie', autopct='%1.1f%%', colors=['#ffd93d', '#6bcf7f', '#4d96ff'], ax=ax2)
    ax2.set_title('Распределение пассажиров по классам')
    ax2.set_ylabel('')
    
    # График возраст и стоимость билета
    ax3 = fig.add_subplot(gs[1, :])
    scatter = ax3.scatter(filtered_df['age'], filtered_df['fare'], 
                         c=filtered_df['survived'], cmap='coolwarm', alpha=0.6)
    ax3.set_title('Возраст и стоимость билета')
    ax3.set_xlabel('Возраст')
    ax3.set_ylabel('Стоимость билета')
    plt.colorbar(scatter, ax=ax3, label='Выжил (0=Нет, 1=Да)')
    
    # инфа о фильтрах
    info_text = f"Отфильтровано записей: {len(filtered_df)} из {len(df)}\n"
    info_text += f"Возраст: {age_filter[0]}-{age_filter[1]} лет\n"
    info_text += f"Классы: {', '.join(map(str, class_filter))}"
    fig.text(0.5, 0.01, info_text, ha='center', fontsize=10, 
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray"))
    
    plt.tight_layout()
    return fig

interactive_fig = create_interactive_dashboard(titanic_df) # создание, отображение визуализации
plt.show()