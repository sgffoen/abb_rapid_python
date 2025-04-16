import ghpythonlib.components as ghc
import Rhino.Geometry as rg
import math
from rapid_parser import RapidParser
from pathlib import Path


def quaternion_to_plane(position, quaternion):
    """Convert position and quaternion to Rhino plane"""
    # Create a point from position
    point = rg.Point3d(position[0], position[1], position[2])
    
    # Convert quaternion to rotation matrix
    qw, qx, qy, qz = quaternion
    xx = qx * qx
    yy = qy * qy
    zz = qz * qz
    xy = qx * qy
    xz = qx * qz
    yz = qy * qz
    wx = qw * qx
    wy = qw * qy
    wz = qw * qz
    
    # Create rotation matrix
    matrix = rg.Transform()
    matrix.M00 = 1 - 2 * (yy + zz)
    matrix.M01 = 2 * (xy - wz)
    matrix.M02 = 2 * (xz + wy)
    matrix.M10 = 2 * (xy + wz)
    matrix.M11 = 1 - 2 * (xx + zz)
    matrix.M12 = 2 * (yz - wx)
    matrix.M20 = 2 * (xz - wy)
    matrix.M21 = 2 * (yz + wx)
    matrix.M22 = 1 - 2 * (xx + yy)
    
    # Create plane and transform it
    plane = rg.Plane.WorldXY
    plane.Transform(matrix)
    plane.Origin = point
    
    return plane

def create_gh_targets(rapid_targets):
    """Convert RAPID targets to Grasshopper Robot targets"""
    gh_targets = []
    
    for target in rapid_targets:
        # Create plane from position and orientation
        plane = quaternion_to_plane(target['position'], target['orientation'])
        
        # Create Grasshopper Robot target
        gh_target = ghc.Robots.Createtarget(plane=plane)
        
        # Set speed (default values for now)
        speed = ghc.Robots.Createspeed(translation=5)
        gh_target.Speed = speed
        
        # Set zone (default values for now)
        gh_target.Zone.set_Distance(3.0)
        
        gh_targets.append(gh_target)
    
    return gh_targets

def set_tool(target, tool):
    """Set the tool for the robot target"""
    target.set_Tool(tool)

def create_gh_targets_from_rapid_file(file_path):
    # Parse RAPID file
    parser = RapidParser()
    parser.parse_file(file_path)
    rapid_targets = parser.get_targets()
    
    return create_gh_targets(rapid_targets)

def get_data_dir():
    return Path(__file__).parent / 'data'

def main():
    # Parse RAPID file
    parser = RapidParser()
    file_path = 'data/test_movel_T_ROB1.mod'
    parser.parse_file(file_path)
    rapid_targets = parser.get_targets()
    
    # Convert to Grasshopper Robot targets
    gh_targets = create_gh_targets(rapid_targets)
    
    # Print information about the created targets
    print("\nCreated Grasshopper Robot Targets:")
    for i, target in enumerate(gh_targets, 1):
        print(f"\nTarget {i}:")
        print(f"  Position: {target.Plane.Origin}")
        print(f"  Speed: {target.Speed}")
        print(f"  Zone Distance: {target.Zone.get_Distance()}")

if __name__ == "__main__":
    main() 