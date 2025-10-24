import random


words = ['стол','крона','ветер', 'рамка','парта','метро', 'волна','лидер','гость', 'снег', 'река', 'нота', 'книга', 'цвет', 'дверь']

choice_word = random.choice(words)

print("Загадано слово из 5 букв. У вас есть 6 попыток отгадать его.")

def give_feedback(player_word, choice_word): # функция сравнивает два слова + осуществляет возврат подсказки
    feedback = [''] * 5 # список под каждую букву: 5 строк, будет храниться результат по каждой букве
    choice_checked = [False] * 5  # Чтобы не использовать одну букву дважды, отмечачать использованные буквы
    player_checked = [False] * 5

    for i in range(5):  # отметить правильно угаданные буквы, которые на своих местах
        if player_word[i] == choice_word[i]:
            feedback[i] = f"[{player_word[i]}]"
            choice_checked[i] = True #буква уже учтена => не использовать снова
            player_checked[i] = True

    for i in range(5): # поиск буквы, которая есть в слове не на своем месте
        if not player_checked[i]:
            for j in range(5): 
                if not choice_checked[j] and player_word[i] == choice_word[j]: # если буква есть на другом месте, то в круглые скобки
                    feedback[i] = f"({player_word[i]})"
                    choice_checked[j] = True
                    player_checked[i] = True
                    break

    for i in range(5): 
        if not feedback[i]: # буквы нет в загаданном слове/ не совпала
            feedback[i] = choice_word[i] # оставить букву без изменений

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