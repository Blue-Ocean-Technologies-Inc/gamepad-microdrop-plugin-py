# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

"""Smoke tests for the gamepad_controls packaging.

They guard what packaging must get right: the manifest parses and points at
the plugin class, and importing the plugin module never imports pygame (a
disabled plugin group must not load SDL).
"""

# Standard library imports.
import sys
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_manifest_declares_the_ui_group_and_plugin():
    manifest = tomllib.loads((REPO_ROOT / "microdrop_plugin.toml").read_text())

    assert manifest["name"] == "gamepad"
    assert manifest["packages"] == ["gamepad_controls"]

    [group] = manifest["groups"]
    assert group["name"] == "gamepad_ui"
    assert group["plugins"] == ["gamepad_controls.plugin:GamepadControlsPlugin"]


def test_plugin_module_imports_without_loading_pygame():
    assert "pygame" not in sys.modules, "pygame already loaded by another test"

    from gamepad_controls.plugin import GamepadControlsPlugin

    assert "pygame" not in sys.modules

    plugin = GamepadControlsPlugin()
    assert plugin.id == "gamepad_controls.plugin"
    assert plugin.name == "Gamepad Controls Plugin"
