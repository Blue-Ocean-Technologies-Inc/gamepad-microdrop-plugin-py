# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

"""Tests for the ported gamepad interaction service, without hardware."""

# Standard library imports.
import json
import sys

# Microdrop package imports.
from dropbot_controller.consts import DETECT_DROPLETS
from gamepad_controls.consts import GAMEPAD_BTN_FIND, GAMEPAD_POLL_INTERVAL_MS
from gamepad_controls.preferences import GamepadPreferences
from gamepad_controls.services import gamepad_interaction_service
from gamepad_controls.services.gamepad_interaction_service import (
    GamepadInteractionService,
)


def _service(context):
    return GamepadInteractionService(
        model=context.model,
        device_view=context.device_view,
        preferences=GamepadPreferences(preferences=context.preferences),
        stepping=context.stepping,
    )


def test_importing_the_service_leaves_pygame_unloaded():
    assert gamepad_interaction_service.pygame is None
    assert "pygame" not in sys.modules


def test_a_plugged_in_controller_is_polled_fast(fake_pygame, context):
    service = _service(context)

    assert service._pygame_enabled
    assert service._pygame_timer.interval() == GAMEPAD_POLL_INTERVAL_MS

    service.cleanup()


def test_without_pygame_the_service_stays_idle(no_pygame, context):
    service = _service(context)

    assert not service._pygame_enabled
    assert service._pygame_timer is None

    service.cleanup()


def test_the_d_pad_drives_the_shared_stepping(fake_pygame, context):
    service = _service(context)

    service._handle_pygame_hat((0, 1))

    assert context.stepping.calls[-1] == ("step", "up")

    service.cleanup()


def test_bindings_come_from_the_plugin_node_and_reload_live(fake_pygame, context):
    context.preferences.set("microdrop.gamepad_controls.gamepad_btn_clear", "4")
    service = _service(context)

    assert service._btn_clear == 4

    service.preferences.gamepad_btn_clear = 6

    assert service._btn_clear == 6

    service.cleanup()


def test_a_captured_button_is_stored_on_the_plugin_node(fake_pygame, context):
    service = _service(context)

    service.begin_button_capture("split")
    service._handle_pygame_button(11, pressed=True)

    assert service._btn_split == 11
    assert GamepadPreferences(preferences=context.preferences).gamepad_btn_split == 11

    service.cleanup()


def test_find_liquid_asks_for_droplets_on_every_channel(
    fake_pygame, context, monkeypatch
):
    published = []
    monkeypatch.setattr(
        gamepad_interaction_service,
        "publish_message",
        lambda topic, message: published.append((topic, message)),
    )
    context.model.electrodes.channels_electrode_ids_map = {3: ["e3"], 7: ["e7"]}
    service = _service(context)

    service._handle_pygame_button(GAMEPAD_BTN_FIND, pressed=True)

    assert published == [(DETECT_DROPLETS, json.dumps([3, 7]))]
    assert context.model.electrodes.cleared == 1

    service.cleanup()
