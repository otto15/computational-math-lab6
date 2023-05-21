from pydantic import BaseModel


class ODUTo(BaseModel):
    equation_id: int
    x_0: float
    y_0: float
    length: float
    h: float
    e: float
