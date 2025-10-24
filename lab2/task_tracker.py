import json
import os

class Task: # хранит инф-ю об 1й задаче
    def __init__(self, description, category):
        self.description = description # текст задачи
        self.category = category # категория
        self.is_completed = False # статус выполнения
    
    def __str__(self): # красиво показывает
        status = "✓" if self.is_completed else " "
        return f"- [{status}] {self.description} #{self.category}" # статус выпол-я
    
    def __repr__(self): # техническое представление
        return f"Task('{self.description}', '{self.category}')"
    
    def to_dict(self): # Превращение задачи в словарь для сохранения в JSON 
        return {
            "description": self.description,
            "category": self.category,
            "is_completed": self.is_completed
        }
    
    @classmethod #  Создатние объекта Task из словаря с данными
    def from_dict(cls, data):
        task = cls(data["description"], data["category"]) # создание задачи, берет описание и катег-ю из словаря
        task.is_completed = data["is_completed"] # восстановление статуса выполнения
        return task

class TaskTracker: # Управляет всей коллекцией задач + сохраняет/загружает из файла
    def __init__(self, filename="tasks.json"): # конструктор
        self._filename = filename  # Защищенный, хранит имя файла 
        self._tasks = [] # Защищенный, список задач
        self._load_tasks() # автозагрузка
    
    def _load_tasks(self): # Достать сохраненные задачи из JSON, превратить их в объекты Python
        try:
            if os.path.exists(self._filename): # проверка существования файла
                with open(self._filename, 'r', encoding='utf-8') as file: # чтение и преобразование данных
                    data = json.load(file)
                    self._tasks = [Task.from_dict(task_data) for task_data in data]
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            self._tasks = []
    
    def _save_tasks(self): # сохранить в json задачи
        try:
            with open(self._filename, 'w', encoding='utf-8') as file:
                tasks_data = [task.to_dict() for task in self._tasks] #  Преобразование задач в словари
                json.dump(tasks_data, file, ensure_ascii=False, indent=2) # Сохранение в JSON 
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def add_task(self, description, category): # добавить новую задачу
        if not description or not description.strip(): # валидация
            print("Описание пустое, добавьте описание")
            return False
        
        task = Task(description.strip(), category.strip().lower()) # Создание задачи
        self._tasks.append(task) # добавление в список
        self._save_tasks() # автосохранение
        print("Задача успешно добавлена")
        return True
    
    def complete_task(self, task_index): # Отметить задачу как выполненную по её номеру в списке
        try:
            if 1 <= task_index <= len(self._tasks): # проверка номера на корректность
                task = self._tasks[task_index - 1]
                task.is_completed = True # отметка выполнения
                self._save_tasks()
                print("Задача выполнена")
                return True
            else:
                print("Неверный номер задачи")
                return False
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
    
    def show_all_tasks(self): # показ всех задач
        if not self._tasks:
            print("Список задач пуст")
            return
        
        for i, task in enumerate(self._tasks, 1):
            print(f"{i}. {task}")
    
    def show_tasks_by_category(self, category): # показать задачи определенной категории
        filtered = []
        for task in self._tasks:
            if task.category == category.lower(): # проверка: совпалает ли текущая задача с нужной категорией
                filtered.append(task) # если совпала, добавить в список
    
        if filtered: # вывод
            for task in filtered:
                print(task)
        else:
            print(f"В категории '{category}' нет задач")

def main():
    tracker = TaskTracker()  # Создание трекера
    
    print("Таск-трекер готов к работе")
    print("-" * 20)    
    
    while True:
        print("1. Показать все задачи")
        print("2. Добавить задачу")
        print("3. Отметить задачу выполненной")
        print("4. Показать задачи по категории")
        print("5. Выход")
        print("-" * 20)   
        
        choice = input("Выберите действие (1-6): ").strip()
        
        if choice == "1":
            tracker.show_all_tasks()
            
        elif choice == "2":
            description = input("Введите описание задачи: ").strip()
            category = input("Введите категорию: ").strip()
            tracker.add_task(description, category)
            
        elif choice == "3":
            tracker.show_all_tasks()
            if tracker._tasks:
                try:
                    task_num = input("Введите номер задачи: ").strip()
                    if task_num.isdigit():
                        tracker.complete_task(int(task_num))
                    else:
                        print("Введите число")
                except ValueError:
                    print("Ошибка ввода")
                    
        elif choice == "4":
            category = input("Введите категорию: ").strip()
            tracker.show_tasks_by_category(category)
            
        elif choice == "5":
            print("Пока!!")
            break
            
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()
