import random

words = ['стол','крона','ветер', 'рамка','парта','метро', 'волна','лидер','гость', 'снег', 'река', 'нота', 'книга', 'цвет', 'дверь']

choice_word = random.choice(words)

print("Загадано слово из 5 букв. У вас есть 6 попыток отгадать его.")

def give_feedback(player_word, choice_word): #генерация подсказок, функция сравнивает два слова + осуществляет возврат подсказки
    feedback = [''] * 5 # список под каждую букву: 5 строк, будет храниться результат по каждой букве
    choice_checked = [False] * 5  # Чтобы не использовать одну букву дважды, отмечачать использованные буквы
    player_checked = [False] * 5 #  для отметки проверенных букв в слове игрока

    # Шаг 1: отметить правильно угаданные буквы (на своих местах)
    for i in range(5):
        if player_word[i] == choice_word[i]:
            feedback[i] = f"[{player_word[i]}]"
            choice_checked[i] = True #буква уже учтена => не использовать снова
            player_checked[i] = True

    # Шаг 2: отметить буквы, которые есть в слове, но на других местах
    for i in range(5):
        if not player_checked[i]: #проверка неотмеченных букв
            for j in range(5):
                if not choice_checked[j] and player_word[i] == choice_word[j]:
                    feedback[i] = f"({player_word[i]})"
                    choice_checked[j] = True
                    player_checked[i] = True
                    break

    # Шаг 3: для оставшихся букв - вывести их без изменений
    for i in range(5):
        if not feedback[i]: # если буква не была обработана
            feedback[i] = player_word[i]  # ИСПРАВЛЕНИЕ: player_word[i], а не choice_word[i]

    return ' '.join(feedback) # подсказка: буквы через пробел

for attempt in range(1, 7): # цикл из 6 попыток пользователя
    player_word = input(f"Попытка {attempt}: ").lower() # ввод пользователя + перевод в маленькие буквы

    # проверка, точно ли ввели 5 букв, уведомление, если нет + переход к след. попытке
    if len(player_word) != 5:
        print("Введите слово из 5 букв.")
        continue
    if player_word not in words: # если такого слова нет в списке, уведомить
        print("Слово не походит")
        continue

    result = give_feedback(player_word, choice_word) # получение подсказки + отображение результата
    print("Результат:", result)

    if player_word == choice_word: # если слово угадали
        print(f'Вы угадали слово "{choice_word}" за {attempt} попыток!')
        break
else: # если не угадали
    print(f'Вы не угадали, слово: "{choice_word}".')