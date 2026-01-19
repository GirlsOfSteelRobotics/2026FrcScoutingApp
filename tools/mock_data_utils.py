import dataclasses
import random
from typing import List


@dataclasses.dataclass
class IntValue:
    min_value: int
    max_value: int

    def get_value(self):
        return random.randint(self.min_value, self.max_value)


@dataclasses.dataclass
class BooleanValue:
    min_probability: float

    def get_value(self):
        val = random.random()
        return val > self.min_probability


@dataclasses.dataclass
class EnumValue:
    choices: List[str]
    probability: List[float]

    def get_value(self):
        x = random.choices(self.choices, weights=self.probability, k=1)[0]
        return x
