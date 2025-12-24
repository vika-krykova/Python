import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns
from memory_profiler import memory_usage


def generate_test_datasets() -> dict:# Создание тестовых наборов данных разного размера
    return {
        '10^3': np.random.random(1000),
        '10^4': np.random.random(10000),
        '10^5': np.random.random(100000),
        '10^6': np.random.random(1000000)
    }

# Реализация операций на чистом питоне
def py_square(data):
    return [x ** 2 for x in data]

def py_sin(data):
    return [np.sin(x) for x in data]  # np.sin - для вычисления

def py_sum(data):
    return sum(data)

def py_max(data):
    return max(data)

#  операции с  NumPy
def np_square(data):
    return np.square(data)

def np_sin(data):
    return np.sin(data)

def np_sum(data):
    return np.sum(data)

def np_max(data):
    return np.max(data)

# Бенчмаркинг 
def benchmark_operation(py_func, np_func, data):
    results = {}
    
    # Измерение времени выполнения и потребления памяти  для чистого питона
    py_data = list(data) if isinstance(data, np.ndarray) else data
    start_time = time.time()
    _ = py_func(py_data)
    py_time = time.time() - start_time
    
    mem_usage = memory_usage((py_func, (py_data,)), interval=0.01)
    py_memory = max(mem_usage) - min(mem_usage)
    
    # Измерение времени выполнения и потребления памяти для NumPy
    start_time = time.time()
    _ = np_func(data)
    np_time = time.time() - start_time
    
    mem_usage = memory_usage((np_func, (data,)), interval=0.01)
    np_memory = max(mem_usage) - min(mem_usage)
    
    return {
        'py_time': py_time,
        'py_memory': py_memory,
        'np_time': np_time,
        'np_memory': np_memory
    }


def benchmark_all_operations():
   
    datasets = generate_test_datasets()
    
    operations = [
        ('square', py_square, np_square),
        ('sin', py_sin, np_sin),
        ('sum', py_sum, np_sum),
        ('max', py_max, np_max)
    ]
    
    results = {}
    
    for name, data in datasets.items():
        results[name] = {}
        for op_name, py_func, np_func in operations:
            results[name][op_name] = benchmark_operation(py_func, np_func, data)
    
    return results, list(datasets.keys()), [op[0] for op in operations]

# сравнительные графики 
def plot_results(results, dataset_sizes, operations):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    #  1 - Время выполнения
    ax1 = axes[0]
    x_positions = np.arange(len(dataset_sizes))
    width = 0.35
    
    for i, op in enumerate(operations):
        py_times = [results[size][op]['py_time'] for size in dataset_sizes]
        np_times = [results[size][op]['np_time'] for size in dataset_sizes]

        if op == 'square': 
            bars1 = ax1.bar(x_positions - width/2, py_times, width, 
                           label='Python', alpha=0.8, color='skyblue')
            bars2 = ax1.bar(x_positions + width/2, np_times, width, 
                           label='NumPy', alpha=0.8, color='lightcoral')
    
    ax1.set_xlabel('Размер данных')
    ax1.set_ylabel('Время выполнения - сек')
    ax1.set_title('Время выполнения операции square')
    ax1.set_xticks(x_positions)
    ax1.set_xticklabels(dataset_sizes)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    for bars in [bars1, bars2]: # Добавление значений на столбцы
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}', ha='center', va='bottom', fontsize=8)
    
 #  2 - Потребление памяти 
    ax2 = axes[1]
    
    for op in operations:
        py_mem = [results[size][op]['py_memory'] for size in dataset_sizes]
        np_mem = [results[size][op]['np_memory'] for size in dataset_sizes]
        
        ax2.plot(dataset_sizes, py_mem, marker='o', linewidth=2, 
                label=f'{op} (Python)', alpha=0.8)
        ax2.plot(dataset_sizes, np_mem, marker='s', linewidth=2, 
                label=f'{op} (NumPy)', alpha=0.8, linestyle='--')
    
    ax2.set_xlabel('Размер данных')
    ax2.set_ylabel('Потребление памяти МБ')
    ax2.set_title('Потребление памяти операций')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax2.grid(True, alpha=0.3)

    #  3 - Тепловая карта ускорения 
    ax3 = axes[2]
    speedup_matrix = np.zeros((len(dataset_sizes), len(operations)))
    
    for i, size in enumerate(dataset_sizes):
        for j, op in enumerate(operations):
            py_time = results[size][op]['py_time']
            np_time = results[size][op]['np_time']
            speedup_matrix[i, j] = py_time / np_time if np_time > 0 else 0
    
    im = ax3.imshow(speedup_matrix, cmap='YlOrRd', aspect='auto')  # Создание тепловой карты
    
    # Настройка подписей
    ax3.set_xticks(np.arange(len(operations)))
    ax3.set_yticks(np.arange(len(dataset_sizes)))
    ax3.set_xticklabels(operations)
    ax3.set_yticklabels(dataset_sizes)
    

    for i in range(len(dataset_sizes)):   # Добавление значений в ячейки
        for j in range(len(operations)):
            text = ax3.text(j, i, f'{speedup_matrix[i, j]:.1f}x',
                           ha="center", va="center", 
                           color="black" if speedup_matrix[i, j] < 5 else "white",
                           fontweight='bold')
            
    ax3.set_xlabel('Операция')
    ax3.set_ylabel('Размер данных')
    ax3.set_title('Ускорение NumPy над Python')
    

    plt.colorbar(im, ax=ax3, label='Коэффициент ускорения')# Добавление цветовой шкалы
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    results, dataset_sizes, operations = benchmark_all_operations()  #  бенчмаркинг
    
    plot_results(results, dataset_sizes, operations)
