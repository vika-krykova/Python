def main():
    # Цикл, пока не введется корректное число + обработка исключений 
    while True:
        try:
            N = int(input("Введите целое число больше 0: "))
            if N > 0:
                break
            else:
                print("Ошибка: число должно быть больше 0!")
        except ValueError:
            print("Ошибка: введите целое число!")
     # Список, хранить делители + их перебор и добавление в список
    divisors = []
    for i in range(1, N + 1):
        if N % i == 0:
            divisors.append(i)
    print(f"Делители числа {N}: {divisors}")
    # Проверка, простое ли число: кроме 1, должно быть 2 делителя
    if N == 1:
         print("Число 1 не является ни простым, ни составным")
    elif len(divisors) == 2:
         print(f"Число {N} является простым")
    else:
        print(f"Число {N} не является простым")
     # Проверка, совершенное ли число
    divisors_sum = 0
    for divisor in divisors:
        if divisor != N:  
            divisors_sum += divisor
    
    if divisors_sum == N:
        print(f"Число {N} является совершенным ({'+'.join(str(d) for d in divisors if d != N)}={N})")
    else:
        print(f"Число {N} не является совершенным")

if __name__ == "__main__":
    main()