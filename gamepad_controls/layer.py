# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

"""The gamepad's device viewer layer (#783)."""

# Enthought library imports.
from pyface.qt.QtWidgets import QLabel
from traits.api import Instance, observe

# Microdrop package imports.
from device_viewer.consts import BaseDeviceViewerLayer

# Local imports.
from .consts import GAMEPAD_LAYER_ID, LAYER_CONTRACT_VERSION_BUILT_AGAINST
from .preferences import GamepadPreferences
from .services.gamepad_interaction_service import GamepadInteractionService
from .status_icon import build_gamepad_status_icon


class GamepadLayer(BaseDeviceViewerLayer):
    """Drive the device viewer's electrode cursor from a game controller.

    Adds no sidebar section, opacity rows, or modes. While attached it shows
    the joystick icon in the status bar; from the first device load it polls
    the controller and drives ``LayerContext.stepping``, the cursor the
    arrow keys move.
    """

    id = GAMEPAD_LAYER_ID

    contract_version = LAYER_CONTRACT_VERSION_BUILT_AGAINST

    #: The plugin that contributed this layer: holds the status-bar icon
    #: contribution and relays the Gamepad tab's requests to ``service``.
    plugin = Instance("gamepad_controls.plugin.GamepadControlsPlugin")

    #: This plugin's preferences node, on the pane's preferences root.
    preferences = Instance(GamepadPreferences)

    #: The joystick indicator; contributed to the status bar while attached.
    status_icon = Instance(QLabel)

    #: Polls the controller; built on the first device load.
    service = Instance(GamepadInteractionService)

    def attach(self, context):
        super().attach(context)

        self.preferences = GamepadPreferences(preferences=context.preferences)
        self.status_icon = build_gamepad_status_icon()

        self.plugin.status_bar_icons.append(self.status_icon)
        self.plugin.live_layer = self

    def on_device_loaded(self, electrodes):
        stepping = self.context.stepping

        if stepping is None:
            return

        # One poller for the pane's lifetime; a new device only brings a new
        # electrode cursor.
        if self.service is not None:
            self.service.stepping = stepping
            return

        self.service = GamepadInteractionService(
            model=self.context.model,
            device_view=self.context.device_view,
            preferences=self.preferences,
            stepping=stepping,
            status_bar_manager=self.context.status_bar_manager,
            gamepad_icon=self.status_icon,
        )

    def detach(self):
        if self.service is not None:
            self.service.cleanup()
            self.service = None

        if self.status_icon in self.plugin.status_bar_icons:
            self.plugin.status_bar_icons.remove(self.status_icon)

        self.status_icon = None

        if self.plugin.live_layer is self:
            self.plugin.live_layer = None

        # Stop the helper listening to the preferences node.
        self.preferences.preferences = None
        self.preferences = None

        super().detach()

    @observe("context:status_bar_manager")
    def _share_status_bar(self, event):
        """The window creates its status bar after the pane mounts layers."""
        if self.service is not None and self.context is not None:
            self.service.status_bar_manager = self.context.status_bar_manager
