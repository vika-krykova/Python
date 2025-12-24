import pandas as pd
import numpy as np
import polars as pl
import time
import matplotlib.pyplot as plt
import seaborn as sns
from memory_profiler import memory_usage

# Создание датасета
def generate_large_dataset(n_rows=1000000):
    return pd.DataFrame({
        'id': range(n_rows),
        'timestamp': pd.date_range('2020-01-01', periods=n_rows, freq='1min'),
        'category': np.random.choice(['A', 'B', 'C', 'D'], n_rows),
        'value1': np.random.normal(0, 1, n_rows),
        'value2': np.random.exponential(1, n_rows),
        'value3': np.random.randint(0, 100, n_rows)
    })

# Фильтрация и агрегация
def pandas_filter_aggregate(df):
    filtered = df[df['value1'] > 0]
    return filtered.groupby('category').agg({'value2': ['mean', 'std', 'count']})

def pandas_pyarrow_filter_aggregate(df):
    try:
        df_pyarrow = df.copy()
        df_pyarrow['category'] = df_pyarrow['category'].astype('string[pyarrow]')
        filtered = df_pyarrow[df_pyarrow['value1'] > 0]
        return filtered.groupby('category').agg({'value2': ['mean', 'std', 'count']})
    except ImportError:
        return pandas_filter_aggregate(df)

def polars_filter_aggregate(df): 
    pl_df = pl.from_pandas(df)
    return (pl_df.filter(pl.col('value1') > 0)
              .group_by('category')
              .agg([pl.mean('value2').alias('avg_value'),
                    pl.std('value2').alias('std_value'),
                    pl.len().alias('count')])
              .sort('avg_value', descending=True))

# Группировка со статистиками
def pandas_groupby_stats(df):
    return df.groupby('category').agg({
        'value1': ['sum', 'mean', 'count'],
        'value2': ['sum', 'mean'],
        'value3': ['min', 'max', 'mean']
    })

def pandas_pyarrow_groupby_stats(df):
    try:
        df_pyarrow = df.copy()
        df_pyarrow['category'] = df_pyarrow['category'].astype('string[pyarrow]')
        return df_pyarrow.groupby('category').agg({
            'value1': ['sum', 'mean', 'count'],
            'value2': ['sum', 'mean'],
            'value3': ['min', 'max', 'mean']
        })
    except ImportError:
        return pandas_groupby_stats(df)

def polars_groupby_stats(df):
    pl_df = pl.from_pandas(df)
    return pl_df.group_by('category').agg([
        pl.sum('value1').alias('sum_value1'),
        pl.mean('value1').alias('mean_value1'),
        pl.count('value1').alias('count_value1'),
        pl.sum('value2').alias('sum_value2'),
        pl.mean('value2').alias('mean_value2'),
        pl.min('value3').alias('min_value3'),
        pl.max('value3').alias('max_value3'),
        pl.mean('value3').alias('mean_value3')
    ])

def pandas_join(df):
    df1 = df[['id', 'category', 'value1']].copy()
    df2 = df[['id', 'value2', 'value3']].copy()
    return pd.merge(df1, df2, on='id', how='inner')

def pandas_pyarrow_join(df):
    try:
        df_pyarrow = df.copy()
        df_pyarrow['category'] = df_pyarrow['category'].astype('string[pyarrow]')
        df1 = df_pyarrow[['id', 'category', 'value1']].copy()
        df2 = df_pyarrow[['id', 'value2', 'value3']].copy()
        return pd.merge(df1, df2, on='id', how='inner')
    except ImportError:
        return pandas_join(df)

def polars_join(df):
    pl_df = pl.from_pandas(df)
    df1 = pl_df.select(['id', 'category', 'value1'])
    df2 = pl_df.select(['id', 'value2', 'value3'])
    return df1.join(df2, on='id', how='inner')

# Скользящее среднее
def pandas_rolling(df):
    df_sorted = df.sort_values('timestamp')
    df_sorted['rolling_avg'] = df_sorted['value1'].rolling(window=5).mean()
    return df_sorted

def pandas_pyarrow_rolling(df):
    try:
        df_pyarrow = df.copy()
        df_pyarrow['category'] = df_pyarrow['category'].astype('string[pyarrow]')
        df_sorted = df_pyarrow.sort_values('timestamp')
        df_sorted['rolling_avg'] = df_sorted['value1'].rolling(window=5).mean()
        return df_sorted
    except ImportError:
        return pandas_rolling(df)

def polars_rolling(df):
    pl_df = pl.from_pandas(df)
    return pl_df.sort('timestamp').with_columns(
        pl.col('value1').rolling_mean(window_size=5).alias('rolling_avg')
    )

# Временные ряды
def pandas_resample(df):
    df_resampled = df.set_index('timestamp').resample('D').agg({
        'value1': 'mean',
        'value2': 'sum',
        'value3': 'count'
    })
    return df_resampled

def pandas_pyarrow_resample(df):
    try:
        df_pyarrow = df.copy()
        df_pyarrow['category'] = df_pyarrow['category'].astype('string[pyarrow]')
        df_resampled = df_pyarrow.set_index('timestamp').resample('D').agg({
            'value1': 'mean',
            'value2': 'sum',
            'value3': 'count'
        })
        return df_resampled
    except ImportError:
        return pandas_resample(df)

def polars_resample(df):
    pl_df = pl.from_pandas(df)
    return (pl_df.set_sorted('timestamp')
              .group_by_dynamic('timestamp', every='1d')
              .agg([
                  pl.mean('value1').alias('mean_value1'),
                  pl.sum('value2').alias('sum_value2'),
                  pl.count('value3').alias('count_value3')
              ]))

# Бенчмаркинг
def benchmark_operation(func, df, name):
    start_time = time.time()
    mem_usage = memory_usage((func, (df,)), interval=0.01)
    result = func(df)
    end_time = time.time()
    
    return {
        'time': end_time - start_time,
        'memory': max(mem_usage) - min(mem_usage),
        'name': name
    }

# Удобство API и читаемость
def analyze_api_readability():
    print("\n--- Удобство API и читаемость кода ---")
    print("\nСравнение синтаксиса:")
    print("-" * 40)
    print("Pandas: df[df['col'] > 0].groupby('cat').agg({'val': 'mean'})")
    print("Polars: df.filter(pl.col('col') > 0).group_by('cat').agg(pl.mean('val'))")
    print("\nВыводы:")
    print("Pandas: более знакомый синтаксис")
    print("Polars: лучше читаемость через метод цепочек")
    print("Pandas+PyArrow: баланс знакомства и производительности")

# Отчет
def run_benchmarks():
    df = generate_large_dataset(500000)
    
    operations = [
        ('Фильтрация', pandas_filter_aggregate, pandas_pyarrow_filter_aggregate, polars_filter_aggregate),
        ('Группировка', pandas_groupby_stats, pandas_pyarrow_groupby_stats, polars_groupby_stats),
        ('JOIN', pandas_join, pandas_pyarrow_join, polars_join),
        ('Скользящее среднее', pandas_rolling, pandas_pyarrow_rolling, polars_rolling),
        ('Resampling', pandas_resample, pandas_pyarrow_resample, polars_resample)
    ]
    
    results = []
    
    for op_name, pandas_func, pyarrow_func, polars_func in operations:
        print(f"\n{op_name}:")
        results.append(benchmark_operation(pandas_func, df, 'pandas'))
        results.append(benchmark_operation(pyarrow_func, df, 'pandas_pyarrow'))
        results.append(benchmark_operation(polars_func, df, 'polars'))
        print(f"  Pandas: {results[-3]['time']:.3f}s (память: {results[-3]['memory']:.1f} MB), "
              f"Pandas+PyArrow: {results[-2]['time']:.3f}s (память: {results[-2]['memory']:.1f} MB), "
              f"Polars: {results[-1]['time']:.3f}s (память: {results[-1]['memory']:.1f} MB)")
    
    return results

def generate_report(results):
    # Данные для графиков
    operations_names = ['Фильтрация', 'Группировка', 'JOIN', 'Скользящее среднее', 'Resampling']
    op_count = len(operations_names)
    
    pandas_times = [results[i*3]['time'] for i in range(op_count)]
    pyarrow_times = [results[i*3+1]['time'] for i in range(op_count)]
    polars_times = [results[i*3+2]['time'] for i in range(op_count)]
    
    pandas_memory = [results[i*3]['memory'] for i in range(op_count)]
    pyarrow_memory = [results[i*3+1]['memory'] for i in range(op_count)]
    polars_memory = [results[i*3+2]['memory'] for i in range(op_count)]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Время выполнения каждой операции
    ax1 = axes[0, 0]
    x = np.arange(op_count)
    width = 0.25
    
    ax1.bar(x - width, pandas_times, width, label='Pandas', color='skyblue')
    ax1.bar(x, pyarrow_times, width, label='Pandas+PyArrow', color='lightgreen')
    ax1.bar(x + width, polars_times, width, label='Polars', color='salmon')
    
    ax1.set_xlabel('Операции')
    ax1.set_ylabel('Время (сек)')
    ax1.set_title('Время выполнения операций')
    ax1.set_xticks(x)
    ax1.set_xticklabels(operations_names, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 2. Пиковое использование памяти
    ax2 = axes[0, 1]
    ax2.bar(x - width, pandas_memory, width, label='Pandas', color='skyblue')
    ax2.bar(x, pyarrow_memory, width, label='Pandas+PyArrow', color='lightgreen')
    ax2.bar(x + width, polars_memory, width, label='Polars', color='salmon')
    
    ax2.set_xlabel('Операции')
    ax2.set_ylabel('Память (MB)')
    ax2.set_title('Пиковое использование памяти')
    ax2.set_xticks(x)
    ax2.set_xticklabels(operations_names, rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. Удобство API и читаемость кода
    ax3 = axes[1, 0]
    
    # Оценка удобства API (оценки от 1 до 10)
    api_criteria = ['Синтаксис', 'Читаемость', 'Кривая обучения', 'Документация', 'Сообщество']
    pandas_scores = [9, 7, 9, 10, 10]
    pyarrow_scores = [9, 7, 9, 8, 10]
    polars_scores = [7, 9, 6, 7, 6]
    
    x_criteria = np.arange(len(api_criteria))
    width = 0.25
    
    ax3.bar(x_criteria - width, pandas_scores, width, label='Pandas', color='skyblue', alpha=0.8)
    ax3.bar(x_criteria, pyarrow_scores, width, label='Pandas+PyArrow', color='lightgreen', alpha=0.8)
    ax3.bar(x_criteria + width, polars_scores, width, label='Polars', color='salmon', alpha=0.8)
    
    ax3.set_xlabel('Критерии')
    ax3.set_ylabel('Оценка (1-10)')
    ax3.set_title('Удобство API и читаемость кода')
    ax3.set_xticks(x_criteria)
    ax3.set_xticklabels(api_criteria, rotation=45, ha='right')
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.set_ylim(0, 11)
    
    ax4 = axes[1, 1]
    ax4.axis('off')

    plt.suptitle('Сравнение Polars, Pandas и Pandas+PyArrow', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Сравнение Polars, Pandas и Pandas+PyArrow")
    print("-" * 50)
    
    analyze_api_readability()
    
    print("\n" + "-" * 50)
    print("Бенчмаркинг производительности и использования памяти")
    print("Размер датасета: 500,000 строк")
    print("-" * 50)
    
    results = run_benchmarks()
    
    print("\n" + "-" * 50)
    print("Визуализация результатов")
    print("-" * 50)
    generate_report(results)