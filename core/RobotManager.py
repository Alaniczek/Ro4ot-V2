from typing import Optional
from RobotKit import RobotKit
from CommandManager import CommandManager

class RobotManager:
    def __init__(self):
        self.selected_robot: Optional[RobotKit] = None
        self.command_manager: Optional[CommandManager] = None
        self.robot_units_path: str = '../../Jsons/robotUnits'

    def changePath(self, path: str):
        self.robot_path = path
    def selectRobot(self, robot: RobotKit):
        self.selected_robot = robot
