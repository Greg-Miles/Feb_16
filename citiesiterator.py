import json
from dataclasses import dataclass, fields
from typing import Self, List, Dict

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
            self.cities = []
            for city in cities_data:
                if City.validate_city_data(city):
                    self.cities.append(City(**city))
                else:
                    raise ValueError("Неверный формат данных json-файла")


        self.index = 0

    def __iter__(self)-> Self:
        return self
    
    def __next__(self) -> City:
        if self.index >= len(self.cities):
            raise StopIteration
        city = self.cities[self.index]
        self.index += 1
        return city

c_iter = CitiesIterator("cities.json")
print(next(c_iter))
print(next(c_iter))
