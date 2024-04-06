from pydantic import BaseModel


class Result(BaseModel):
    position: str
    driver_number: int
    driver_name: str
    team_name: str
    time: str
    points: int


class Results(BaseModel):
    data: list[dict[str, list[Result]]]
