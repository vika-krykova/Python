import json
import os

class Transaction: # Класс для представления операции (описание, сумма, категория)
    def __init__(self, description, amount, transaction_type, category): # конструктор класса с атрибутами защищенными
        self._description = description
        self._amount = amount
        self._transaction_type = transaction_type
        self._category = category
    
    def __str__(self): # магический метод для пользователей  
        sign = "+" if self._transaction_type == "доход" else "-"
        return f"{sign}{self._amount} руб. - {self._description} ({self._category})"
    
    def __repr__(self):
        return f"Transaction('{self._description}', {self._amount}, '{self._transaction_type}', '{self._category}')"


class BudgetTracker: # магический метод для официального представления
    def __init__(self, filename="budget.json"):
        self.__filename = filename
        self.__transactions = []
        self.__balance = 0.0
        self.__load_data()
    
    def __load_data(self): # private метод для загрузки данных из файла при запуске программы
        try:
            if os.path.exists(self.__filename): # существует ли файл
                with open(self.__filename, 'r', encoding='utf-8') as file: # открывает, читает и закрывает файл
                    data = json.load(file) # преобразует JSON в словарь Python
                
                self.__transactions = [] # очистка старых данных
                for transaction_data in data.get('transactions', []): # создание объектов Transaction из данных
                    transaction = Transaction(
                        transaction_data['description'],
                        transaction_data['amount'],
                        transaction_data['type'],
                        transaction_data['category']
                    )
                    self.__transactions.append(transaction)
                
                self.__balance = data.get('balance', 0.0) # берем баланс из данных/ 0.0- если нет
                print("Данные загружены")
                
        except Exception as e: # отлавливание любой ошибки
            print(f"Ошибка при загрузке данных: {e}")
            self.__transactions = []
            self.__balance = 0.0 # значения по умолчанию пустые 
    
    def __save_data(self): # private метод
        try:
            data = { # создание словаря
                'transactions': [ # список всех операций
                    { # создание словарей для каждого t 
                        'description': t._description,
                        'amount': t._amount,
                        'type': t._transaction_type,
                        'category': t._category
                    }
                    for t in self.__transactions # перебор объектов t 
                ],
                'balance': self.__balance # текущий баланс
            }
            
            with open(self.__filename, 'w', encoding='utf-8') as file: # преобразование в JSON и запись в файл
                json.dump(data, file, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")
    
    def add_transaction(self): # начало и заголовок
        print("\n--- Добавление новой операции ---")
        
        while True:
            description = input("Описание операции: ").strip() # ввод, проверка описания
            if description and description.strip():
                break
            print("Описание не может быть пустым")
        
        while True:
            try: # ввод и проверка суммы
                amount = float(input("Сумма: ").strip())
                if amount <= 0:
                    print("Сумма должна быть положительной")
                    continue
                break
            except ValueError:
                print("Введите корректное число")
            
        while True:    
            print("Тип операции: 1 - Доход, 2 - Расход") # ввод типа операции
            type_choice = input("Ваш выбор: ").strip()
            if type_choice == "1":
                transaction_type = "доход"
                break
            elif type_choice == "2":
                transaction_type = "расход"
                break
            else:
                print("Выберите 1 или 2")
            
        while True:
            category = input("Категория: ").strip() # ввод и проверка категории
            if category and category.strip():  # ИСПРАВЛЕНО: убрано "not"
                break
            print("Категория не может быть пустой")
                
            
        transaction = Transaction(description, amount, transaction_type, category) # создание, добавление транзакции
        self.__transactions.append(transaction)
            
        if transaction_type == "доход": # обновление баланса
            self.__balance += amount
        else:
            self.__balance -= amount
            
        self.__save_data()
        print("Операция добавлена")
    
    def show_balance(self): # показывает баланс
        print(f"\n--- Текущий баланс ---")
        print(f"Баланс: {self.__balance:.2f} руб.")
        
        if self.__transactions:
            print("\nПоследние операции:")
            for transaction in self.__transactions[-3:]:
                print(f"  {transaction}")
        else:
            print("Операций пока нет.")

    def show_menu(self):
        while True:
            print("\n" + "-"*40)
            print("          Трекер бюджета")
            print("-"*40)
            print("1 - Добавить операцию")
            print("2 - Показать баланс")
            print("3 - Выход")
            print("-"*40)
            
            choice = input("Выберите действие: ").strip()
            
            if choice == "1":
                self.add_transaction()
            elif choice == "2":
                self.show_balance()
            elif choice == "3":
                print("До свидания! Данные сохранены.")
                break
            else:
                print("Пожалуйста, выберите 1, 2, 3.")
  

if __name__ == "__main__":
    tracker = BudgetTracker()
    tracker.show_menu()