# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

"""Tests for the plugin's preferences contribution and its relays."""

# Microdrop package imports.
from gamepad_controls.preferences import GamepadPreferences


def test_the_plugin_adds_the_gamepad_tab(plugin):
    (category,) = plugin.preferences_categories

    assert category.name == "Gamepad"
    assert category.id == "microdrop.gamepad_controls.preferences"


def test_rebind_on_the_gamepad_tab_reaches_the_live_gamepad(
    plugin, context, fake_pygame
):
    (layer_factory,) = plugin.layers
    layer = layer_factory()
    layer.attach(context)
    layer.on_device_loaded(context.model.electrodes)

    (pane_factory,) = plugin.preferences_panes
    pane = pane_factory(dialog=None)
    pane.model = GamepadPreferences(preferences=context.preferences)
    pane.trait_context()

    pane._model.rebind_split = True

    assert layer.service._capture_action == "split"

    layer.detach()


def test_requests_with_no_gamepad_mounted_are_ignored(plugin):
    plugin.request_button_capture("split")
    plugin.request_reconnect()

    assert plugin.live_layer is None
