import random

choices = ['камень', 'ножницы', 'бумага', 'ящерица', 'спок']

# Правила побед
rules = {
    'ножницы':     ['бумага', 'ящерица'],
    'бумага':      ['камень', 'спок'],
    'камень':      ['ножницы', 'ящерица'],
    'ящерица':     ['спок', 'бумага'],
    'спок':        ['ножницы', 'камень']
}

win_phrases = {
    ('ножницы', 'бумага'): "Ножницы режут бумагу",
    ('бумага', 'камень'): "Бумага накрывает камень",
    ('камень', 'ящерица'): "Камень давит ящерицу",
    ('ящерица', 'спок'): "Ящерица травит Спока",
    ('спок', 'ножницы'): "Спок ломает ножницы",
    ('ножницы', 'ящерица'): "Ножницы убивают ящерицу",
    ('ящерица', 'бумага'): "Ящерица ест бумагу",
    ('бумага', 'спок'): "Бумага подставляет Спока",
    ('спок', 'камень'): "Спок испаряет камень",
    ('камень', 'ножницы'): "Камень затупляет ножницы"
}

def ask_target_score():
    while True:
        try:
            target = int(input("До скольки побед играем? "))
            if target > 0:
                return target
            else:
                print("Введите положительное число.")
        except ValueError:
            print("Введите число.")

def play_round():
    player = input("Ваш ход (камень/ножницы/бумага/ящерица/спок): ").lower()
    if player not in choices:
        print("Неверный ввод. Попробуйте еще раз.")
        return None, None

    computer = random.choice(choices)
    print(f"Ход компьютера: {computer}")

    if player == computer:
        print("Ничья!")
        return 0, 0

    if computer in rules[player]:
        phrase = win_phrases.get((player, computer), "")
        print(f"{phrase}! Вы победили!")
        return 1, 0
    else:
        phrase = win_phrases.get((computer, player), "")
        print(f"{phrase}! Компьютер победил :( )")
        return 0, 1

def play_game():
    target_score = ask_target_score()
    user_score = 0
    computer_score = 0

    while user_score < target_score and computer_score < target_score:
        print("\n--- Новый раунд ---")
        user_win, computer_win = play_round()
        
        if user_win is None:
            continue

        user_score += user_win
        computer_score += computer_win

        print(f"Счет: Вы - {user_score}, Компьютер - {computer_score}")

    if user_score == target_score:
        print("\n Вы выиграли матч!")
    else:
        print("\n Компьютер выиграл матч.")


play_game()