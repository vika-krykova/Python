import time
import random
from functools import wraps, reduce, lru_cache
from typing import List, Tuple, Callable, Any


def timing_decorator(func: Callable) -> Callable: # декоратор для измерения времени выполнения функций
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} executed in {end-start:.4f} seconds")
        return result
    return wrapper


@lru_cache(maxsize=None) # functools.lru_cache для мемоизации
def heavy_computation(n: int) -> int:
    time.sleep(0.001)  # Имитация тяжелых вычислений
    # Функциональный стиль: map + sum вместо цикла
    return sum(map(lambda x: x * x, range(1, n + 1)))


def compose(*functions: Callable) -> Callable: # pipeline обработки данных с помощью композиции функций
    return reduce(lambda f, g: lambda x: f(g(x)), functions)


def normalize_data(data: List[int]) -> List[float]:
    if not data:
        return []
    min_val, max_val = min(data), max(data)
    if max_val == min_val:
        return [0.0] * len(data)
    # Функциональный стиль: map вместо цикла
    return list(map(lambda x: (x - min_val) / (max_val - min_val), data))


def calculate_metrics(data: List[float]) -> Tuple[float, float, float]:
    if not data:
        return 0.0, 0.0, 0.0
    
    mean = reduce(lambda acc, x: acc + x, data, 0.0) / len(data) # Среднее значение через reduce
    
    sorted_data = sorted(data)  # Медиана с использованием sorted
    n = len(sorted_data)
    mid = n // 2
    median = (sorted_data[mid] + sorted_data[~mid]) / 2 if n % 2 == 0 else sorted_data[mid]
    
    # Стандартное отклонение через reduce
    variance = reduce(lambda acc, x: acc + (x - mean) ** 2, data, 0.0) / len(data)
    std_dev = variance ** 0.5
    
    return mean, median, std_dev


def generate_report(metrics: Tuple[float, float, float]) -> str:
    mean, median, std_dev = metrics
    return f"Metrics: Mean={mean:.4f}, Median={median:.4f}, StdDev={std_dev:.4f}"


analysis_pipeline = compose(
    generate_report,    # 3-й шаг: генерация отчета
    calculate_metrics,  # 2-й шаг: вычисление метрик
    normalize_data      # 1-й шаг: нормализация данных
)


@timing_decorator
def run_experiment(data_size: int) -> str:
    try:
        # Генерация данных с помощью генераторного выражения
        data = (random.randint(1, 1000) for _ in range(data_size))
        
        # Функциональная обработка: filter + map
        processed_data = list(map(
            lambda x: heavy_computation(x % 20 + 1),
            filter(lambda x: x > 0, data)  # Фильтрация положительных
        ))
        
        # Запуск конвейера обработки
        return analysis_pipeline(processed_data)
    
    except ValueError as e:
        return f"Value error: {str(e)}"
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


# Сравнительный анализ на разных размерах данных
def run_single_experiment(size: int) -> Tuple[int, str]:
    return size, run_experiment(size)


def display_results(results: List[Tuple[int, str]]) -> None:
    print("\n" + "-"*40)
    print("Результаты сравнительного анализа:")
    print("-"*40)
    
    for size, result in results:
        print(f"\nData size: {size}")
        print(f"Result: {result}")


def comparative_analysis() -> None:
    sizes = [200, 500, 1000]
    
    # map для запуска экспериментов
    results = list(map(run_single_experiment, sizes))
    
    display_results(results)


def main() -> None:
    try:
        comparative_analysis()
    except KeyboardInterrupt:
        print("\nПрограмма прервана")
    except MemoryError:
        print("Ошибка: недостаточно памяти")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        print("\nВыполнение завершено")


if __name__ == "__main__":
    main()
