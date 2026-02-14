import carb
import omni.ui as ui
import omni.kit.app

STYLE = {
    "Window": {"background_color": 0xFF1A1A2E},
    "Label::header": {"font_size": 20, "color": 0xFFE0E0E0},
    "Label::subheader": {"font_size": 14, "color": 0xFFB0B0B0},
    "Label::category": {"font_size": 16, "color": 0xFFFFFFFF},
    "Label::item": {"font_size": 14, "color": 0xFFD0D0D0},
    "Label::description": {"font_size": 12, "color": 0xFF909090},
    "Button::tool": {"background_color": 0xFF2D2D5E, "border_radius": 6, "margin": 2, "padding": 8},
    "Button::tool:hovered": {"background_color": 0xFF3D3D7E},
    "CollapsableFrame": {
        "background_color": 0xFF16213E,
        "secondary_color": 0xFF0F3460,
        "border_radius": 6,
        "margin": 4,
        "padding": 6,
    },
    "Separator": {"color": 0xFF333366},
}

# Robotics tool definitions: (label, description, action_callback_name)
CATEGORIES = {
    "Manipulation": {
        "icon": "robot",
        "tools": [
            ("Articulation Inspector", "Inspect and control robot joint positions and velocities"),
            ("Manipulator Controller", "Position/velocity control for articulated manipulators"),
            ("Gripper Control", "Open-loop and surface gripper control"),
            ("Gain Tuner", "Tune PD gains for robot joints"),
        ],
    },
    "Navigation": {
        "icon": "car",
        "tools": [
            ("Wheeled Robot Control", "Drive and steer wheeled robot platforms"),
            ("Motion Generation", "Plan collision-free paths with Lula/RMPflow"),
            ("Cortex Behaviors", "Define and run task-level robot behaviors"),
        ],
    },
    "Sensors": {
        "icon": "eye",
        "tools": [
            ("Camera Inspector", "View and configure camera sensors"),
            ("Lidar Viewer", "Visualize RTX and PhysX lidar data"),
            ("Contact Sensor", "Monitor contact forces on rigid bodies"),
            ("IMU Sensor", "Read IMU acceleration and angular velocity"),
        ],
    },
    "Setup Tools": {
        "icon": "wrench",
        "tools": [
            ("Robot Assembler", "Assemble multi-body robots from URDF/MJCF"),
            ("Robot Wizard", "Step-by-step robot import and configuration"),
            ("XRDF Editor", "Edit robot description files"),
            ("Grasp Editor", "Define and test grasp poses"),
        ],
    },
    "Synthetic Data": {
        "icon": "camera",
        "tools": [
            ("Synthetic Recorder", "Record RGB, depth, segmentation from cameras"),
            ("Domain Randomization", "Randomize materials, lighting, poses for training"),
            ("Replicator Behaviors", "Define replicator behavior scripts"),
        ],
    },
}

# Map tool names to the Isaac Sim menu paths they open
TOOL_MENU_ACTIONS = {
    "Articulation Inspector": "Tools/Robotics/OmniGraph Controllers/Joint Position",
    "Manipulator Controller": "Tools/Robotics/OmniGraph Controllers/Joint Position",
    "Gripper Control": "Tools/Robotics/OmniGraph Controllers/Open Loop Gripper",
    "Gain Tuner": "Tools/Robotics/Gain Tuner",
    "Wheeled Robot Control": "Tools/Robotics/OmniGraph Controllers/Differential Controller",
    "Motion Generation": "Tools/Robotics/Motion Generation",
    "Cortex Behaviors": "Tools/Robotics/Cortex",
    "Camera Inspector": "Tools/Camera Inspector",
    "Robot Assembler": "Tools/Robotics/Robot Assembler",
    "Robot Wizard": "Window/Robot Wizard [Beta]",
    "XRDF Editor": "Tools/Robotics/XRDF Editor",
    "Grasp Editor": "Tools/Robotics/Grasp Editor",
    "Synthetic Recorder": "Tools/Synthetic Data Recorder",
}


class NwavesRoboticsWindow(ui.Window):
    def __init__(self, title, **kwargs):
        super().__init__(title, **kwargs)
        self.deferred_dock_in("Content", ui.DockPolicy.CURRENT_WINDOW_IS_ACTIVE)
        self.frame.set_build_fn(self._build_ui)

    def _build_ui(self):
        with self.frame:
            with ui.ScrollingFrame(
                horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
                style_type_name_override="TreeView",
            ):
                with ui.VStack(spacing=8, style=STYLE):
                    ui.Spacer(height=4)

                    # Header
                    with ui.HStack(height=50):
                        ui.Spacer(width=12)
                        with ui.VStack(spacing=2):
                            ui.Label("Nwaves.ai Robotics", name="header")
                            ui.Label("AI-Powered Simulation Platform", name="subheader")

                    ui.Separator(height=2, name="separator")
                    ui.Spacer(height=4)

                    # Build each category
                    for category_name, category_data in CATEGORIES.items():
                        self._build_category(category_name, category_data)

                    ui.Spacer(height=8)

    def _build_category(self, name, data):
        with ui.CollapsableFrame(name, height=0, collapsed=False):
            with ui.VStack(spacing=4):
                for tool_name, tool_desc in data["tools"]:
                    self._build_tool_button(tool_name, tool_desc)

    def _build_tool_button(self, name, description):
        with ui.HStack(height=40):
            ui.Spacer(width=8)
            btn = ui.Button(
                name,
                name="tool",
                width=ui.Fraction(1),
                height=36,
                clicked_fn=lambda n=name: self._on_tool_clicked(n),
                tooltip=description,
            )

    def _on_tool_clicked(self, tool_name):
        menu_path = TOOL_MENU_ACTIONS.get(tool_name)
        if menu_path:
            try:
                import omni.kit.menu.utils
                omni.kit.menu.utils.trigger_menu_click(menu_path)
                carb.log_info(f"[nwaves.ai.robotics] Opened: {tool_name}")
            except Exception as e:
                carb.log_warn(f"[nwaves.ai.robotics] Could not open {tool_name}: {e}")
        else:
            carb.log_info(f"[nwaves.ai.robotics] {tool_name} - no direct menu mapping, open via Isaac Sim menus")

    def destroy(self):
        super().destroy()
