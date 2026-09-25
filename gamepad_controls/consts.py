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

# No topics are published or subscribed yet: the gamepad interaction logic
# has not moved out of Microdrop's device_viewer into this plugin (see
# AGENTS.md and issues #622/#650). Populated once that migration lands.
ACTOR_TOPIC_DICT = {}
