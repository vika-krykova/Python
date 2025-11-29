from abc import ABC, abstractmethod

class Vehicle(ABC): # абстрактный базовый класс Vehicle
    @abstractmethod # делает метод абстрактным
    def get_max_speed(self): # макс. скорость
        pass # заглушка - метод не имеет реализации
    
    @abstractmethod
    def get_vehicle_type(self): # тип транспортного сред-ва
        pass
    
    def __str__(self):
        return f"{self.get_vehicle_type()}"
    
    def __repr__(self):
        return f"{self.__class__.__name__}()"


class RoadVehicle(Vehicle): # абстрактный подкласс, добавляет абстр. метод
    @abstractmethod
    def get_engine_type(self):
        pass


class Car(RoadVehicle): # наследуется от абст. класса RoadVehicle, наследует методы от Vehocle и RoadVehicle
    def __init__(self, car_type, engine_type):

        if not car_type or not isinstance(car_type, str): # обр. ошибок car_type
            raise ValueError("Тип автомобиля не может быть пустым")
        if not car_type.strip():
            raise ValueError("Тип автомобиля не может быть пробелами")
        
        if not engine_type or not isinstance(engine_type, str): # обр. ошибок engine_type
            raise ValueError("Тип двигателя быть пустым")
        if not engine_type.strip():
            raise ValueError("Тип двигателя не может быть пробелами")

        self._car_type = car_type
        self._engine_type = engine_type
    
    def get_max_speed(self): # реализация абст.метода get_max_speed 
        return 200
    
    def get_vehicle_type(self): # реализация абст.метода get_vehicle_type
        return "Автомобиль"
    
    def get_engine_type(self): # реализация абст.метода get_engine_type
        return self._engine_type
    
    def __str__(self):
        return f"Автомобиль ({self._car_type}, {self._engine_type})"
    
    def __repr__(self):
        return f"Car('{self._car_type}', '{self._engine_type}')"


class Bicycle(RoadVehicle): # наследуется от абст. класса RoadVehicle, наследует методы от Vehocle и RoadVehicle
    def __init__(self, bicycle_type):

        if not bicycle_type or not isinstance(bicycle_type, str):  # об. ошибок bicycle_type
            raise ValueError("Тип велосипеда не может быть пустым")
        if not bicycle_type.strip():
            raise ValueError("Тип велосипеда не может быть пробелами")

        self._bicycle_type = bicycle_type
    
    def get_max_speed(self):
        return 30
    
    def get_vehicle_type(self):
        return "Велосипед"
    
    def get_engine_type(self):
        return "мускульная сила"
    
    def __str__(self):
        return f"Велосипед ({self._bicycle_type})"
    
    def __repr__(self):
        return f"Bicycle('{self._bicycle_type}')"


if __name__ == "__main__":
    car = Car("седан", "электрический")
    print(car.get_vehicle_type())  
    print(car.get_engine_type())   

    print("-"*40)
    
    bicycle = Bicycle("городской")
    print(bicycle.get_vehicle_type())  
    print(bicycle.get_engine_type())  