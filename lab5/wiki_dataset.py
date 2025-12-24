import requests 
import re 
import os
import json


SAVE_DIR = "/home/vika/Рабочий стол/MyPythonProjects/wikipedia_articles"


os.makedirs(SAVE_DIR, exist_ok=True)
print(f" Файлы будут сохранены в: {SAVE_DIR}\n")

WIKI_API_URL = "https://ru.wikipedia.org/w/api.php" 
PERIOD_TOPICS = [ 
    "Пермский период", 
    "Массовое пермское вымирание", 
    "Уфимский ярус", 
    "Палеозой", 
    "Герцинская складчатость", 
    "Силурийский период", 
    "Каменноугольный период", 
    "Казанский ярус", 
    "Биармийский отдел", 
    "Триасовый период" 
] 

# Получить статью из Википедии по заголовку
def get_wiki_article(title: str) -> str: 
    params = { 
        'action': 'query', 
        'format': 'json', 
        'titles': title, 
        'prop': 'extracts', 
        'explaintext': True, 
        'exsectionformat': 'plain' 
    } 
 
    headers = {'User-Agent': 'WikiBot/1.0'} 
 
    try: 
        response = requests.get(WIKI_API_URL, params=params, headers=headers, timeout=10) 
        response.raise_for_status() 
        data = response.json() 
 
        pages = data.get('query', {}).get('pages', {}) 
        for page_id, page_data in pages.items(): 
            if page_id != '-1': 
                return page_data.get('extract', '') 
        return '' 
    except Exception as e: 
        print(f" Ошибка '{title}': {e}") 
        return '' 
 
def clean_text(text: str) -> str:  # очистка текста 
    if not text:
        return ''
    text = re.sub(r'\s+', ' ', text) 
    text = re.sub(r'\n+', '\n', text) 
    return text.strip() 
 
def count_tokens(text: str) -> int: # подсчет токенов
    if not text:
        return 0
    return len(text) // 3  


def main(): 
    print("-" * 60)
    print("Загрузка статей из википедии")
    print("-" * 60)
    

    articles = []
    total_words = 0 
    total_chars = 0 
    total_tokens = 0 
 
    # Загрузка статей
    for topic in PERIOD_TOPICS: 
        print(f"\n Загружаем: {topic}") 
        content = get_wiki_article(topic) 
 
        if content: 
            cleaned_content = clean_text(content) 
            if cleaned_content: 
                words = len(cleaned_content.split()) 
                chars = len(cleaned_content) 
                tokens = count_tokens(cleaned_content)
                
                # Сохраняем в файл
                filename = os.path.join(SAVE_DIR, f"{topic.replace(' ', '_')}.txt")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                
                articles.append({
                    'title': topic,
                    'content': cleaned_content,
                    'words': words,
                    'chars': chars,
                    'tokens': tokens,
                    'filename': filename
                })
                
                total_words += words 
                total_chars += chars 
                total_tokens += tokens 
                
                print(f" Слов: {words}, Токенов: {tokens}")
                print(f" Файл: {os.path.basename(filename)}")
            else:
                print(f" Статья пуста после очистки")
        else: 
            print(f" Статья не найдена")
    
    # статистика
    print("\n" + "-" * 60) 
    print("Статистика") 
    print("-" * 60) 
    
    if articles:
        print(f"Количество статей: {len(articles)}") 
        print(f"Общее количество слов: {total_words}") 
        print(f"Общее количество символов: {total_chars}") 
        print(f"Общее количество токенов: {total_tokens}") 
        
        avg_words = total_words / len(articles) 
        avg_chars = total_chars / len(articles) 
        avg_tokens = total_tokens / len(articles) 
        
        print(f"\nСредние значения:") 
        print(f" Слов на статью: {avg_words:.0f}") 
        print(f" Символов на статью: {avg_chars:.0f}") 
        print(f" Токенов на статью: {avg_tokens:.0f}")
    else:
        print("Не загружены статьи")
    
    # требования
    print("\n" + "-" * 60)
    print("Проверка требований:")
    print("-" * 60)
    
    if articles:
        if total_words >= 10000: 
            print("Требование к объему (10 000 слов и больше) выполнено") 
        else: 
            print(f"Требование к объему Не выполнено: {total_words}/10000 слов")

        if len(articles) >= 5: 
            print("Требование к количеству статей (5 и более) выполнено") 
        else: 
            print(f"Требование к количеству статей Не выполнено: {len(articles)}/5")
    else:
        print("Требования не могут быть проверены: статьи не загружены")
    
    print("-" * 60)
    print(f"\nВсе файлы сохранены в: {SAVE_DIR}")
    
    # список файлов
    if os.path.exists(SAVE_DIR):
        print(f"\nСозданные файлы:")
        files = [f for f in os.listdir(SAVE_DIR) if f.endswith('.txt')]
        if files:
            for file in sorted(files):
                size = os.path.getsize(os.path.join(SAVE_DIR, file))
                print(f" {file} ({size:,} байт)")
        else:
            print("   (нет .txt файлов)")
    
    print("\n" + "-" * 60)
    print("Все ок")
    print("-" * 60)

if __name__ == "__main__": 
    main()
