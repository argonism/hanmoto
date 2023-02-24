from pathlib import Path


def get_resource_dir() -> Path:
    return Path(__file__).parent.joinpath("resources")


def get_resource(file_path: str) -> Path:
    return get_resource_dir().joinpath(file_path)
