import json
from dataclasses import dataclass, fields
from typing import Self, List, Dict, Any, Bool
from pprint import pprint

@dataclass
class City:
    """
    Датакласс для хранения информации о городе. Поля:
    - lat: Широта города.
    - lon: Долгота города.
    - district: Федеральный округ.
    - name: Название.
    - population: Население.
    - subject: Регион, в котором город находится.
    """
    lat: float
    lon: float
    district: str
    name: str
    population: int
    subject: str

    @classmethod
    def validate_city_data(cls, city_data: Dict[str, Any]) -> Bool:
        """
        Метод валидации данных о городе. Проверяет, что все необходимые поля присутствуют в словаре.
        :param city_data: Словарь с данными о городе.
        :return: True, если данные валидны, иначе False.
        """
        
        if 'coords' not in  city_data or 'lat' not in city_data['coords'] or 'lon' not in city_data['coords']:
            return False
        coords = city_data.pop("coords")
        city_data['lat'] = float(coords['lat'])
        city_data['lon'] = float(coords['lon'])
        required_fields = {field.name for field in fields(cls)}
        provided_fields = set(city_data.keys())
        return required_fields == provided_fields

class CitiesIterator:
    """
    Класс итератора для перебора городов. При создании принимает путь к файлу с данными о городах.
    :param filepath: str. Путь к файлу с данными о городах.
    :attr all_cities: List[City]. Список всех городов.
    :attr cities: List[City]. Список объектов City для фильтрации или сортировки.
    :attr index: int. Индекс текущего города.
    :raises ValueError: Если данные в файле невалидны.
    """

    def __init__(self, filepath: str):
        """
        Инициализирует итератор используя данные из JSON-файла.
        :param filepath: str. Путь к файлу с данными о городах.
        :raises ValueError: Если данные в файле невалидны.
        """

        with open(filepath, "r", encoding="utf-8-sig")as file:
            cities_data = json.load(file)
            self.all_cities = []
            for city in cities_data:
                if City.validate_city_data(city):
                    self.all_cities.append(City(**city))
                else:
                    raise ValueError("Неверный формат данных json-файла")

        self.cities = self.all_cities.copy()
        self.index = 0

    def __iter__(self)-> Self:
        """
        Делает класс итератором.
        :return: self. 
        """
        return Self
    
    def __next__(self) -> City:
        """
        Возвращает следующий город из списка.
        :return: City. Следующий город из списка.
        :raises StopIteration: Если все города были пройдены.
        """
        if self.index >= len(self.cities):
            raise StopIteration
        city = self.cities[self.index]
        self.index += 1
        return city
    
    def set_population_filter(self, min_pop: int = 1, max_pop: int = 20_000_000)-> Self:
        """
        Устанавливает фильтр по населению.
        :param min_pop: int. Минимальное население.
        :param max_pop: int. Максимальное население.
        :return: Self. Итератор с установленным фильтром.
        """
        self.cities = [city for city in self.all_cities if min_pop <= city.population <= max_pop]
        self.index = 0
        return Self

    def sort_by_parameter(self, parameter: str, reverse: bool = False) -> Self:
        """
        Сортировщик по параметру.
        :param parameter: str. Параметр для сортировки.
        :param reverse: bool. Флаг для сортировки по убыванию.
        :return: Self. Итератор с отсортированными городами.
        """
        self.cities.sort(key=lambda city: getattr(city, parameter), reverse=reverse)
        self.index = 0
        return self



c_iter = CitiesIterator("cities.json")

c_iter.set_population_filter(10000, 20000)
pprint(next(c_iter))
pprint(next(c_iter))
c_iter.set_population_filter(20000, 22000)
c_iter.sort_by_parameter("district")
pprint(list(c_iter), sort_dicts=False)
c_iter.sort_by_parameter("subject")
pprint(list(c_iter), sort_dicts=False)
