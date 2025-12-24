import json
from functools import reduce
from collections import Counter
import os

def create_data_files(): # Создание JSON файлы
    countries_list = [ # countries.json
        "Afghanistan", 
        "Albania", 
        "Algeria", 
        "Andorra", 
        "Angola",
        "Antigua and Barbuda", 
        "Argentina", "Armenia", 
        "Australia", "Austria",
        "Finland", 
        "Sweden", 
        "Denmark", 
        "Norway", 
        "Iceland",
        "England", 
        "Ireland", 
        "Poland", 
        "Switzerland", 
        "Thailand",
        "Estonia", 
        "Ethiopia", 
        "Pakistan", 
        "India", 
        "China" 
    ]
    
    countries_detailed = [ # countries-data.json
        {
            "name": "Afghanistan",
            "capital": "Kabul",
            "languages": ["Pashto", "Uzbek", "Turkmen"],
            "population": 27657145
        },
        {
            "name": "Albania",
            "capital": "Tirana",
            "languages": ["Albanian"],
            "population": 2886026
        },
        {
            "name": "Algeria",
            "capital": "Algiers",
            "languages": ["Arabic"],
            "population": 40400000
        },
        {
            "name": "Finland",
            "capital": "Helsinki",
            "languages": ["Finnish", "Swedish"],
            "population": 5530719
        },
        {
            "name": "Sweden",
            "capital": "Stockholm",
            "languages": ["Swedish"],
            "population": 10353442
        },
        {
            "name": "China",
            "capital": "Beijing",
            "languages": ["Chinese"],
            "population": 1402112000
        },
        {
            "name": "India",
            "capital": "New Delhi",
            "languages": ["Hindi", "English"],
            "population": 1380004385
        },
        {
            "name": "USA",
            "capital": "Washington D.C.",
            "languages": ["English"],
            "population": 331002651
        },
        {
            "name": "Russia",
            "capital": "Moscow",
            "languages": ["Russian"],
            "population": 145912025
        },
        {
            "name": "Brazil",
            "capital": "Brasília",
            "languages": ["Portuguese"],
            "population": 212559417
        },
        {
            "name": "Mexico",
            "capital": "Mexico City",
            "languages": ["Spanish"],
            "population": 128932753
        },
        {
            "name": "Japan",
            "capital": "Tokyo",
            "languages": ["Japanese"],
            "population": 126476461
        },
        {
            "name": "Germany",
            "capital": "Berlin",
            "languages": ["German"],
            "population": 83783942
        },
        {
            "name": "France",
            "capital": "Paris",
            "languages": ["French"],
            "population": 65273511
        },
        {
            "name": "Italy",
            "capital": "Rome",
            "languages": ["Italian"],
            "population": 60461826
        }
    ]
    
    with open('countries.json', 'w', encoding='utf-8') as f: # Сохранение в файлы
        json.dump(countries_list, f, ensure_ascii=False, indent=2)
    
    with open('countries-data.json', 'w', encoding='utf-8') as f:
        json.dump(countries_detailed, f, ensure_ascii=False, indent=2)
    
    # print("Файлы с данными созданы")

# задачи с map
def convert_to_uppercase(countries): # названия стран к верхнему регистру
    return list(map(lambda c: c.upper(), countries))

def filter_countries(countries): # фильтрация по критериям
    results = {
        'land': list(filter(lambda c: 'land' in c.lower(), countries)),
        'six_chars': list(filter(lambda c: len(c) == 6, countries)),
        'six_plus': list(filter(lambda c: len(c) >= 6, countries)),
        'starts_e': list(filter(lambda c: c.lower().startswith('e'), countries))
    }
    return results

def format_nordic_countries(countries): # страны Северной Европы
    nordic = ['Finland', 'Sweden', 'Denmark', 'Norway', 'Iceland']
    nordic_in_list = [c for c in nordic if c in countries]
    
    if len(nordic_in_list) >= 2:
        result = reduce(lambda x, y: f"{x}, {y}", nordic_in_list[:-1])
        return f"{result} и {nordic_in_list[-1]} это страны Северной Европы"
    elif nordic_in_list:
        return f"{nordic_in_list[0]} это страны Северной Европы"
    else:
        return "Стран Северной Европы нет в списке"

# задачи без map
def get_uppercase_imperative(countries): # верхний регистр
    result = []
    for country in countries:
        result.append(country.upper())
    return result

def filter_by_substring_imperative(countries, substring): # подстрока land
    result = []
    for country in countries:
        if substring in country.lower():
            result.append(country)
    return result

def filter_by_length_imperative(countries, length): # Фильтрация по длине 6 символов
    result = []
    for country in countries:
        if len(country) == length:
            result.append(country)
    return result

def filter_by_min_length_imperative(countries, min_length): # Фильтрация по длине 6 и больше символов
    result = []
    for country in countries:
        if len(country) >= min_length:
            result.append(country)
    return result

def filter_by_starting_letter_imperative(countries, letter): # начальная буква Е
    result = []
    for country in countries:
        if country.lower().startswith(letter.lower()):
            result.append(country)
    return result

def format_nordic_countries_imperative(countries): # Северная Европа
    nordic = ['Finland', 'Sweden', 'Denmark', 'Norway', 'Iceland']

    nordic_in_list = [] # поиск стран Северной Европы
    for country in countries:
        if country in nordic:
            nordic_in_list.append(country)
    
    if not nordic_in_list:
        return "Стран Северной Европы нет в списке"
    
    if len(nordic_in_list) == 1:
        return f"{nordic_in_list[0]} это страны Северной Европы"
    
    result = nordic_in_list[0] # объединение
    for i in range(1, len(nordic_in_list) - 1):
        result += f", {nordic_in_list[i]}"
    
    result += f" и {nordic_in_list[-1]} - это страны Северной Европы"
    return result

# каррирование
categorize_countries = lambda pattern: lambda countries: [
   c for c in countries if pattern.lower() in c.lower()
]

# замыкания
def create_country_filter(pattern): 
    def filter_function(countries):
        return [c for c in countries if pattern.lower() in c.lower()]
    return filter_function

# анализ данных 
def analyze_detailed_countries(data): 
    if not data:
        return {}
    
    # Сортировка стран
    sorted_by_name = sorted(data, key=lambda x: x['name'])
    sorted_by_capital = sorted(data, key=lambda x: x['capital'])
    sorted_by_population = sorted(data, key=lambda x: x['population'], reverse=True)
    
    # 10 самых распространенных языков
    all_languages = [lang for country in data for lang in country['languages']]
    top_10_languages = Counter(all_languages).most_common(10)
    
    # Страны для каждого языка (10 )
    countries_by_language = {}
    for lang, _ in top_10_languages:
        countries_for_lang = [
            country['name'] 
            for country in data 
            if lang in country['languages']
        ]
        countries_by_language[lang] = countries_for_lang
    
    # 10 самых населенных стран
    top_10_populated = [(c['name'], c['population']) for c in sorted_by_population[:10]]
    
    return {
        'sorted_by_name': sorted_by_name,
        'sorted_by_capital': sorted_by_capital,
        'sorted_by_population': sorted_by_population,
        'top_10_languages': top_10_languages,
        'countries_by_language': countries_by_language,
        'top_10_populated': top_10_populated
    }

def main():
    print("-" * 30)
    print("Страны в функциональном стиле")
    print("-" * 30)
    
    try:
        with open('countries.json', 'r', encoding='utf-8') as f:
            countries = json.load(f)
        print(f"   Загружено {len(countries)} стран из countries.json")
    except:
        print("   Ошибка загрузки countries.json")
        return
    
    try:
        with open('countries-data.json', 'r', encoding='utf-8') as f:
            detailed_countries = json.load(f)
        print(f"   Загружено {len(detailed_countries)} стран из countries-data.json")
    except:
        print("   Ошибка загрузки countries-data.json")
        detailed_countries = []
    
    # map
    print("\n" + "-" * 30)
    print("Map - страны в верхнем регистре")
    print("-" * 30)
    uppercase_countries = convert_to_uppercase(countries)
    print(f"Первые 5: {uppercase_countries[:5]}")
    
    # filter
    print("\n" + "-" * 30)
    print("Фильтрация стран")
    print("-" * 30)
    filtered_results = filter_countries(countries)
    print(f"Содержат 'land': {filtered_results['land']}")
    print(f"Ровно 6 символов: {filtered_results['six_chars']}")
    print(f"6+ символов: {len(filtered_results['six_plus'])} стран")
    print(f"Начинаются с 'E': {filtered_results['starts_e']}")
    
    # reduce
    print("\n" + "-" * 30)
    print("Страны Северной Европы")
    print("-" * 30)
    nordic_string = format_nordic_countries(countries)
    print(nordic_string)
    
    # без map/filter/reduce
    print("\n" + "-" * 30)
    print("Без map/filter/reduce")
    print("-" * 30)
    
    # Верхний регистр без map
    uppercase_imperative = get_uppercase_imperative(countries)
    print(f"Верхний регистр: {uppercase_imperative[:3]}")
    
    # Фильтрация без filter
    print("\nФильтрация (без filter):")
    print(f"   а) С 'land': {filter_by_substring_imperative(countries, 'land')}")
    print(f"   б) 6 символов: {filter_by_length_imperative(countries, 6)}")
    print(f"   в) 6+ символов: {len(filter_by_min_length_imperative(countries, 6))} стран")
    print(f"   г) Начинаются с 'E': {filter_by_starting_letter_imperative(countries, 'e')}")
    
    # Объединение без reduce
    print(f"\nОбъединение стран Северной Европы (без reduce):")
    nordic_imperative = format_nordic_countries_imperative(countries)
    print(f"   {nordic_imperative}")
    
    # каррирование (полное для всех шаблонов)
    print("\n" + "-" * 30)
    print("Каррирование")
    print("-" * 30)
    print("Использование каррирования:")
    print(f"1. 'land': {categorize_countries('land')(countries)}")
    print(f"2. 'ia': {categorize_countries('ia')(countries)}")
    print(f"3. 'island': {categorize_countries('island')(countries)}")
    print(f"4. 'stan': {categorize_countries('stan')(countries)}")
    
    # замыкания 
    print("\n" + "-" * 30)
    print("Замыкания")
    print("-" * 30)
    print("Использование замыканий :")
    print(f"1. 'land': {create_country_filter('land')(countries)}")
    print(f"2. 'ia': {create_country_filter('ia')(countries)}")
    print(f"3. 'island': {create_country_filter('island')(countries)}")
    print(f"4. 'stan': {create_country_filter('stan')(countries)}")
    
    # анализ расширенных данных (полное выполнение задания 8)
    print("\n" + "-" * 30)
    print("Aнализ countries-data.json")
    print("-" * 30)
    
    if detailed_countries:
        analysis_results = analyze_detailed_countries(detailed_countries)
        
        # Сортировка стран по названию, столице и населению
        print("\nСортировка стран:")
        
        print("\n   а) По названию (5):")
        for country in analysis_results['sorted_by_name'][:5]:
            print(f"      • {country['name']}")
        
        print("\n   б) По столице (5):")
        for country in analysis_results['sorted_by_capital'][:5]:
            print(f"      • {country['capital']} ({country['name']})")
        
        print("\n   в) По населению (первые 5 по убыванию):")
        for i, country in enumerate(analysis_results['sorted_by_population'][:5], 1):
            print(f"      {i}. {country['name']}: {country['population']:,}")
        
        #  10 самых распространенных языков и стран, где на них говорят
        print("\n10 самых распространенных языков и стран, где на них говорят:")
        for i, (language, count) in enumerate(analysis_results['top_10_languages'], 1):
            countries_for_language = analysis_results['countries_by_language'].get(language, [])
            print(f"\n   {i}. {language} - {count}:")
            print(f"      Страны: {', '.join(countries_for_language)}")
        
        #  10 самых населенных стран
        print("\n10 самых населенных стран:")
        for i, (country_name, population) in enumerate(analysis_results['top_10_populated'], 1):
            # поиск страны в данных для получения дополнительной информации
            country_info = next(
                (c for c in detailed_countries if c['name'] == country_name), 
                None
            )
            if country_info:
                languages = ', '.join(country_info['languages'])
                print(f"   {i:2}. {country_name:15} - {population:>15,}")
                print(f"        Столица: {country_info['capital']}, Языки: {languages}")
            else:
                print(f"   {i:2}. {country_name:15} - {population:>15,}")
        
    else:
        print("Нет данных")

if __name__ == "__main__":
    main()