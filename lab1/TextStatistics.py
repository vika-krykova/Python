import string
from collections import Counter

# Удаление пунктуации и приведение к нижнему регистру
def clean_text(text):
    text = text.lower()  # к нижнему регистру
    for char in string.punctuation + "«»—–…":
        text = text.replace(char, "")
    return text

# Запрос текста от пользователя
def get_text():
    while True:
        text = input("Введите текст для анализа (не менее 100 символов):\n> ")
        if len(text) >= 100:
            return text
        else:
            print("Текст слишком короткий. Попробуйте ещё раз.\n")

# Основная функция анализа
def analyze_text(text):
    cleaned = clean_text(text)

    total_chars = len(text)
    chars_no_spaces = len(text.replace(" ", ""))

    words = cleaned.split()
    word_count = len(words)

    # Подсчёт частоты слов
    word_freq = Counter(words)

    # 5 самых частых слов
    most_common = word_freq.most_common(5)

    # 5 самых длинных слов (уникальные, сортировка по длине)
    unique_words = list(set(words))
    longest_words = sorted(unique_words, key=len, reverse=True)[:5]

    # Средняя длина слова
    total_word_length = sum(len(word) for word in words)
    avg_word_length = total_word_length / word_count if word_count > 0 else 0

    # Вывод результатов
    print("\nРезультаты анализа:")
    print(f"Общее количество символов: {total_chars} (без пробелов: {chars_no_spaces})")
    print(f"Количество словоформ: {word_count}")
    print("Самые частые словоформы:")
    for word, count in most_common:
        print(f"- '{word}': {count} раз(а)")
    print("Самые длинные словоформы:")
    for word in longest_words:
        print(f"- '{word}' ({len(word)} букв)")
    print(f"Средняя длина словоформы: {round(avg_word_length, 1)} символа")

# Запуск
text = get_text()
analyze_text(text)