# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

"""Tests for the gamepad's device viewer layer, against a fake pane."""

# Microdrop package imports.
from device_viewer.consts import LAYER_CONTRACT_VERSION, IDeviceViewerLayer

# Microdrop utils imports.
from microdrop_utils.pyface_helpers import StatusBarManager

# Local imports.
from .fakes import RecordingStepping


def _mounted(plugin, context):
    """Build the layer the way the device viewer does, then load a device."""
    (factory,) = plugin.layers
    layer = factory()

    layer.attach(context)
    layer.on_device_loaded(context.model.electrodes)

    return layer


def test_the_plugin_contributes_one_layer_on_the_current_contract(plugin):
    (factory,) = plugin.layers
    layer = factory()

    assert isinstance(layer, IDeviceViewerLayer)
    assert layer.id == "gamepad"
    assert layer.plugin is plugin
    # Fails when Microdrop moves the contract: re-verify, then bump the
    # plugin's LAYER_CONTRACT_VERSION_BUILT_AGAINST.
    assert layer.contract_version == LAYER_CONTRACT_VERSION


def test_attach_shows_the_icon_before_any_device(plugin, context, fake_pygame):
    (factory,) = plugin.layers
    layer = factory()

    layer.attach(context)

    assert plugin.status_bar_icons == [layer.status_icon]
    assert plugin.live_layer is layer
    assert layer.service is None
    assert layer.status_icon.toolTip() == "Gamepad disconnected"

    layer.detach()


def test_the_first_device_load_starts_the_gamepad(plugin, context, fake_pygame):
    layer = _mounted(plugin, context)

    assert layer.service.stepping is context.stepping
    assert layer.service._pygame_timer.isActive()
    assert layer.status_icon.toolTip() == "Fake Pad"

    layer.detach()


def test_a_new_device_swaps_the_stepping_and_keeps_one_timer(
    plugin, context, fake_pygame
):
    layer = _mounted(plugin, context)
    service, timer = layer.service, layer.service._pygame_timer

    context.stepping = RecordingStepping()
    layer.on_device_loaded(context.model.electrodes)

    assert layer.service is service
    assert layer.service._pygame_timer is timer
    assert layer.service.stepping is context.stepping

    layer.service._handle_pygame_hat((-1, 0))

    assert context.stepping.calls[-1] == ("step", "left")

    layer.detach()


def test_detach_stops_polling_and_withdraws_everything(plugin, context, fake_pygame):
    layer = _mounted(plugin, context)
    timer = layer.service._pygame_timer

    layer.detach()

    assert not timer.isActive()
    assert plugin.status_bar_icons == []
    assert plugin.live_layer is None
    assert layer.service is None
    assert layer.context is None


def test_without_pygame_the_layer_mounts_inert(plugin, context, no_pygame):
    layer = _mounted(plugin, context)

    assert layer.service._pygame_timer is None
    assert layer.status_icon.toolTip() == "Gamepad disconnected"

    layer.detach()

    assert plugin.status_bar_icons == []


def test_a_status_bar_created_after_mounting_reaches_the_service(
    plugin, context, fake_pygame
):
    layer = _mounted(plugin, context)

    context.status_bar_manager = StatusBarManager(messages=["Free Mode"])
    layer.service._set_hud("Pad: MOVE up")

    assert layer.service.status_bar_manager is context.status_bar_manager
    assert "Pad: MOVE up" in context.status_bar_manager.messages

    layer.detach()
