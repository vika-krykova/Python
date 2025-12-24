import random
import math
import asyncio
import json
from functools import partial, reduce
from itertools import combinations
from typing import Generator, Tuple, List, Dict, Any
import plotly.graph_objects as go
import webbrowser
import os


# Генерация точек
def generate_points(n: int, bounds: Tuple[float, float] = (0, 100)) -> Generator[Tuple[float, float, float], None, None]:
    low, high = bounds
    for _ in range(n):
        yield (
            random.uniform(low, high),
            random.uniform(low, high),
            random.uniform(low, high)
        )

# Расстояние между двумя точками
def euclidean_distance(p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

# Генерация дорог между точками
def generate_roads(points: List[Tuple[float, float, float]], bidirectional_ratio: float = 0.5) -> Generator[Tuple[int, int, float], None, None]:
    if len(points) < 2:
        return

    pairs = filter(lambda p: p[0] < p[1], combinations(range(len(points)), 2))

    for i, j in pairs:
        distance = euclidean_distance(points[i], points[j])
        yield (i, j, distance)
        if random.random() < bidirectional_ratio:
            yield (j, i, distance)


# Феромоны
def initialize_pheromones(points: List[Tuple[float, float, float]]) -> Dict[Tuple[int, int], float]:
    n = len(points)
    return {(i, j): 1.0 for i in range(n) for j in range(n) if i != j}

# Вероятность перехода
def transition_probability(pheromone: Dict[Tuple[int, int], float],
                          distances: Dict[Tuple[int, int], float],
                          alpha: float, beta: float,
                          current: int, unvisited: set) -> int:
    if not unvisited:
        return -1
    
    def score(j: int) -> float:
        p = pheromone.get((current, j), 1.0)
        d = distances.get((current, j), 1.0)
        if d == 0:
            return 0
        return (p ** alpha) * ((1.0 / d) ** beta) 

    scores = list(map(score, unvisited))
    total = sum(scores)

    if total == 0:
        return random.choice(list(unvisited))

    probabilities = [s / total for s in scores]
    r = random.random()
    cumulative = 0

    for node, prob in zip(unvisited, probabilities):
        cumulative += prob
        if r <= cumulative:
            return node

    return list(unvisited)[-1]

# Муравьи строят путь
def construct_path(pheromone: Dict[Tuple[int, int], float],
                  points: List[Tuple[float, float, float]],
                  alpha: float = 1, beta: float = 2) -> List[int]:

    n = len(points)
    if n <= 1:
        return list(range(n))

    distances = {(i, j): euclidean_distance(points[i], points[j])
                 for i in range(n) for j in range(n) if i != j}

    start = random.randrange(n)
    path = [start]

    unvisited = set(range(n)) - {start}

    choose_next = partial(transition_probability, pheromone, distances, alpha, beta)

    while unvisited:
        nxt = choose_next(path[-1], unvisited)
        if nxt == -1:
            break
        path.append(nxt)
        unvisited.remove(nxt)

    return path

# Длина пути
def calculate_path_length(path: List[int], points: List[Tuple[float, float, float]]) -> float:
    if len(path) < 2:
        return 0.0

    total = 0.0
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        total += euclidean_distance(points[a], points[b])
    
    total += euclidean_distance(points[path[-1]], points[path[0]])
    return total

# Испарение феромонов
def evaporate_pheromones(pheromone: Dict[Tuple[int, int], float], evaporation_rate: float = 0.1):
    return {edge: (1 - evaporation_rate) * v for edge, v in pheromone.items()}

# Обновление феромонов
def update_pheromones(pheromone: Dict[Tuple[int, int], float],
                     best_path: List[int],
                     points: List[Tuple[float, float, float]],
                     Q: float = 100.0):
    pheromone = evaporate_pheromones(pheromone)
    L = calculate_path_length(best_path, points)

    if L > 0:
        deposit = Q / L
        for i in range(len(best_path)):
            a, b = best_path[i], best_path[(i + 1) % len(best_path)]  
            pheromone[(a, b)] = pheromone.get((a, b), 1.0) + deposit

    return pheromone

# основной генератор
def ant_colony_optimization(points: List[Tuple[float, float, float]],
                           iterations: int = 20,
                           num_ants: int = None):

    if len(points) < 3:
        print("Ошибка: нужно минимум 3 точки")
        yield [], 0.0
        return

    if num_ants is None:
        num_ants = min(10, len(points))

    pheromone = initialize_pheromones(points)

    for iteration in range(iterations):  
        paths = [construct_path(pheromone, points) for _ in range(num_ants)]

        valid = [p for p in paths if len(p) == len(points)]
        if not valid:
            continue

        best = min(valid, key=lambda p: calculate_path_length(p, points))
        pheromone = update_pheromones(pheromone, best, points)
        yield best, calculate_path_length(best, points)


def create_final_plot(points: List[Tuple[float, float, float]],
                     best_path: List[int],
                     best_length: float,
                     lengths_history: List[float]) -> None:

    fig_3d = go.Figure()

    # Точки
    x_all, y_all, z_all = zip(*points)
    fig_3d.add_trace(go.Scatter3d(
        x=x_all, y=y_all, z=z_all,
        mode='markers',
        marker=dict(size=6, color='blue'),
        name='Точки'
    ))

    # Линия маршрута 
    if best_path and len(best_path) > 1:
        # Создаем замкнутый путь
        x, y, z = [], [], []
        for i in range(len(best_path) + 1):
            idx = best_path[i % len(best_path)]
            x.append(points[idx][0])
            y.append(points[idx][1])
            z.append(points[idx][2])

        fig_3d.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines+markers',
            line=dict(color='red', width=4), 
            marker=dict(size=4, color='red'),
            name=f'Лучший путь'
        ))

    fig_3d.update_layout(
        title=f'Муравьиный алгоритм — лучший маршрут<br>Длина: {best_length:.2f}',
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            bgcolor='white',
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.6))
        ),
        width=900,
        height=700,
        showlegend=True
    )

    print("\nЛучший путь:", best_path)
    print("Длина пути:", best_length)

    filename = "3d_plot_result.html"
    fig_3d.write_html(filename)

    try:
        fig_3d.show()
    except Exception as e:
        print(f"Ошибка при отображении графика: {e}")

    # Автоматическое открытие
    try:
        webbrowser.open('file://' + os.path.abspath(filename))
        print("График сохранён и автоматически открыт.")
    except Exception as e:
        print(f"Ошибка при открытии графика: {e}")

# Асинхронный запуск
async def run_algorithm_async(points: List[Tuple[float, float, float]],
                            iterations: int = 15):

    print(f"Запуск ACO для {len(points)} точек...")
    lengths = []
    best_path, best_len = [], float('inf')

    for i, (path, length) in enumerate(ant_colony_optimization(points, iterations, 10)):
        lengths.append(length)

        if 0 < length < best_len:
            best_len = length
            best_path = path.copy()

        if i % 2 == 0:
            print(f"  Итерация {i}: длина={length:.2f}, лучшая={best_len:.2f}")

        await asyncio.sleep(0.01)

    return best_path, best_len, lengths


# Демонстрации
async def demo_small():
    print("\nДемонстрация (15 точек)")
    points = list(generate_points(15))
    best_path, best_length, history = await run_algorithm_async(points, iterations=20)
    create_final_plot(points, best_path, best_length, history)


async def demo_medium():
    print("\nДемонстрация (30 точек)")
    points = list(generate_points(30))
    roads = list(generate_roads(points, 0.7))
    print("Сгенерировано дорог:", len(roads))
    best_path, best_length, history = await run_algorithm_async(points, iterations=15)
    create_final_plot(points, best_path, best_length, history)


def create_datasets():
    print("\nСоздание наборов данных...")

    sizes = [50, 100, 200]
    for size in sizes:
        points = list(generate_points(size))
        fname = f"dataset_{size}_points.json"

        try:
            with open(fname, 'w') as f:
                json.dump(points, f, indent=2)

            roads = list(generate_roads(points))
            print(f"✓ {size} точек, сохранено → {fname}")
        except Exception as e:
            print(f"Ошибка сохранения ({size}): {e}")


async def main():
    while True:
        print("\n" + "-"*50)
        print("Генератор координат и маршрутов")
        print("-"*50)
        print("1 — Быстрая демонстрация (15 точек)")
        print("2 — Средняя демонстрация (30 точек)")
        print("3 — Создать наборы данных")
        print("4 — Выход")
        print("-"*50)

        choice = input("Выбор: ").strip()

        if choice == "1":
            await demo_small()
        elif choice == "2":
            await demo_medium()
        elif choice == "3":
            create_datasets()
        elif choice == "4":
            print("Выход.")
            break
        else:
            print("Неверный ввод.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрервано пользователем")
    except Exception as e:
        print(f"Произошла ошибка: {e}")