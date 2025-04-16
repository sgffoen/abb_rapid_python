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
        self.targets = []
        self.speed_data = {}
        self.zone_data = {}
        self.tool_data = {}
        self.wobj_data = {}

    def parse_speed_data(self, line):
        """Parse speeddata declarations"""
        match = re.match(r'TASK PERS speeddata (\w+):=\[([\d.,\s]+)\];', line)
        if match:
            name, values = match.groups()
            self.speed_data[name] = [float(v) for v in values.split(',')]

    def parse_zone_data(self, line):
        """Parse zonedata declarations"""
        match = re.match(r'TASK PERS zonedata (\w+):=\[([\w.,\s]+)\];', line)
        if match:
            name, values = match.groups()
            self.zone_data[name] = [float(v) if v.replace('.', '').isdigit() else v 
                                  for v in values.split(',')]

    def parse_tool_data(self, line):
        """Parse tooldata declarations"""
        match = re.match(r'PERS tooldata (\w+):=\[([\w.,\s\[\]]+)\];', line)
        if match:
            name, values = match.groups()
            # This is a simplified parsing - you might want to enhance this
            self.tool_data[name] = {'raw': values}

    def parse_wobj_data(self, line):
        """Parse wobjdata declarations"""
        match = re.match(r'TASK PERS wobjdata (\w+):=\[([\w.,\s\[\]""]+)\];', line)
        if match:
            name, values = match.groups()
            # This is a simplified parsing - you might want to enhance this
            self.wobj_data[name] = {'raw': values}

    def parse_move_command(self, line):
        """Parse move commands to extract position and orientation"""
        # Pattern to match position and orientation in move commands
        pattern = r'(MoveJ|MoveL|MoveAbsJ)\s+\[\[([\d.,\s-]+)\],\[([\d.,\s-]+)\]'
        
        match = re.search(pattern, line)
        if match:
            try:
                move_type = match.group(1)
                pos_str = match.group(2)
                orient_str = match.group(3)
                
                # Parse position
                position = [float(x.strip()) for x in pos_str.split(',')]
                
                # Parse orientation (quaternion)
                orientation = [float(q.strip()) for q in orient_str.split(',')]
                
                return {
                    'move_type': move_type,
                    'position': position,
                    'orientation': orientation
                }
            except ValueError as e:
                print(f"Error parsing values in line: {line.strip()}")
                print(f"Error details: {str(e)}")
                return None
        return None

    def parse_file(self, file_path):
        """Parse a RAPID file and extract positions"""
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

    def get_targets(self):
        """Return all parsed targets"""
        return self.targets

    def get_speed_data(self):
        """Return all parsed speed data"""
        return self.speed_data

    def get_zone_data(self):
        """Return all parsed zone data"""
        return self.zone_data

    def get_tool_data(self):
        """Return all parsed tool data"""
        return self.tool_data

    def get_wobj_data(self):
        """Return all parsed work object data"""
        return self.wobj_data

def main():
    # Example usage
    parser = RapidParser()
    file_path = 'data/test_movel_T_ROB1.mod'
    
    # Verify file exists
    try:
        with open(file_path, 'r') as f:
            print(f"Successfully opened file: {file_path}")
            # Print first few lines to verify content
            print("\nFirst few lines of the file:")
            for i, line in enumerate(f):
                if i < 5:  # Print first 5 lines
                    print(f"Line {i+1}: {line.strip()}")
                else:
                    break
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return
    
    # Parse the file
    parser.parse_file(file_path)
    
    # Print all targets
    print("\nRobot Positions and Orientations:")
    for i, target in enumerate(parser.get_targets(), 1):
        print(f"\nTarget {i}:")
        print(f"  Move Type: {target['move_type']}")
        print(f"  Position: {target['position']}")
        print(f"  Orientation: {target['orientation']}")

if __name__ == "__main__":
    main() 