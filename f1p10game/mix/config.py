import configparser
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    title: str
    initial_players: list[str]
    path_drivers: Path
    path_circuits: Path
    path_players: Path
    path_results: Path
    path_points_table: Path


def get_config():
    config = configparser.ConfigParser()
    config.read("config.ini")

    return Config(
        title=config.get("root", "title"),
        initial_players=[pl.strip() for pl in config.get("root", "initial_players").split(",")],
        path_drivers=Path(config.get("paths", "drivers_path")),
        path_circuits=Path(config.get("paths", "circuits_path")),
        path_players=Path(config.get("paths", "players_path")),
        path_results=Path(config.get("paths", "results_path")),
        path_points_table=Path(config.get("paths", "points_path"))
    )
