from typing import Callable


class ODU:
    odu_id: int
    representation: str
    f: Callable[[float, float], float]
    calc_coefficient: Callable[[float, float], float]
    answer: Callable[[float, float], float]

    def __init__(self, odu_id, representation, f, calc_coefficient, answer):
        self.odu_id = odu_id
        self.representation = representation
        self.f = f
        self.calc_coefficient = calc_coefficient
        self.answer = answer


class ODUResult:
    result: list[tuple[float, float]]

    def __init__(self, x, y):
        self.result = list(zip(x, y))
