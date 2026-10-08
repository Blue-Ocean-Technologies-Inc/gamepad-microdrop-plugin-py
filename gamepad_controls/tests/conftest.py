# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

# Third-party imports.
import pytest

# Enthought library imports.
from apptools.preferences.api import Preferences
from pyface.qt.QtWidgets import QApplication


@pytest.fixture(scope="session", autouse=True)
def qapp():
    """A QApplication for the Qt timers and widgets the plugin creates."""
    return QApplication.instance() or QApplication([])


@pytest.fixture
def preferences():
    """An in-memory preferences root; ``flush`` writes nothing."""
    return Preferences()
