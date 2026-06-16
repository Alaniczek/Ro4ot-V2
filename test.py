import asyncio
import json
from contextlib import asynccontextmanager
from typing import Dict, Any, Set
from pathlib import Path


def start_robot_list() -> list[Dict[str, Any]]:
    robot_list = []
    dir_to_robot = Path('jsons/robotUnits')

    if dir_to_robot.exists():
        for file_path in dir_to_robot.glob('*.json'):
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                robot_list.append({
                    "robot_name": file_path.stem,
                    "content": json.load(f)
                })

    return robot_list


if __name__ == '__main__':
    lista_robotow = start_robot_list()
    print(lista_robotow)
