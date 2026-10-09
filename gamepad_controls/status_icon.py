# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

"""The gamepad's joystick indicator for the app status bar."""

# Enthought library imports.
from pyface.qt.QtGui import QFont
from pyface.qt.QtWidgets import QLabel

# Microdrop package imports.
from microdrop_status_bar.consts import ICON_PRIORITY_LEFTMOST

# Microdrop style imports.
from microdrop_style.colors import GREY
from microdrop_style.fonts.fontnames import ICON_FONT_FAMILY
from microdrop_style.icon_styles import STATUSBAR_ICON_POINT_SIZE
from microdrop_style.icons.icons import ICON_JOYSTICK


def build_gamepad_status_icon():
    """Return the joystick glyph in its disconnected state.

    The gamepad service recolors it and sets its tooltip on controller
    connect / disconnect; the status bar places it leftmost.
    """
    font = QFont(ICON_FONT_FAMILY)
    font.setPointSize(STATUSBAR_ICON_POINT_SIZE)

    icon = QLabel(ICON_JOYSTICK)
    icon.setFont(font)
    icon.setStyleSheet(f"color: {GREY['lighter']};")
    icon.setToolTip("Gamepad disconnected")
    icon.status_bar_icon_priority = ICON_PRIORITY_LEFTMOST

    return icon
