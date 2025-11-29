class Engine:
    def __init__(self, power, angle, speed, acceleration): # конструктор
        self._power = power
        self._angle = angle
        self._speed = speed
        self._acceleration = acceleration
    
    def __str__(self):
        return f"Двигатель: мощность = {self._power}, угол = {self._angle}"
    
    def __repr__(self):
        return f"Engine(power={self._power}, angle={self._angle})"
    
    def __eq__(self, other): # сравнение объектов по мощности - равны/ нет
        return self._power == other._power
    
    def __lt__(self, other): # сравнение объектов по мощности - какой объект с меньшей мощностью
        return self._power < other._power


class RotaryEngine(Engine):
    def __init__(self, power, torque, angle, speed, acceleration): # новый параметр-torque (вращающий момент)
        super().__init__(power, angle, speed, acceleration) # вызов конструктора-родителя
        self.__torque = torque
    
    def __str__(self):
        return f"Вращательный Двигатель: мощность = {self._power}, вращающий момент = {self.__torque}"
    
    def __repr__(self):
        return f"RotaryEngine(power={self._power}, torque={self.__torque})"


class SynchronousServodrive(RotaryEngine):
    def __init__(self, power, torque, precision, angle, speed, acceleration):  # новый параметр-precision (точность позиционирования)
        super().__init__(power, torque, angle, speed, acceleration) # вызов конструктора-родителя
        self.__precision = precision
    
    def set_angle(self, angle): # управление углом поворота
        self._angle = angle
    
    def __str__(self):
        return f"Синхронный Сервопривод: мощность = {self._power}, точность позиционирования = {self.__precision}"
    
    def __repr__(self):
        return f"SynchronousServodrive(power={self._power}, precision={self.__precision})"


class SixAxisManipulator:
    def __init__(self): # конструктор класса с параметрами: мощность, 
        self.__servos = [SynchronousServodrive(100, 5, 0.1, 0, 0, 0),
                        SynchronousServodrive(150, 8, 0.1, 0, 0, 0),
                        SynchronousServodrive(120, 6, 0.1, 0, 0, 0),
                        SynchronousServodrive(80, 3, 0.1, 0, 0, 0),
                        SynchronousServodrive(60, 2, 0.1, 0, 0, 0),
                        SynchronousServodrive(40, 1, 0.1, 0, 0, 0)]
        self.__position = [0, 0, 0] # начальная позиция 
    
    def __add__(self, move): # маг. метод для сложения векторов
        new_manip = SixAxisManipulator()
        new_manip.__position = [a + b for a, b in zip(self.__position, move)] # вычисление новой позиции
        return new_manip
    
    def __str__(self):
        return f"Манипулятор: позиция = {self.__position}"
    
    def __repr__(self):
        return f"SixAxisManipulator{self.__position}"


if __name__ == "__main__":
    print("--- Классы ---")
    
    # объекты
    engine = Engine(100, 45, 10, 2)
    rotational = RotaryEngine(150, 8.0, 30, 15, 3)
    servo = SynchronousServodrive(200, 10.0, 0.1, 90, 20, 5)
    
    print(engine)
    print(rotational)
    print(servo)
    
    print("\n--- Сравнение по мощности ---")
    servo1 = SynchronousServodrive(100, 5, 0.1, 0, 0, 0)
    servo2 = SynchronousServodrive(150, 5, 0.1, 0, 0, 0)
    
    print(f"servo1 == servo2: {servo1 == servo2}")
    print(f"servo1 < servo2: {servo1 < servo2}")
    
    print("\n--- Позиции манипулятора ---")
    manipulator = SixAxisManipulator()
    print(f"Начальная позиция: {manipulator}")
    
    # Перемещение
    new_manipulator = manipulator + [10, 5, -2]
    print(f"После перемещения: {new_manipulator}")