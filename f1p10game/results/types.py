from pydantic import BaseModel


class Result(BaseModel):
    position: int
    driver_number: int
    driver_name: str
    team_name: str
    time: str
    points: int


class Results(BaseModel):
    data: dict[str, list[Result]]
