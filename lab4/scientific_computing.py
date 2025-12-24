import numpy as np
import scipy.optimize
import scipy.fft
import scipy.signal
import matplotlib.pyplot as plt
import time


def rosenbrock(x): # Функция Розенброка
    return np.sum(100.0 * (x[1:] - x[:-1]**2.0)**2.0 + (1 - x[:-1])**2.0)

def system_equations(vars): # поиск корней
    x, y = vars
    return [x**2 + y - 2, x - y]

def benchmark_optimization(): # Тестирование методов оптимизации
    methods = ['BFGS', 'CG', 'Nelder-Mead', 'Powell']
    results = {}
    
    for method in methods:
        start_time = time.time()
        result = scipy.optimize.minimize(
            rosenbrock,
            x0=np.random.random(10) * 2,  # Векторизованная генерация начальной точки
            method=method
        )
        end_time = time.time()
        
        results[method] = {
            'time': end_time - start_time,
            'iterations': result.nit,
            'success': result.success,
            'minimum': result.fun
        }
    
    return results

# Оптимизация
print("Результаты оптимизации Розенброка:")
opt_results = benchmark_optimization()
for method, res in opt_results.items():
    print(f"{method}: время={res['time']:.3f}c, итерации={res['iterations']}, успех={res['success']}")

# Поиск корней системы уравнений 
root_result = scipy.optimize.root(system_equations, [0, 0])
print(f"\nКорни системы уравнений: {root_result.x}")

# Линейное программирование 
c = np.array([-1, -2])
A_ub = np.array([[1, 1], [-1, 2], [2, 1]], dtype=np.float32) 
b_ub = np.array([6, 2, 8], dtype=np.float32)
bounds = [(0, None), (0, None)]

lp_result = scipy.optimize.linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds)
print(f"\nЛинейное программирование: успех={lp_result.success}, x={lp_result.x}, значение={lp_result.fun}")


# Генерация тестового сигнала 
np.random.seed(42)
fs = 1000
t = np.arange(0, 1, 1/fs)  # Векторизованное создание временной оси
signal_freqs = [50, 120, 300]
clean_signal = np.sum([np.sin(2 * np.pi * f * t) for f in signal_freqs], axis=0)

# Добавление шума 
noise = 0.5 * np.random.randn(len(t))
anomalies = np.zeros_like(t)
anomaly_indices = np.random.choice(len(t), 20, replace=False)
anomalies[anomaly_indices] = 3 * np.random.randn(20)

noisy_signal = clean_signal + noise + anomalies
noisy_signal = noisy_signal.astype(np.float32)  

# Фурье-анализ
fft_values = scipy.fft.fft(noisy_signal)
frequencies = scipy.fft.fftfreq(len(noisy_signal), 1/fs)

# Фильтрация сигнала 
sos = scipy.signal.butter(4, [40, 350], 'bandpass', fs=fs, output='sos')
filtered_signal = scipy.signal.sosfilt(sos, noisy_signal)


# Визуализация
plt.figure(figsize=(10, 6))

# Сравнение  сигналов 
plt.plot(t[:200], clean_signal[:200], 'b', linewidth=2, label='Чистый сигнал')
plt.plot(t[:200], noisy_signal[:200], 'r', alpha=0.6, label='Зашумленный сигнал')
plt.plot(t[:200], filtered_signal[:200], 'g', linewidth=1.5, label='Отфильтрованный сигнал')

plt.xlabel('Время (с)', fontsize=12)
plt.ylabel('Амплитуда', fontsize=12)
plt.title('Сравнение сигналов до и после фильтрации', fontsize=14, fontweight='bold')
plt.legend(fontsize=11, loc='upper right')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()