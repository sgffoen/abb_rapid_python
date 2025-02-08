# Python to RAPID Generator for ABB Robots
Use this python class to generate simple RAPID modules for programming ABB robots.

## Installation
No installation is required. Just include `rapid.py` in your project and import the `RAPID` class.

## Functions
| Function Name                   | Description                                                  |
|----------------------------------|--------------------------------------------------------------|
| `set_tool(...)`                 | Creates a tooldata variable for the RAPID program.         |
| `set_zone(...)`                 | Creates a zone variable for the RAPID program.             |
| `set_speed(...)`                | Creates a speed data structure for the RAPID program.      |
| `set_workobject(...)`           | Creates a workobject variable for the RAPID program.       |
| `set_robtarget(...)`            | Creates a robot target variable for positioning.           |
| `add_MoveL(...)`                | Creates a linear move instruction.                          |
| `add_MoveJ(...)`                | Creates a joint move instruction.                           |
| `add_MoveAbsJ(...)`             | Creates an absolute joint move instruction.                 |
| `add_wait(...)`                 | Creates a wait instruction.                                 |
| `add_wait_digital_input(...)`   | Creates a wait for digital input instruction.              |
| `set_digital_output(...)`       | Creates a set digital output instruction.                   |
| `set_analog_output(...)`        | Creates a set analog output instruction.                    |
| `add_comment(...)`              | Creates a comment in the RAPID program.                    |
| `add_print_statement(...)`      | Creates a TPWrite instruction for printing messages.       |
| `begin_module(...)`             | Starts a new module in the RAPID program.                  |
| `end_module()`                  | Ends the current module in the RAPID program.              |
| `save_module(...)`              | Saves the generated RAPID program to a file.                |

## Usage Example

```python
from abb_rapid import RAPID, Zone

filename = "my_module.mod"
test_points = [(0, 250, 300), (0, 250, 800),
               (0, -250, 800), (0, -250, 300)]

# Initialize the RAPID generator
module = RAPID()

# Set the module and procedure names
module.begin_module(name="TestModule", name_procedure="main")

# Create tool, zone and speed variables at the beginning of the module
module.add_comment("Variables must be defined at the top of the module")
module.set_tool(name="tool")
module.set_tool(name="gripper", tool_frame_pos=[
                0, 0, 100], load_data_mass=2)
module.set_zone(name="zone")
module.set_zone(name="zone_10", val=Zone.Z10)
module.set_speed(name="speed_slow", velocity_tcp=50, velocity_orient=50)
module.set_speed(name="speed_fast", velocity_tcp=500, velocity_orient=150)
module.set_workobject(name="wobj", uf_frame_pos=[800, 0, 0])

# Example of how to use signal functions
module.add_comment("Examples of how to use signal functions")
module.set_digital_output(name="do1", value=1)
module.add_wait(time=1)
module.set_digital_output(name="do1", value=0)
module.add_wait(time=1)
module.set_analog_output(name="ao1", value=50)
module.add_wait(time=1)
module.set_analog_output(name="ao1", value=0)
module.add_wait(time=1)

# Example of how to use motion functions
module.add_comment("Examples of how to use motion functions")
module.add_MoveAbsJ(joint_positions=[0, 0, 0, 0, 0, 0], name_speed="speed_slow", name_zone="zone")
for point in test_points:
    module.add_MoveL(list(point), [1, 0, 0, 0], name_speed="speed_fast", name_tool="tool", name_zone="zone_10")
for point in test_points:
    module.add_MoveJ(list(point), [1, 0, 0, 0], name_speed="speed_fast", name_tool="gripper", name_zone="zone")

# Example of how to use print statements
module.add_comment("Examples of how to use TP Write functions")
module.add_print_statement("Hello, world!")
module.add_print_statement("Number of MoveL points:", len(test_points))
module.add_print_statement("We done?", True)
module.add_print_statement("We really done?", "Yes")

module.end_module()

module.save_module(filename)
print(f"RAPID module saved as {filename}")
```
### Output
```mod
MODULE TestModule
PROC main()
! Variables must be defined at the top of the module
VAR tooldata tool:=[TRUE,[[0, 0, 0],[1, 0, 0, 0]],[0,[0, 0, 0],[1, 0, 0, 0],0,0,0]];
VAR tooldata gripper:=[TRUE,[[0, 0, 100],[1, 0, 0, 0]],[2,[0, 0, 0],[1, 0, 0, 0],0,0,0]];
VAR zonedata zone:=z0;
VAR zonedata zone_10:=z10;
VAR speeddata speed_slow:=[50,50,0,0];
VAR speeddata speed_fast:=[500,150,0,0];
VAR wobjdata wobj:=[FALSE,TRUE,"",[[800, 0, 0],[1, 0, 0, 0]],[[0, 0, 0],[1, 0, 0, 0]]];
! Examples of how to use signal functions
SetDO do1, 1;
WaitTime 1;
SetDO do1, 0;
WaitTime 1;
SetAO ao1, 50;
WaitTime 1;
SetAO ao1, 0;
WaitTime 1;
! Examples of how to use motion functions
MoveAbsJ [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]], speed_slow, zone, tool\Wobj:=wobj;
MoveL [[0, 250, 300],[1, 0, 0, 0],[0, 0, 0, 1],[0, 0, 0, 0, 0, 0]], speed_fast, zone_10, tool\Wobj:=wobj;
MoveL [[0, 250, 800],[1, 0, 0, 0],[0, 0, 0, 1],[0, 0, 0, 0, 0, 0]], speed_fast, zone_10, tool\Wobj:=wobj;
MoveL [[0, -250, 800],[1, 0, 0, 0],[0, 0, 0, 1],[0, 0, 0, 0, 0, 0]], speed_fast, zone_10, tool\Wobj:=wobj;
MoveL [[0, -250, 300],[1, 0, 0, 0],[0, 0, 0, 1],[0, 0, 0, 0, 0, 0]], speed_fast, zone_10, tool\Wobj:=wobj;
MoveJ [[0, 250, 300],[1, 0, 0, 0],[0, 0, 0, 1],[0, 0, 0, 0, 0, 0]], speed_fast, zone, gripper\Wobj:=wobj;
MoveJ [[0, 250, 800],[1, 0, 0, 0],[0, 0, 0, 1],[0, 0, 0, 0, 0, 0]], speed_fast, zone, gripper\Wobj:=wobj;
MoveJ [[0, -250, 800],[1, 0, 0, 0],[0, 0, 0, 1],[0, 0, 0, 0, 0, 0]], speed_fast, zone, gripper\Wobj:=wobj;
MoveJ [[0, -250, 300],[1, 0, 0, 0],[0, 0, 0, 1],[0, 0, 0, 0, 0, 0]], speed_fast, zone, gripper\Wobj:=wobj;
! Examples of how to use TP Write functions
TPWrite "Hello, world!";
TPWrite "Number of MoveL points:"\Num:=4;
TPWrite "We done?"\Bool:=TRUE;
TPWrite "We really done? Yes";
ENDPROC
ENDMODULE
```
