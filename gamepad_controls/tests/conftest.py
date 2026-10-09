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
import sys

# Third-party imports.
import pytest

# Enthought library imports.
from apptools.preferences.api import Preferences
from pyface.qt.QtWidgets import QApplication, QGraphicsView

# Microdrop package imports.
from device_viewer.consts import LayerContext
from gamepad_controls.plugin import GamepadControlsPlugin
from gamepad_controls.services import gamepad_interaction_service

# Local imports.
from .fakes import FakeModel, FakePygame, RecordingStepping


@pytest.fixture(scope="session", autouse=True)
def qapp():
    """A QApplication for the Qt timers and widgets the plugin creates."""
    return QApplication.instance() or QApplication([])


@pytest.fixture
def preferences():
    """An in-memory preferences root; ``flush`` writes nothing."""
    return Preferences()


@pytest.fixture
def fake_pygame(monkeypatch):
    """pygame with one controller plugged in, no events queued."""
    fake = FakePygame(joystick_count=1)
    monkeypatch.setattr(gamepad_interaction_service, "pygame", fake)

    return fake


@pytest.fixture
def no_pygame(monkeypatch):
    """A machine where ``import pygame`` fails."""
    monkeypatch.setattr(gamepad_interaction_service, "pygame", None)
    monkeypatch.setitem(sys.modules, "pygame", None)


@pytest.fixture
def context(preferences):
    """What the device viewer pane hands a layer, minus the scene."""
    return LayerContext(
        model=FakeModel(),
        device_view=QGraphicsView(),
        preferences=preferences,
        stepping=RecordingStepping(),
    )


@pytest.fixture
def plugin():
    """The plugin, unattached: its contribution lists are plain lists."""
    return GamepadControlsPlugin()
