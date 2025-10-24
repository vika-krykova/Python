import random

def generate_number(length): # функция с длиной числа
    numbers = list('0123456789') 
    random.shuffle(numbers)
    return ''.join(numbers[:length]) # берет цифры и перемешивает

def count_cows_and_bulls(choice_number, player_number): # подсчет коров и быков
    cows = 0
    bulls = 0
    for i in range(len(choice_number)): # цикл по индексам цифр 
        if player_number[i] == choice_number[i]: # корова - цифра на позиции совпадает
            cows += 1
        elif player_number[i] in choice_number: # бык - цифра есть на другой позиции 
            bulls += 1
    return cows, bulls

def valid_player(player_number, length): # проверка верности варианта от пользователя
    return (
        player_number.isdigit() and # состоит из цифр
        len(player_number) == length and # введенная длина = длина загаданного числа
        len(set(player_number)) == length # цифры не повторяются
    )

def ask_length(): # выбор длины числа
    while True:
        length = input("Выберите длину числа (3, 4 или 5): ")
        if length in ['3', '4', '5']:
            return int(length)
        else:
            print("Введите 3, 4 или 5.")

def play_game(length): # запуск игры
    choice_number = generate_number(length) # загадывание числа
    attempts = 0 # попытки

    print(f"Загадано число из {length} уникальных цифр.")

    while True:
        player_number = input("Ваш вариант: ")
        if not valid_player(player_number, length): # правильно ли пользователь ввел
            print(f"Введите {length} уникальных цифр.")
            continue # если неверно=> новая итерация

        attempts += 1
        cows, bulls = count_cows_and_bulls(choice_number, player_number)

        if cows == length:
            print(f"Вы угадали число {choice_number} за {attempts} попыток.")
            return attempts
        else:
            print(f"Найдено {cows} коров и {bulls} быков.")

def play_session(): # статистика + несколько игр
    games_played = 0
    attempts_list = [] # список попыток в каждой игре

    while True:
        length = ask_length()
        attempts = play_game(length)
        games_played += 1
        attempts_list.append(attempts)

        again = input("Хотите сыграть еще? (да/нет): ").strip().lower()
        if again != 'да':
            break

    print("\nСтатистика:")
    print(f"Всего игр сыграно: {games_played}")
    print(f"Лучший результат: {min(attempts_list)} попыток")
    print(f"Худший результат: {max(attempts_list)} попыток")
    avg = sum(attempts_list) / len(attempts_list)
    print(f"Средний результат: {round(avg, 1)} попыток")

play_session()