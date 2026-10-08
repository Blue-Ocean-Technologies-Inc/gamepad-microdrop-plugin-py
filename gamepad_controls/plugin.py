# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

# Standard library imports.
from functools import partial

# Enthought library imports.
from envisage.api import PREFERENCES_CATEGORIES, PREFERENCES_PANES, Plugin
from traits.api import Instance, List

# Microdrop package imports.
from device_viewer.consts import DEVICE_VIEWER_LAYERS
from microdrop_status_bar.consts import STATUS_BAR_ICONS

# Local imports.
from .consts import PKG, PKG_name

# Logger import.
from logger.logger_service import get_logger

logger = get_logger(__name__)


class GamepadControlsPlugin(Plugin):
    """Drive the device viewer's electrode cursor from a game controller.

    Contributes the gamepad layer to the device viewer, its joystick
    status-bar icon while that layer is mounted, and the Gamepad preferences
    tab. pygame loads on the layer's
    first device load, never on import, so a disabled group costs nothing.
    """

    #: The plugin unique identifier.
    id = PKG + ".plugin"

    #: The plugin name (suitable for displaying to the user).
    name = f"{PKG_name} Plugin"

    #: Zero-arg factory for the gamepad layer; the device viewer builds one
    #: layer per pane and detaches it when this plugin unloads.
    layers = List(contributes_to=DEVICE_VIEWER_LAYERS)

    #: The mounted layer's joystick icon; the layer adds and removes it.
    status_bar_icons = List(contributes_to=STATUS_BAR_ICONS)

    #: The Gamepad tab and its category.
    preferences_panes = List(contributes_to=PREFERENCES_PANES)
    preferences_categories = List(contributes_to=PREFERENCES_CATEGORIES)

    #: The layer mounted on the device viewer; None while none is.
    live_layer = Instance("gamepad_controls.layer.GamepadLayer")

    def _layers_default(self):
        return [self._build_layer]

    def _build_layer(self):
        from .layer import GamepadLayer

        return GamepadLayer(plugin=self)

    def _preferences_panes_default(self):
        from .preferences import GamepadPreferencesPane

        return [
            partial(
                GamepadPreferencesPane,
                request_button_capture=self.request_button_capture,
                request_reconnect=self.request_reconnect,
            )
        ]

    def _preferences_categories_default(self):
        from .preferences import gamepad_tab

        return [gamepad_tab]

    def request_button_capture(self, action):
        """Bind the live gamepad's next button press to ``action``."""
        service = self._live_service("button capture")

        if service is not None:
            service.begin_button_capture(action)

    def request_reconnect(self):
        """Have the live gamepad re-attempt controller acquisition."""
        service = self._live_service("reconnect")

        if service is not None:
            service.reconnect_gamepad()

    def _live_service(self, request):
        """Return the mounted layer's service, or log why ``request`` is dropped."""
        service = None if self.live_layer is None else self.live_layer.service

        if service is None:
            logger.info(
                f"Ignored gamepad {request} request: no gamepad layer is mounted"
            )

        return service
