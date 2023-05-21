from pydantic import BaseModel


class ODUViewTo(BaseModel):
    equation_id: int
    string_rep: str


class PointTo(BaseModel):
    x: float
    y: float


class ODUResultTo(BaseModel):
    euler: list[PointTo]
    runge: list[PointTo]
    miln: list[PointTo]
    exact: list[PointTo]
