from typing import Optional
from pathlib import Path
import json

from RobotKit import RobotKit
from CommandManager import CommandManager

class RobotManager:
    def __init__(self):
        self.selected_robot: Optional[RobotKit] = None
        self.command_manager: Optional[CommandManager] = None
        self.robot_units_path: str = '../../Jsons/robotUnits'

    def changePath(self, path: str):
        self.robot_units_path = path

    def selectRobotByKit(self, robot: RobotKit):
        self.selected_robot = robot

    def selectRobotByName(self, robotName: str) -> bool:
        path_to_robot = Path(self.robot_units_path) / f"{robotName}.json"

        if not path_to_robot.is_file():
            return False

        data = json.loads(path_to_robot.read_text(encoding="utf-8"))

        robot_kit = RobotKit(
            data["IP"],
            int(data["Port"]),
            data["MODEL"],
            data["Name"]
        )

        self.selectRobotByKit(robot_kit)
        return True