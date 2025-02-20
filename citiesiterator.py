import json
from dataclasses import dataclass, fields
from typing import Self, List, Dict
from pprint import pprint

@dataclass
class City:
    coords: Dict[str, str]
    district: str
    name: str
    population: int
    subject: str

    @classmethod
    def validate_city_data(cls, city_data: dict) -> bool:
        required_fields = {field.name for field in fields(cls)}
        provided_fields = set(city_data.keys())
        return required_fields == provided_fields

class CitiesIterator:

    def __init__(self, filepath: str):

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
        return self
    
    def __next__(self) -> City:
        if self.index >= len(self.cities):
            raise StopIteration
        city = self.cities[self.index]
        self.index += 1
        return city
    
    def set_population_filter(self, min_pop: int = 1, max_pop: int = 20_000_000)-> Self:
        self.cities = [city for city in self.all_cities if min_pop <= city.population <= max_pop]
        self.index = 0
        return self

    def sort_by_parameter(self, parameter: str, reverse: bool = False) -> Self:
        self.cities.sort(key=lambda city: getattr(city, parameter), reverse=reverse)
        self.index = 0
        return self



c_iter = CitiesIterator("cities.json")

c_iter.set_population_filter(10000, 20000)
print(next(c_iter))
print(next(c_iter))
c_iter.set_population_filter(20000, 22000)
c_iter.sort_by_parameter("district")
pprint(list(c_iter), sort_dicts=False)
c_iter.sort_by_parameter("subject")
pprint(list(c_iter), sort_dicts=False)
