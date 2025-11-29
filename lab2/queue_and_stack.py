class Queue: # FIFO
    def __init__(self): # создание новой очереди
        self._items = []
    
    def enqueue(self, item): # добавление в очередь
        self._items.append(item)
        print(f"+ {item}")
    
    def dequeue(self): # удаление из очереди
        if not self._items:
            print("Очередь пуста")
            return None
        item = self._items.pop(0) # удаляет и возвращает 1й элемент
        print(f"- {item}")
        return item
     
    def peek(self): # просмотр 1го элемента, очередь остается
        if not self._items:
            print("Очередь пуста")
            return None
        return self._items[0]
    
    def __str__(self):
        return f"Queue({self._items})"
    
    def __repr__(self):
        return f"Queue({self._items})"


class Stack: # LIFO
    def __init__(self):
        self.__items = []
    
    def push(self, item):  # добавление элемента в конец списка
        self.__items.append(item)
        print(f"+ {item}")
    
    def pop(self):  # удаляет и возвращает последний элемент
        if not self.__items:
            print("Стек пуст")
            return None
        item = self.__items.pop()
        print(f"- {item}")
        return item
    
    def peek(self):  # просмотр последнего элемента, очередь остается
        if not self.__items:
            print("Стек пуст")
            return None
        return self.__items[-1]
    
    def __str__(self):
        return f"Stack({self.__items})"
    
    def __repr__(self):
        return f"Stack({self.__items})"
    
    
if __name__ == "__main__":
    print("--- Очередь ---")
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.dequeue()
        
    print("\n --- Стек ---")
    s = Stack()
    s.push(1)
    s.push(2)
    s.pop()