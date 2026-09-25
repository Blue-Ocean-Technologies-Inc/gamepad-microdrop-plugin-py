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

# Local imports.
from .consts import PKG, PKG_name

# Logger import.
from logger.logger_service import get_logger

logger = get_logger(__name__)


class GamepadControlsPlugin(Plugin):
    """Envisage plugin for gamepad-driven device-viewer interaction controls.

    Scaffold only (issue #622): the gamepad interaction, electrode-stepping,
    and preference logic this plugin will own currently lives in Microdrop's
    ``device_viewer`` package (``services/gamepad_interaction_service.py``
    and related modules). It moves here once issue #650 (the device viewer's
    pluggable interaction-layer contract) lands, so it can be reimplemented
    against that contract instead of importing ``device_viewer`` internals
    directly, which ``.importlinter`` forbids.

    Until then, enabling this plugin's group starts an empty plugin: no
    dock panes, menus, or topics are contributed yet.
    """

    #: The plugin unique identifier.
    id = PKG + ".plugin"

    #: The plugin name (suitable for displaying to the user).
    name = f"{PKG_name} Plugin"

    def start(self):
        # Lazy import: pygame is this plugin's whole reason for existing as
        # a separate package (it is not a core MicroDrop dependency), so it
        # must never load just because this module was imported — only when
        # the gamepad_ui plugin group is actually enabled and started.
        import pygame  # noqa: F401 (imported for its SDL init side effect)

        logger.info(f"{PKG_name} plugin started (scaffold; see #622, #650).")

    def stop(self):
        logger.info(f"{PKG_name} plugin stopped.")
