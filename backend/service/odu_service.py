from typing import Callable

from dao import odu_dao
from domain.odu import ODU, ODUResult
from dto.request import ODUTo
from dto.response import ODUViewTo, ODUResultTo, PointTo
from service.method import euler, miln, runge


def get_all() -> list[ODUViewTo]:
    return list(map(transform, odu_dao.find_all()))


def transform(odu: ODU) -> ODUViewTo:
    return ODUViewTo(
        equation_id=odu.odu_id,
        string_rep=odu.representation
    )


def check_accuracy(f: Callable[[float, float], float], c: float, x: list[float], y: list[float]) -> float:
    return max(list(map(lambda i: abs(f(x[i], c) - y[i]), range(0, len(x)))))


def solve(odu: ODUTo) -> ODUResultTo:
    chosen_odu: ODU = odu_dao.find_by_id(odu.equation_id)
    calculated_coefficient: float = chosen_odu.calc_coefficient(odu.x_0, odu.y_0)

    h: float = odu.h

    print("runge")
    runge_res: ODUResult = runge.solve(chosen_odu.f, odu.y_0, odu.h, (odu.x_0, odu.x_0 + odu.length), odu.e)

    print("mmiln")
    miln_res: ODUResult = miln.solve(chosen_odu.f, odu.y_0, odu.h, (odu.x_0, odu.x_0 + odu.length), odu.e)
    while not check_accuracy(chosen_odu.answer, calculated_coefficient, [el[0] for el in miln_res.result],
                             [el[1] for el in miln_res.result]):
        h /= 2
        miln_res = miln.solve(chosen_odu.f, odu.y_0, odu.h, (odu.x_0, odu.x_0 + odu.length), odu.e)

    print("euler")
    euler_res: ODUResult = euler.solve(chosen_odu.f, odu.y_0, odu.h, (odu.x_0, odu.x_0 + odu.length), odu.e)

    return ODUResultTo(
        euler=list(map(lambda el: PointTo(x=el[0], y=el[1]), euler_res.result)),
        miln=list(map(lambda el: PointTo(x=el[0], y=el[1]), miln_res.result)),
        runge=list(map(lambda el: PointTo(x=el[0], y=el[1]), runge_res.result)),
        exact=list(map(lambda el: PointTo(x=el, y=chosen_odu.answer(el, calculated_coefficient)),
                       [el[0] for el in miln_res.result]))
    )
