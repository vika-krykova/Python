import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def load_wine_data(): # Загрузка данных о качестве вина
    url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'
    wine_data = pd.read_csv(url, delimiter=';')
    
    # создание категорий качества
    wine_data['quality_category'] = pd.cut(
        wine_data['quality'],
        bins=[0, 4, 6, 10],
        labels=['Низкое', 'Среднее', 'Высокое']
    )
    
    # Обработка пропущенных значений
    wine_data = wine_data.dropna()
    
    return wine_data

# Загрузка данных
wine_data = load_wine_data()

numeric_cols = wine_data.select_dtypes(include=[np.number]).columns
wine_data[numeric_cols] = wine_data[numeric_cols].astype(np.float32)

print(f"Размер датасета: {wine_data.shape}")
print(f"\nРаспределение качества:\n{wine_data['quality_category'].value_counts()}")


# Распределение показателей качества вин
plt.figure(figsize=(10, 6))
wine_data['quality'].hist(bins=20, edgecolor='black')
plt.xlabel('Качество вина (оценка)')
plt.ylabel('Количество')
plt.title('Распределение показателей качества вин')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Анализ выбросов в химических показателях 
key_features = ['alcohol', 'volatile acidity', 'citric acid', 'residual sugar']
plt.figure(figsize=(12, 8))
for i, feature in enumerate(key_features, 1):
    plt.subplot(2, 2, i)
    plt.boxplot(wine_data[feature])
    plt.title(f'Выбросы: {feature}')
    plt.ylabel(feature)
plt.tight_layout()
plt.show()

# Изучение корреляций между свойствами вина
plt.figure(figsize=(10, 8))
correlation_matrix = wine_data[numeric_cols].corr()
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0)
plt.title('Корреляция между свойствами вина')
plt.tight_layout()
plt.show()


# Сравнение химического состава вин разного качества 
plt.figure(figsize=(10, 4))
features_to_compare = ['alcohol', 'volatile acidity']

for i, feature in enumerate(features_to_compare, 1):
    plt.subplot(1, 2, i)
    # Векторизованная группировка
    quality_groups = wine_data.groupby('quality_category')[feature]
    data_to_plot = [group.values for name, group in quality_groups]
    plt.boxplot(data_to_plot, labels=quality_groups.groups.keys())
    plt.title(f'{feature} по качеству')
    plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#  Анализ связи алкоголя и качества 
plt.figure(figsize=(10, 6))
plt.scatter(wine_data['alcohol'], wine_data['quality'], alpha=0.5)
plt.xlabel('Содержание алкоголя (%)')
plt.ylabel('Качество вина')
plt.title('Связь между содержанием алкоголя и качеством вина')
plt.grid(True, alpha=0.3)

# Линия тренда
z = np.polyfit(wine_data['alcohol'], wine_data['quality'], 1)
p = np.poly1d(z)
plt.plot(wine_data['alcohol'], p(wine_data['alcohol']), "r--", alpha=0.8)
plt.tight_layout()
plt.show()

# Влияние уровня сахара на воспринимаемое качество
plt.figure(figsize=(8, 5))
sugar_by_quality = wine_data.groupby('quality_category')['residual sugar'].mean()
sugar_by_quality.plot(kind='bar')
plt.xlabel('Категория качества')
plt.ylabel('Средний уровень сахара')
plt.title('Влияние уровня сахара на качество')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Статистическая проверка различий между группами качества 
print("\nСтатистическая проверка различий (алкоголь по категориям качества):")

# Разделение данных по категориям качества
low_quality = wine_data[wine_data['quality_category'] == 'Низкое']['alcohol']
medium_quality = wine_data[wine_data['quality_category'] == 'Среднее']['alcohol']
high_quality = wine_data[wine_data['quality_category'] == 'Высокое']['alcohol']

print(f"Среднее содержание алкоголя:")
print(f"Низкое качество: {low_quality.mean():.2f}% (n={len(low_quality)})")
print(f"Среднее качество: {medium_quality.mean():.2f}% (n={len(medium_quality)})")
print(f"Высокое качество: {high_quality.mean():.2f}% (n={len(high_quality)})")

# ANOVA для 3 групп
f_stat, p_value_anova = stats.f_oneway(low_quality, medium_quality, high_quality)
print(f"\nANOVA тест: F={f_stat:.3f}, p={p_value_anova:.4f}")

if p_value_anova < 0.05:
    print("Существуют статистически значимые различия в содержании алкоголя между группами качества")
else:
    print("Нет статистически значимых различий в содержании алкоголя между группами качества")