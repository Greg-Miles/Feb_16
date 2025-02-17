import json
from dataclasses import dataclass, field
from typing import Self, List, Dict

@dataclass
class City:
    lat: float
    lon: float
    district: str
    name: str
    population: int
    subject: str

class CitiesIterator:

    def __init__(self, filepath: str):
        with open(filepath, "r")as file:
            self.cities = [City(**city) for city in json.load(file)]
        self.index = 0

    def __iter__(self)-> Self:
        return self
    
    def __next__(self) -> City:
        if self.index >= len(self.cities):
            raise StopIteration
        city = self.cities[self.index]
        self.index += 1
        return city