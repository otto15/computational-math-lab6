from domain.odu import ODUResult
from service.method import runge
from math import ceil


def solve(f, initial_conditions, h, bounds, accuracy):
    n = ceil((bounds[1] - bounds[0]) / h) + 1
    if n < 4:
        return ODUResult([], [])

    x = [bounds[0] + h * i for i in range(n)]

    first_dots: ODUResult = runge.solve(f, initial_conditions, h, [x[0], x[3]], accuracy)

    runge_x, runge_result = [el[0] for el in first_dots.result], [el[1] for el in first_dots.result]
    y = runge_result[:4]

    for i in range(4, n):
        y_prediction = prediction(h, f, x, y, i)
        y_correction = correction(h, f, x, y, i, y_prediction)

        while abs(y_correction - y_prediction) > accuracy:
            y_prediction = y_correction
            y_correction = correction(h, f, x, y, i, y_prediction)
        y.append(y_correction)

    return ODUResult(x, y)


def prediction(h, f, x, y, i):
    tmp = 2 * f(x[i - 3], y[i - 3]) - f(x[i - 2], y[i - 2]) + 2 * f(x[i - 1], y[i - 1])
    return y[i - 4] + 4 * h * tmp / 3


def correction(h, f, x, y, i, y_pred):
    tmp = f(x[i - 2], y[i - 2]) + 4 * f(x[i - 1], y[i - 1]) + f(x[i], y_pred)
    return y[i - 2] + h * tmp / 3
