import carb
import omni.ui as ui

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
STYLE = {
    "Window": {"background_color": 0xFF1A1A2E},
    "Label::header": {"font_size": 20, "color": 0xFFE0E0E0},
    "Label::subheader": {"font_size": 13, "color": 0xFFB0B0B0},
    "Label::category": {"font_size": 15, "color": 0xFFFAC434},
    "Label::desc": {"font_size": 12, "color": 0xFF909090},
    "Button::demo": {
        "background_color": 0xFF2D2D5E,
        "border_radius": 5,
        "margin": 2,
        "padding": 6,
    },
    "Button::demo:hovered": {"background_color": 0xFF3D3D7E},
    "Button::tool": {
        "background_color": 0xFF16213E,
        "border_radius": 5,
        "margin": 2,
        "padding": 6,
    },
    "Button::tool:hovered": {"background_color": 0xFF1A3A5C},
    "CollapsableFrame": {
        "background_color": 0xFF16213E,
        "secondary_color": 0xFF0F3460,
        "border_radius": 6,
        "margin": 4,
        "padding": 6,
    },
    "Separator": {"color": 0xFF333366},
}

# ---------------------------------------------------------------------------
# Interactive demos — launched via the Isaac Sim Examples Browser
# Each entry: (display_name, browser_example_name, browser_category)
# Names must match exactly what isaacsim.examples.interactive registers.
# ---------------------------------------------------------------------------
DEMO_CATEGORIES = {
    "Manipulation": [
        ("Franka Pick & Place", "Franka Pick Place", "Manipulation"),
        ("Follow Target", "Follow Target", "Manipulation"),
        ("Path Planning", "Path Planning", "Manipulation"),
        ("Bin Filling (UR10)", "Bin Filling", "Manipulation"),
        ("Simple Stack", "Simple Stack", "Manipulation"),
    ],
    "Locomotion & Policy": [
        ("Spot Quadruped", "Quadruped", "Policy"),
        ("Unitree H1 Humanoid", "Humanoid", "Policy"),
        ("Kaya Gamepad", "Kaya Gamepad", "Input Devices"),
    ],
    "Cortex Behaviors": [
        ("UR10 Palletizing", "UR10 Palletizing", "Cortex"),
        ("Franka Cortex", "Franka Cortex Examples", "Cortex"),
    ],
    "Multi-Robot": [
        ("Robo Factory", "RoboFactory", "Multi-Robot"),
        ("Robo Party", "RoboParty", "Multi-Robot"),
    ],
}

# ---------------------------------------------------------------------------
# Tool windows — opened via ui.Workspace.show_window
# Each entry: (display_name, window_title_to_show)
# ---------------------------------------------------------------------------
TOOL_CATEGORIES = {
    "Robot Setup": [
        ("Robot Assembler", "Robot Assembler"),
        ("Robot Wizard", "Robot Wizard [Beta]"),
        ("Gain Tuner", "Gain Tuner"),
        ("Grasp Editor", "Grasp Editor"),
        ("Robot Description Editor", "Robot Description Editor"),
    ],
    "Sensors": [
        ("Camera Inspector", "Camera Inspector"),
        ("Physics Inspector", "Physics Inspector"),
        ("Synthetic Data Recorder", "Synthetic Data Recorder"),
    ],
}


def _find_and_execute_example(browser, example_name, category):
    """Search the browser model for a registered example and execute it.

    The examples browser stores registered examples internally via
    register_example(). We walk the model to find the matching example
    and call its execute_entrypoint callback.
    """
    # The browser model stores Example objects. Try common internal paths.
    model = getattr(browser, "_browser_model", None)
    if model is None:
        return False

    # model._examples is typically dict[category -> dict[name -> Example]]
    examples_dict = getattr(model, "_examples", None)
    if examples_dict and isinstance(examples_dict, dict):
        cat_dict = examples_dict.get(category, {})
        example = cat_dict.get(example_name)
        if example is not None:
            entrypoint = getattr(example, "execute_entrypoint", None)
            if callable(entrypoint):
                entrypoint()
                return True

    # Fallback: iterate all examples if stored as a flat list
    all_examples = getattr(model, "_all_examples", getattr(model, "examples", None))
    if all_examples and hasattr(all_examples, "__iter__"):
        for ex in all_examples:
            if getattr(ex, "name", None) == example_name:
                entrypoint = getattr(ex, "execute_entrypoint", None)
                if callable(entrypoint):
                    entrypoint()
                    return True

    return False


class NwavesRoboticsWindow(ui.Window):
    """Centralized hub for Isaac Sim robotics demos and tools."""

    def __init__(self, title, **kwargs):
        super().__init__(title, **kwargs)
        self.deferred_dock_in("Content", ui.DockPolicy.CURRENT_WINDOW_IS_ACTIVE)
        self.frame.set_build_fn(self._build_ui)

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def _build_ui(self):
        with self.frame:
            with ui.ScrollingFrame(
                horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
                style_type_name_override="TreeView",
            ):
                with ui.VStack(spacing=6, style=STYLE):
                    ui.Spacer(height=4)

                    # Header
                    with ui.VStack(spacing=2, height=48):
                        ui.Spacer(height=4)
                        with ui.HStack():
                            ui.Spacer(width=12)
                            ui.Label("Nwaves.ai Robotics", name="header")
                        with ui.HStack():
                            ui.Spacer(width=12)
                            ui.Label(
                                "AI-Powered Simulation Platform",
                                name="subheader",
                            )

                    ui.Separator(height=2)
                    ui.Spacer(height=2)

                    # --- Interactive Demos ---
                    with ui.HStack(height=20):
                        ui.Spacer(width=8)
                        ui.Label("INTERACTIVE DEMOS", name="category")

                    for cat_name, demos in DEMO_CATEGORIES.items():
                        self._build_demo_category(cat_name, demos)

                    ui.Spacer(height=6)
                    ui.Separator(height=2)
                    ui.Spacer(height=2)

                    # --- Tools ---
                    with ui.HStack(height=20):
                        ui.Spacer(width=8)
                        ui.Label("TOOLS", name="category")

                    for cat_name, tools in TOOL_CATEGORIES.items():
                        self._build_tool_category(cat_name, tools)

                    ui.Spacer(height=12)

    # ------------------------------------------------------------------
    # Builders
    # ------------------------------------------------------------------
    def _build_demo_category(self, name, demos):
        with ui.CollapsableFrame(name, height=0, collapsed=False):
            with ui.VStack(spacing=3):
                for display_name, browser_name, browser_category in demos:
                    ui.Button(
                        display_name,
                        name="demo",
                        height=30,
                        clicked_fn=lambda bn=browser_name, bc=browser_category: self._launch_demo(
                            bn, bc
                        ),
                        tooltip=f"Launch '{browser_name}' ({browser_category})",
                    )

    def _build_tool_category(self, name, tools):
        with ui.CollapsableFrame(name, height=0, collapsed=False):
            with ui.VStack(spacing=3):
                for display_name, window_title in tools:
                    ui.Button(
                        display_name,
                        name="tool",
                        height=30,
                        clicked_fn=lambda wt=window_title: self._open_tool(wt),
                        tooltip=f"Open {window_title}",
                    )

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    @staticmethod
    def _launch_demo(example_name, category):
        """Launch an interactive demo through the Examples Browser."""
        try:
            from isaacsim.examples.browser import get_instance as get_browser

            browser = get_browser()
            if browser is None:
                carb.log_warn("[nwaves.ai.robotics] Examples Browser not ready")
                return

            if _find_and_execute_example(browser, example_name, category):
                carb.log_info(
                    f"[nwaves.ai.robotics] Launched: {example_name} ({category})"
                )
                return

            # Could not find it programmatically — open the browser window
            carb.log_info(
                f"[nwaves.ai.robotics] Opening Examples Browser for: {example_name}"
            )
            ui.Workspace.show_window("Isaac Sim Example Browser", True)

        except Exception as e:
            carb.log_warn(f"[nwaves.ai.robotics] Error launching {example_name}: {e}")
            ui.Workspace.show_window("Isaac Sim Example Browser", True)

    @staticmethod
    def _open_tool(window_title):
        """Open an Isaac Sim tool window by its registered title."""
        try:
            ui.Workspace.show_window(window_title, True)
            carb.log_info(f"[nwaves.ai.robotics] Opened: {window_title}")
        except Exception as e:
            carb.log_warn(f"[nwaves.ai.robotics] Could not open {window_title}: {e}")

    def destroy(self):
        super().destroy()
