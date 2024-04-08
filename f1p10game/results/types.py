from pydantic import BaseModel


class Result(BaseModel):
    position: str
    driver_number: int
    driver_name: str
    team_name: str
    time: str
    points: str


class Results(BaseModel):
    data: dict[str, list[Result]]
