import re
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class RobotTarget:
    position: List[float]  # [x, y, z]
    orientation: List[float]  # [q1, q2, q3, q4] quaternion
    conf: List[int]  # [cf1, cf4, cf6, cfx]
    ext_axes: List[float]  # [eax_a, eax_b, eax_c, eax_d, eax_e, eax_f]
    speed: str
    zone: str
    tool: str
    wobj: Optional[str] = None
    move_type: Optional[str] = None  # MoveJ, MoveL, MoveAbsJ

class RapidParser:
    def __init__(self):
        self.targets: List[RobotTarget] = []
        self.speed_data: Dict[str, List[float]] = {}
        self.zone_data: Dict[str, List[float]] = {}
        self.tool_data: Dict[str, Dict[str, Any]] = {}
        self.wobj_data: Dict[str, Dict[str, Any]] = {}

    def parse_speed_data(self, line: str) -> None:
        """Parse speeddata declarations"""
        match = re.match(r'TASK PERS speeddata (\w+):=\[([\d.,\s]+)\];', line)
        if match:
            name, values = match.groups()
            self.speed_data[name] = [float(v) for v in values.split(',')]

    def parse_zone_data(self, line: str) -> None:
        """Parse zonedata declarations"""
        match = re.match(r'TASK PERS zonedata (\w+):=\[([\w.,\s]+)\];', line)
        if match:
            name, values = match.groups()
            self.zone_data[name] = [float(v) if v.replace('.', '').isdigit() else v 
                                  for v in values.split(',')]

    def parse_tool_data(self, line: str) -> None:
        """Parse tooldata declarations"""
        match = re.match(r'PERS tooldata (\w+):=\[([\w.,\s\[\]]+)\];', line)
        if match:
            name, values = match.groups()
            # This is a simplified parsing - you might want to enhance this
            self.tool_data[name] = {'raw': values}

    def parse_wobj_data(self, line: str) -> None:
        """Parse wobjdata declarations"""
        match = re.match(r'TASK PERS wobjdata (\w+):=\[([\w.,\s\[\]""]+)\];', line)
        if match:
            name, values = match.groups()
            # This is a simplified parsing - you might want to enhance this
            self.wobj_data[name] = {'raw': values}

    def parse_move_command(self, line: str) -> Optional[RobotTarget]:
        """Parse MoveJ, MoveL, and MoveAbsJ commands"""
        move_pattern = r'(MoveJ|MoveL|MoveAbsJ)\s+\[\[([\d.,\s-]+)\],\[([\d.,\s-]+)\],(\w+),\[([\d.,\s-]+)\]\],(\w+),(\w+),(\w+)(?:\s*\\WObj:=(\w+))?'
        match = re.match(move_pattern, line)
        
        if not match:
            return None

        move_type, pos_str, orient_str, conf_str, ext_axes_str, speed, zone, tool, wobj = match.groups()
        
        # Parse position
        position = [float(x) for x in pos_str.split(',')]
        
        # Parse orientation (quaternion)
        orientation = [float(q) for q in orient_str.split(',')]
        
        # Parse configuration
        conf = [int(c) for c in conf_str.split(',')]
        
        # Parse external axes
        ext_axes = [float(e) if e != '9E9' else float('inf') for e in ext_axes_str.split(',')]
        
        return RobotTarget(
            position=position,
            orientation=orientation,
            conf=conf,
            ext_axes=ext_axes,
            speed=speed,
            zone=zone,
            tool=tool,
            wobj=wobj,
            move_type=move_type
        )

    def parse_file(self, file_path: str) -> None:
        """Parse a RAPID file and extract all targets and data"""
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Try to parse different types of declarations
                self.parse_speed_data(line)
                self.parse_zone_data(line)
                self.parse_tool_data(line)
                self.parse_wobj_data(line)
                
                # Try to parse move commands
                target = self.parse_move_command(line)
                if target:
                    self.targets.append(target)

    def get_targets(self) -> List[RobotTarget]:
        """Return all parsed targets"""
        return self.targets

    def get_speed_data(self) -> Dict[str, List[float]]:
        """Return all parsed speed data"""
        return self.speed_data

    def get_zone_data(self) -> Dict[str, List[float]]:
        """Return all parsed zone data"""
        return self.zone_data

    def get_tool_data(self) -> Dict[str, Dict[str, Any]]:
        """Return all parsed tool data"""
        return self.tool_data

    def get_wobj_data(self) -> Dict[str, Dict[str, Any]]:
        """Return all parsed work object data"""
        return self.wobj_data

def main():
    # Example usage
    parser = RapidParser()
    parser.parse_file('data/test_T_ROB1.mod')
    
    # Print all targets
    print("Robot Targets:")
    for i, target in enumerate(parser.get_targets(), 1):
        print(f"\nTarget {i}:")
        print(f"  Position: {target.position}")
        print(f"  Orientation: {target.orientation}")
        print(f"  Configuration: {target.conf}")
        print(f"  External Axes: {target.ext_axes}")
        print(f"  Speed: {target.speed}")
        print(f"  Zone: {target.zone}")
        print(f"  Tool: {target.tool}")
        print(f"  Work Object: {target.wobj}")
        print(f"  Move Type: {target.move_type}")

if __name__ == "__main__":
    main() 