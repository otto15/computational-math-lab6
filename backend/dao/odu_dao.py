from math import exp

from domain.odu import ODU

odu_storage: dict[int, ODU] = {
    0: ODU(
        0,
        "y + (1 + x) * y^2",
        lambda x, y: y + (1 + x) * (y ** 2),
        lambda x, y: -((exp(x) * (x * y + 1)) / y),
        lambda x, c: -(exp(x)) / (c + exp(x) * x)
    ),
    1: ODU(
        1,
        "x^2 - 2y",
        lambda x, y: (x ** 2) - 2 * y,
        lambda x, y: (1 / 4) * exp(2 * x) * (-2 * x ** 2 + 2 * x + 4 * y - 1),
        lambda x, c: c * exp(-2 * x) + x ** 2 / 2 - x / 2 + 1 / 4
    ),
    2: ODU(
        2,
        "x + y",
        lambda x, y: x + y,
        lambda x, y: exp(-x) * (x + y + 1),
        lambda x, c: c * exp(x) - x - 1
    )
}


def find_by_id(odu_id: int) -> ODU:
    return odu_storage[odu_id]


def find_all() -> list[ODU]:
    return list(odu_storage.values())
