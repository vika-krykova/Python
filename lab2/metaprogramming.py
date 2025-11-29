class PluginRegistry(dict): # Реестр плагинов
    
    def __str__(self):
        return f"PluginRegistry({list(self.keys())})"
    
    def __repr__(self):
        return f"PluginRegistry({dict(self)})"


class Plugin: # Базовый класс для всех плагинов
    
    __registry = PluginRegistry() # приватный реестр
    
    _name = None   # Защищенный атрибут для переопределения
    
    def __init_subclass__(cls, **kwargs): # Автоматическая регистрация подклассов
        super().__init_subclass__(**kwargs)
        
        if not cls._name:
            raise ValueError(f"Плагин {cls.__name__} должен определить _name")
        
        if cls._name in cls.__registry:
            raise ValueError(f"Плагин '{cls._name}' уже существует")
            
        cls.__registry[cls._name] = cls
    
    def __str__(self):
        return f"Плагин '{self._name}'"
    
    def __repr__(self):
        return f"{self.__class__.__name__}()"
    
    @classmethod
    def get_registry(cls):
        return cls.__registry
    
    def execute(self, text):
        if not isinstance(text, str):
            raise ValueError("Ожидается строка")
        raise NotImplementedError("Метод должен быть реализован")


# Конкретные плагины
class UpperCasePlugin(Plugin):
    _name = "upper"
    
    def execute(self, text):
        if not isinstance(text, str):
            raise ValueError("Ожидается строка")
        return text.upper()


class ReversePlugin(Plugin):
    _name = "reverse"
    
    def execute(self, text):
        if not isinstance(text, str):
            raise ValueError("Ожидается строка")
        return text[::-1]


if __name__ == "__main__":
    registry = Plugin.get_registry()
    print(registry)
    
    plugin = registry["upper"]()
    print(plugin.execute("hello"))