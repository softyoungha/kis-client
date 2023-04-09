from typing import Union
import yaml


def load_yaml(file_path: str) -> Union[list, dict]:
    """ load yaml file """
    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data
