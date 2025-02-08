"""
Simple python class that generates RAPID modules for ABB robots.

Author: Madeline Gannon (atonaton.com)
Date: 02.08.2025
"""

from enum import Enum


class Zone(Enum):
    Z0 = 0
    Z5 = 5
    Z10 = 10
    Z50 = 50
    Z100 = 100
    Z200 = 200


class RAPID:

    def __init__(self):
        self.program: str = ""
        self.name_wobj = None

    def set_tool(
            self,
            name: str = "tool",
            rob_hold: bool = True,
            tool_frame_pos=[0, 0, 0],
            tool_frame_orient=[1, 0, 0, 0],
            load_data_mass=0,
            load_data_cog=[0, 0, 0],
            load_data_orient=[1, 0, 0, 0],
            load_data_inertia=[0, 0, 0]):
        """Creates a tooldata variable for the RAPID program.

        Args:
            name (str, optional): Tool variable name. Defaults to "tool".
            rob_hold (bool, optional): Flag for if robot is holding tool. Defaults to True.
            tool_frame_pos (list, optional): Position of Tool Frame. Defaults to [0, 0, 0].
            tool_frame_orient (list, optional): Orientation of Tool Frame. Defaults to [1, 0, 0, 0].
            load_data_mass (int, optional): Tool Load Mass. Defaults to 0.
            load_data_cog (list, optional): Tool Load Center of Gravity. Defaults to [0, 0, 0].
            load_data_orient (list, optional): Tool Load Orientation. Defaults to [1, 0, 0, 0].
            load_data_inertia (list, optional): Tool Load Inertia. Defaults to [0, 0, 0].
        """

        tool = f"VAR tooldata {name}:=[{str(rob_hold).upper()},[{tool_frame_pos},{tool_frame_orient}],[{
            load_data_mass},{load_data_cog},{load_data_orient},{load_data_inertia[0]},{load_data_inertia[1]},{load_data_inertia[2]}]];"
        self.program += tool + "\n"

    def set_zone(self, name="zone", val=Zone.Z0):
        """Creates a zone variable for the RAPID program.

        Args:
            name (str, optional): Zone variable name. Defaults to "zone".
            val (int, optional): Zone value. Valid options are 0, 5, 10, 50, 100, 200. Defaults to 0 (fine).
        """

        zone = f"VAR zonedata {name}:=z{val.value};"
        self.program += zone + "\n"

    def set_speed(self, name="speed", velocity_tcp=50, velocity_orient=50, velocity_leax=0, velocity_reax=0):
        """Creates a speed data structure for the RAPID program.

        Args:
            name(str, optional): Speed variable name. Defaults to "speed".
            velocity_tcp(int, optional): TCP Velocity. Defaults to "50".
            velocity_orient(int, optional): Orientation Velocity. Defaults to "50".
            velocity_leax(int, optional): Linear External Axis Velocity. Defaults to "0".
            velocity_reax(int, optional): Rotary External Axis Velocity. Defaults to "0".
        """
        
        speed = f"VAR speeddata {name}:=[{velocity_tcp},{
            velocity_orient},{velocity_leax},{velocity_reax}];"
        self.program += speed + "\n"

    def set_workobject(
        self,
        name="wobj",
        rob_hold=False,
        uf_prog=True,
        uf_mecunit="",
        uf_frame_pos=[0, 0, 0],
        uf_frame_orient=[1, 0, 0, 0],
        of_frame_pos=[0, 0, 0],
        of_frame_orient=[1, 0, 0, 0]
    ):
        """Creates a workobject variable for the RAPID program.

        Args:
            name (str, optional): Work object variable name. Defaults to "wobj".
            rob_hold (bool, optional): Whether the robot holds the work object. Defaults to False.
            uf_prog (bool, optional): Whether user frame is used. Defaults to True.
            uf_mecunit (str, optional): User mechanical unit name defined in system parameters. Defaults to "".
            uf_frame_pos (list, optional): User frame position [X, Y, Z]. Defaults to [0, 0, 0].
            uf_frame_orient (list, optional): User frame orientation [Q1, Q2, Q3, Q4]. Defaults to [1, 0, 0, 0].
            of_frame_pos (list, optional): Object frame position [X, Y, Z]. Defaults to [0, 0, 0].
            of_frame_orient (list, optional): Object frame orientation [Q1, Q2, Q3, Q4]. Defaults to [1, 0, 0, 0].
        """
        self.name_wobj = name
        wobj = (
            f"VAR wobjdata {name}:=[{str(rob_hold).upper()},{str(uf_prog).upper()},\"{uf_mecunit}\","
            f"[{uf_frame_pos},{uf_frame_orient}],[{of_frame_pos},{of_frame_orient}]];"
        )
        self.program += wobj + "\n"

    def set_robtarget(self, pos=[0, 0, 0], orient=[1, 0, 0, 0], confdata=[0, 0, 0, 1], extax=[0, 0, 0, 0, 0, 0]):
        """_summary_

        Args:
            pos (list, optional): Position. Defaults to [0, 0, 0].
            orient (list, optional): Orientation. Defaults to [1, 0, 0, 0].
            confdata (list, optional): Configuration. Defaults to [0, 0, 0, 1].
            extax (list, optional): Position of each external axis. Defaults to [0, 0, 0, 0, 0, 0].

        Returns:
            string: robtarget
        """
        return f"[{pos},{orient},{confdata},{extax}]"

    def add_MoveL(self, pos=[0, 0, 0], orient=[1, 0, 0, 0], confdata=[0, 0, 0, 1], extax=[0, 0, 0, 0, 0, 0], name_speed="speed", name_zone="zone", name_tool="tool"):
        """Creates a linear move.

        Args:
            pos (list, optional): Position. Defaults to [0, 0, 0].
            orient (list, optional): Orientation. Defaults to [1, 0, 0, 0].
            confdata (list, optional): Configuration. Defaults to [0, 0, 0, 1].
            extax (list, optional): Position of each external axis. Defaults to [0, 0, 0, 0, 0, 0].
            name_speed (str, optional): Name of speeddata variable. Defaults to "speed".
            name_zone (str, optional): Name of zonedata variable. Defaults to "zone".
            name_tool (str, optional): Name of tooldata variable. Defaults to "tool".

        """
        self.program += f"MoveL {self.set_robtarget(pos, orient, confdata, extax)}, {
            name_speed}, {name_zone}, {name_tool}"
        if self.name_wobj is not None:
            self.program += f"\\Wobj:={self.name_wobj}"
        self.program += ";\n"

    def add_MoveJ(self, pos=[0, 0, 0], orient=[1, 0, 0, 0], confdata=[0, 0, 0, 1], extax=[0, 0, 0, 0, 0, 0], name_speed="speed", name_zone="zone", name_tool="tool"):
        """Creates a joint move.

        Args:
            pos (list, optional): Position. Defaults to [0, 0, 0].
            orient (list, optional): Orientation. Defaults to [1, 0, 0, 0].
            confdata (list, optional): Configuration. Defaults to [0, 0, 0, 1].
            extax (list, optional): Position of each external axis. Defaults to [0, 0, 0, 0, 0, 0].
            name_speed (str, optional): Name of speeddata variable. Defaults to "speed".
            name_zone (str, optional): Name of zonedata variable. Defaults to "zone".
            name_tool (str, optional): Name of tooldata variable. Defaults to "tool".
        """
        self.program += f"MoveJ {self.set_robtarget(pos, orient, confdata, extax)}, {name_speed}, {name_zone}, {name_tool}"
        if self.name_wobj is not None:
            self.program += f"\\Wobj:={self.name_wobj}"
        self.program += ";\n"

    def add_MoveAbsJ(self, joint_positions=[0, 0, 0, 0, 0, 0], extax=[0, 0, 0, 0, 0, 0], name_speed="speed", name_zone="zone", name_tool="tool"):
        """Creates an absolute joint move.

        Args:
            joint_positions (list, optional): Angle of each joint (in degrees). Defaults to [0, 0, 0, 0, 0, 0].
            extax (list, optional): Position of each external axis. Defaults to [0, 0, 0, 0, 0, 0].
            name_speed (str, optional): Name of speeddata variable. Defaults to "speed".
            name_zone (str, optional): Name of zonedata variable. Defaults to "zone".
            name_tool (str, optional): Name of tooldata variable. Defaults to "tool".
        """

        self.program += f"MoveAbsJ [{joint_positions}, {extax}], {name_speed}, {name_zone}, {name_tool}"
        if self.name_wobj is not None:
            self.program += f"\\Wobj:={self.name_wobj}"
        self.program += ";\n"

    def add_wait(self, time):
        """Creates a wait instruction.

        Args:
            time (int, optional): Time to wait (in seconds).
        """
        self.program += f"WaitTime {time};" + "\n"

    def add_wait_digital_input(self, input, value):
        """Creates a wait digital input instruction.

        Args:
            input (int): Digital input number.
            value (int): Value to wait for (0 or 1).
        """
        self.program += f"WaitDI {input}, {value};" + "\n"

    def set_digital_output(self, name, value):
        """Creates a set digital output instruction.

        Args:
            output (str): Name of digital output signal.
            value (int): Value to set (0 or 1).
        """
        self.program += f"SetDO {name}, {value};" + "\n"

    def set_analog_output(self, name, value):
        """Creates a set analog output instruction.

        Args:
            output (int): Name of analog output signal.
            value (int): Value to set (0-100).
        """
        self.program += f"SetAO {name}, {value};" + "\n"

    def add_comment(self, msg):
        """Creates a comment.

        Args:
            msg (str): Comment message.
        """
        self.program += f"! {msg}" + "\n"

    def add_print_statement(self, msg, val=None):
        """Creates a TPWrite instruction.

        Args:
            msg (str): Message to write.
            val (str, optional): Value to write. Defaults to None.
        """
        if val is not None:
            if isinstance(val, bool):
                # Convert True/False to RAPID-style TRUE/FALSE
                self.program += f'TPWrite "{msg}"\\Bool:={str(val).upper()};\n'
            elif isinstance(val, int):
                self.program += f'TPWrite "{msg}"\\Num:={val};\n'
            elif isinstance(val, float):
                self.program += f'TPWrite "{msg}"\\Dnum:={val};\n'
            elif isinstance(val, str):
                self.program += f'TPWrite "{msg} {val}";\n'
            else:
                raise TypeError(f"Unsupported type for val: {type(val)}")
        else:
            self.program += f"TPWrite \"{msg}\";" + "\n"

    def begin_module(self, name="MainModule", name_procedure="main"):
        self.program += f"MODULE {name}\nPROC {name_procedure}()" + "\n"

    def end_module(self):
        self.program += "ENDPROC\nENDMODULE"

    def save_module(self, filename):
        with open(filename, 'w') as file:
            file.write(self.program)
