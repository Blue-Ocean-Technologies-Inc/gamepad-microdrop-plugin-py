# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

# Enthought library imports.
from envisage.api import Plugin
from traits.api import Instance, List

# Microdrop package imports.
from device_viewer.consts import DEVICE_VIEWER_LAYERS
from microdrop_status_bar.consts import STATUS_BAR_ICONS

# Local imports.
from .consts import PKG, PKG_name


class GamepadControlsPlugin(Plugin):
    """Drive the device viewer's electrode cursor from a game controller.

    Contributes the gamepad layer to the device viewer and, while that layer
    is mounted, its joystick status-bar icon. pygame loads on the layer's
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

    #: The layer mounted on the device viewer; None while none is.
    live_layer = Instance("gamepad_controls.layer.GamepadLayer")

    def _layers_default(self):
        return [self._build_layer]

    def _build_layer(self):
        from .layer import GamepadLayer

        return GamepadLayer(plugin=self)
