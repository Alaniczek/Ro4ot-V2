class RobotKit:
    def __init__(self, robot_ip: str, robot_port: int, robot_model: str, robot_name: str):
        self.robot_ip: str = robot_ip
        self.robot_port: int = robot_port
        self.robot_model: str = robot_model
        self.robot_name: str = robot_name