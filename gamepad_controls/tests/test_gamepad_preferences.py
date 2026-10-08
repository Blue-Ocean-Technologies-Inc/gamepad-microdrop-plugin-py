# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

"""Tests for the Gamepad preferences tab."""

# Third-party imports.
import pytest

# Microdrop package imports.
from gamepad_controls.preferences import GamepadPreferences, GamepadPreferencesPane

#: The keys the device viewer moves onto this plugin's node (#783).
MOVED_KEYS = [
    "gamepad_btn_clear",
    "gamepad_btn_find",
    "gamepad_btn_split",
    "gamepad_btn_add",
    "gamepad_btn_remove",
    "gamepad_btn_realtime",
    "gamepad_debounce_move_split",
    "gamepad_debounce_add_remove",
    "gamepad_debounce_find",
    "gamepad_debounce_realtime",
    "gamepad_axis_threshold",
]


@pytest.fixture
def requests():
    return []


@pytest.fixture
def pane(preferences, requests):
    pane = GamepadPreferencesPane(
        model=GamepadPreferences(preferences=preferences),
        request_button_capture=lambda action: requests.append(("capture", action)),
        request_reconnect=lambda: requests.append(("reconnect", None)),
    )

    # What the preferences dialog does: edit a disconnected copy.
    pane.trait_context()

    return pane


def test_the_preferences_live_on_the_plugin_node_under_their_old_names(preferences):
    helper = GamepadPreferences(preferences=preferences)
    persisted = [
        name for name in helper.trait_names() if helper._is_preference_trait(name)
    ]

    assert helper.preferences_path == "microdrop.gamepad_controls"
    assert sorted(persisted) == sorted(MOVED_KEYS)


def test_rebind_asks_the_live_gamepad_for_a_capture(pane, requests):
    pane._model.rebind_split = True

    assert requests == [("capture", "split")]
    assert "assign to 'split'" in pane._model.capture_prompt_


def test_reconnect_asks_the_live_gamepad_to_reconnect(pane, requests):
    pane._model.reconnect_gamepad = True

    assert requests == [("reconnect", None)]
    assert "reconnect" in pane._model.capture_prompt_


def test_a_capture_made_while_the_dialog_is_open_survives_ok(pane, preferences):
    pane._model.rebind_split = True

    # The live gamepad stores the captured button through its own helper.
    GamepadPreferences(preferences=preferences).gamepad_btn_split = 11

    assert pane._model.gamepad_btn_split == 11
    assert pane._model.capture_prompt_ == ""

    pane.apply()

    assert GamepadPreferences(preferences=preferences).gamepad_btn_split == 11
