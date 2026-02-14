import weakref

import carb
import omni.ext
import omni.ui as ui
from omni.kit.menu.utils import MenuItemDescription, add_menu_items, remove_menu_items

from .window import NwavesRoboticsWindow

WINDOW_TITLE = "Nwaves.ai Robotics"

_extension_instance = None


class NwavesRoboticsExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        self._ext_id = ext_id
        self._window = None

        ui.Workspace.set_show_window_fn(WINDOW_TITLE, self._show_window)

        self._menu_items = [
            MenuItemDescription(
                name="Nwaves.ai Robotics",
                onclick_fn=lambda *_: ui.Workspace.show_window(WINDOW_TITLE, True),
            )
        ]
        add_menu_items(self._menu_items, "Window")

        # Show window on startup
        ui.Workspace.show_window(WINDOW_TITLE, True)

        global _extension_instance
        _extension_instance = self

        carb.log_info("[nwaves.ai.robotics] Extension started")

    def on_shutdown(self):
        remove_menu_items(self._menu_items, "Window")
        if self._window:
            self._window.destroy()
            self._window = None

        ui.Workspace.set_show_window_fn(WINDOW_TITLE, None)

        global _extension_instance
        _extension_instance = None

        carb.log_info("[nwaves.ai.robotics] Extension shutdown")

    def _show_window(self, visible):
        if visible:
            if self._window is None:
                self._window = NwavesRoboticsWindow(WINDOW_TITLE, width=420, height=700)
            self._window.visible = True
        elif self._window:
            self._window.visible = False


def get_instance():
    return _extension_instance
