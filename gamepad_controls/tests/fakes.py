# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

"""Hardware-free stand-ins for pygame and the device viewer the gamepad drives."""

# Standard library imports.
from types import SimpleNamespace

# Enthought library imports.
from traits.api import Bool, Dict, HasTraits, Instance, Int, List, provides

# Microdrop package imports.
from device_viewer.consts import IElectrodeStepping


class FakeJoystick:
    """One attached controller with no button held."""

    def __init__(self, name="Fake Pad"):
        self.name = name
        self.initialised = False

    def init(self):
        self.initialised = True

    def get_init(self):
        return self.initialised

    def quit(self):
        self.initialised = False

    def get_name(self):
        return self.name

    def get_numhats(self):
        return 1

    def get_numaxes(self):
        return 2

    def get_button(self, index):
        return False


class FakeJoystickModule:
    """``pygame.joystick`` with ``count`` controllers plugged in."""

    def __init__(self, count):
        self.count = count
        self.initialised = False

    def init(self):
        self.initialised = True

    def quit(self):
        self.initialised = False

    def get_init(self):
        return self.initialised

    def get_count(self):
        return self.count

    def Joystick(self, index):  # noqa: N802 (pygame's name)
        return FakeJoystick()


class FakePygame:
    """The slice of pygame the gamepad service calls; no events arrive."""

    JOYAXISMOTION = 1536
    JOYHATMOTION = 1538
    JOYBUTTONDOWN = 1539
    JOYBUTTONUP = 1540
    JOYDEVICEADDED = 1541
    JOYDEVICEREMOVED = 1542

    def __init__(self, joystick_count=1):
        self.joystick = FakeJoystickModule(joystick_count)
        self.event = SimpleNamespace(get=lambda: [], pump=lambda: None)
        self.initialised = False

    def init(self):
        self.initialised = True

    def get_init(self):
        return self.initialised


@provides(IElectrodeStepping)
class RecordingStepping(HasTraits):
    """Records what the gamepad asked of the electrode cursor."""

    #: (action, direction) in call order.
    calls = List()

    def map_direction_for_device_rotation(self, direction):
        return direction

    def get_active_electrode_ids(self):
        return set()

    def step_active_electrodes(self, direction):
        self.calls.append(("step", direction))

    def extend_active_electrodes(self, direction):
        self.calls.append(("extend", direction))

    def shrink_active_electrodes(self, direction):
        self.calls.append(("shrink", direction))

    def split_step(self, direction):
        self.calls.append(("split", direction))

    def reset_split_state(self):
        self.calls.append(("reset", None))


class FakeElectrodes(HasTraits):
    """The ``Electrodes`` members the gamepad touches."""

    channels_electrode_ids_map = Dict()

    #: How often the gamepad cleared the actuated electrodes.
    cleared = Int(0)

    def clear_electrode_states(self):
        self.cleared += 1


class FakeModel(HasTraits):
    """The ``DeviceViewMainModel`` traits the gamepad reads."""

    electrodes = Instance(FakeElectrodes, ())
    connected = Bool(False)
    realtime_mode = Bool(False)
    device_rotation_deg = Int(0)
