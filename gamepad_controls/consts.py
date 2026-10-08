# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

"""Constants for the gamepad_controls plugin."""

# This module's package.
PKG = ".".join(__name__.split(".")[:-1])
PKG_name = PKG.title().replace("_", " ")

# Preferences node of this plugin. Microdrop's device viewer moves the
# gamepad_* keys it used to own onto this node once (#783), so this must
# equal device_viewer.consts.GAMEPAD_PLUGIN_PREFERENCES_PATH.
PREFERENCES_PATH = "microdrop.gamepad_controls"

# ---------------------------------------------------------------------------
# Gamepad defaults (editable on the Gamepad preferences tab). Env vars of the
# form MICRODROP_GAMEPAD_* still override the stored preference at runtime.
# Button indices are for the common NES/SNES-style USB pad:
#   X=0, A=1, B=2, Y=3, L=4, R=5, Select=8, Start=9
# ---------------------------------------------------------------------------
GAMEPAD_BTN_CLEAR = 1  # A      -> clear all electrodes
GAMEPAD_BTN_FIND = 8  # Select -> find liquid
GAMEPAD_BTN_SPLIT = 2  # B hold -> split
GAMEPAD_BTN_ADD = 3  # Y hold -> add electrode
GAMEPAD_BTN_REMOVE = 0  # X hold -> remove electrode
GAMEPAD_BTN_REALTIME = 9  # Start  -> toggle realtime mode

GAMEPAD_DEBOUNCE_MOVE_SPLIT_S = 0.7  # D-pad move / split step debounce
GAMEPAD_DEBOUNCE_ADD_REMOVE_S = 0.3  # D-pad add / remove debounce
GAMEPAD_DEBOUNCE_FIND_S = 2.0  # find-liquid button debounce
GAMEPAD_DEBOUNCE_REALTIME_S = 0.4  # realtime-toggle button debounce
GAMEPAD_AXIS_THRESHOLD = 0.6  # analog-stick-as-D-pad activation threshold

# Poll cadence: ~100 Hz only while a controller is attached; with none,
# a slow tick suffices to catch JOYDEVICEADDED hot-plug events instead
# of waking the GUI thread 100x a second for nothing.
GAMEPAD_POLL_INTERVAL_MS = 10
GAMEPAD_IDLE_POLL_INTERVAL_MS = 500

# How long the Gamepad tab shows its capture / reconnect prompt. A capture
# waits ~10 s for a press; a reconnect's result shows on the status-bar icon.
CAPTURE_PROMPT_TIMEOUT_MS = 11000
RECONNECT_PROMPT_TIMEOUT_MS = 2500

# The gamepad publishes dropbot_controller topics (DETECT_DROPLETS,
# SET_REALTIME_MODE) and subscribes to none.
ACTOR_TOPIC_DICT = {}
