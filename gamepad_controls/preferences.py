# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

"""Gamepad preferences: the button mapping, timings, and the Gamepad tab."""

# Enthought library imports.
from apptools.preferences.api import PreferencesHelper
from envisage.ui.tasks.api import PreferencesCategory, PreferencesPane
from pyface.qt.QtCore import QTimer
from traits.api import Button, Callable, Instance, Range, Str, observe
from traitsui.api import Group, HGroup, Item, View

# Microdrop style imports.
from microdrop_style.text_styles import preferences_group_style_sheet

# Local imports.
from .consts import (
    CAPTURE_PROMPT_TIMEOUT_MS,
    GAMEPAD_AXIS_THRESHOLD,
    GAMEPAD_BTN_ADD,
    GAMEPAD_BTN_CLEAR,
    GAMEPAD_BTN_FIND,
    GAMEPAD_BTN_REALTIME,
    GAMEPAD_BTN_REMOVE,
    GAMEPAD_BTN_SPLIT,
    GAMEPAD_DEBOUNCE_ADD_REMOVE_S,
    GAMEPAD_DEBOUNCE_FIND_S,
    GAMEPAD_DEBOUNCE_MOVE_SPLIT_S,
    GAMEPAD_DEBOUNCE_REALTIME_S,
    PREFERENCES_PATH,
    RECONNECT_PROMPT_TIMEOUT_MS,
)

#: Each Rebind button and the gamepad action its capture binds.
REBIND_ACTIONS = {
    "rebind_clear": "clear",
    "rebind_find": "find",
    "rebind_split": "split",
    "rebind_add": "add",
    "rebind_remove": "remove",
    "rebind_realtime": "realtime",
}


class GamepadPreferences(PreferencesHelper):
    """The gamepad plugin's preferences node.

    The keys keep the names they had on the device viewer's node, so
    Microdrop's one-shot move (#783) copies them verbatim.
    """

    preferences_path = Str(PREFERENCES_PATH)

    #: Persisted button indices. MICRODROP_GAMEPAD_* env vars take
    #: precedence; SDL exposes up to 32 buttons.
    gamepad_btn_clear = Range(value=GAMEPAD_BTN_CLEAR, low=0, high=31, mode="spinner")
    gamepad_btn_find = Range(value=GAMEPAD_BTN_FIND, low=0, high=31, mode="spinner")
    gamepad_btn_split = Range(value=GAMEPAD_BTN_SPLIT, low=0, high=31, mode="spinner")
    gamepad_btn_add = Range(value=GAMEPAD_BTN_ADD, low=0, high=31, mode="spinner")
    gamepad_btn_remove = Range(value=GAMEPAD_BTN_REMOVE, low=0, high=31, mode="spinner")
    gamepad_btn_realtime = Range(
        value=GAMEPAD_BTN_REALTIME, low=0, high=31, mode="spinner"
    )

    #: Persisted debounce timings (seconds) and analog-stick threshold.
    gamepad_debounce_move_split = Range(
        value=GAMEPAD_DEBOUNCE_MOVE_SPLIT_S, low=0.0, high=3.0
    )
    gamepad_debounce_add_remove = Range(
        value=GAMEPAD_DEBOUNCE_ADD_REMOVE_S, low=0.0, high=3.0
    )
    gamepad_debounce_find = Range(value=GAMEPAD_DEBOUNCE_FIND_S, low=0.0, high=5.0)
    gamepad_debounce_realtime = Range(
        value=GAMEPAD_DEBOUNCE_REALTIME_S, low=0.0, high=5.0
    )
    gamepad_axis_threshold = Range(value=GAMEPAD_AXIS_THRESHOLD, low=0.1, high=1.0)

    #: Capture / reconnect feedback for the tab; the trailing underscore keeps
    #: it off the preferences node.
    capture_prompt_ = Str()

    #: Bind the next controller button press to an action. Events are never
    #: persisted; no trailing underscore, so the pane can observe them.
    rebind_clear = Button("Rebind")
    rebind_find = Button("Rebind")
    rebind_split = Button("Rebind")
    rebind_add = Button("Rebind")
    rebind_remove = Button("Rebind")
    rebind_realtime = Button("Rebind")

    #: Re-attempt controller acquisition after an unplug / replug.
    reconnect_gamepad = Button("Reconnect controller")


gamepad_tab = PreferencesCategory(
    id=f"{PREFERENCES_PATH}.preferences",
    name="Gamepad",
    after="microdrop.device_viewer.preferences",
)


def _gamepad_button_row(trait_name, rebind_trait, label):
    """A button-index spinner paired with its live 'Rebind' capture button."""
    return HGroup(
        Item(trait_name, label=label),
        Item(
            rebind_trait,
            show_label=False,
            tooltip="Press, then press a button on the gamepad",
        ),
    )


gamepad_settings = Group(
    Group(
        HGroup(
            Item("capture_prompt_", style="readonly", show_label=False, springy=True),
            Item(
                "reconnect_gamepad",
                show_label=False,
                tooltip=(
                    "Re-attempt connection after unplugging/replugging the controller"
                ),
            ),
        ),
        _gamepad_button_row("gamepad_btn_clear", "rebind_clear", "Clear all (A)"),
        _gamepad_button_row("gamepad_btn_find", "rebind_find", "Find liquid (Select)"),
        _gamepad_button_row("gamepad_btn_split", "rebind_split", "Split — hold (B)"),
        _gamepad_button_row("gamepad_btn_add", "rebind_add", "Add — hold (Y)"),
        _gamepad_button_row("gamepad_btn_remove", "rebind_remove", "Remove — hold (X)"),
        _gamepad_button_row(
            "gamepad_btn_realtime", "rebind_realtime", "Realtime toggle (Start)"
        ),
        label="Button mapping",
        show_border=True,
    ),
    Group(
        Item("gamepad_debounce_move_split", label="Move / split (s)"),
        Item("gamepad_debounce_add_remove", label="Add / remove (s)"),
        Item("gamepad_debounce_find", label="Find liquid (s)"),
        Item("gamepad_debounce_realtime", label="Realtime toggle (s)"),
        Item("gamepad_axis_threshold", label="Analog-stick threshold"),
        label="Timing & sensitivity",
        show_border=True,
    ),
    label="Gamepad",
    show_border=True,
    style_sheet=preferences_group_style_sheet,
)


class GamepadPreferencesPane(PreferencesPane):
    """The Gamepad tab: button mapping with live rebinding, and timings.

    The dialog edits ``_model``, a disconnected copy of ``model``; OK copies
    it back. Rebind and Reconnect go to the live gamepad through the two
    callables the plugin hands in.
    """

    model_factory = GamepadPreferences

    category = gamepad_tab.id

    #: Arm a capture on the live gamepad: ``request_button_capture(action)``.
    request_button_capture = Callable()

    #: Re-attempt controller acquisition on the live gamepad.
    request_reconnect = Callable()

    #: Clears a prompt whose outcome writes no binding (timeout, reconnect).
    _prompt_timer = Instance(QTimer)

    view = View(
        Item("_"),
        gamepad_settings,
        Item("_"),
        resizable=True,
    )

    @observe(
        "_model:[rebind_clear,rebind_find,rebind_split,rebind_add,rebind_remove,"
        "rebind_realtime]"
    )
    def _request_capture(self, event):
        action = REBIND_ACTIONS[event.name]

        self._show_prompt(
            f"Press a gamepad button to assign to '{action}'… "
            f"(no press within ~10s cancels)",
            CAPTURE_PROMPT_TIMEOUT_MS,
        )
        self.request_button_capture(action)

    @observe("_model:reconnect_gamepad")
    def _request_reconnect(self, event):
        self._show_prompt(
            "Attempting to reconnect controller…", RECONNECT_PROMPT_TIMEOUT_MS
        )
        self.request_reconnect()

    @observe(
        "model:[gamepad_btn_clear,gamepad_btn_find,gamepad_btn_split,"
        "gamepad_btn_add,gamepad_btn_remove,gamepad_btn_realtime]"
    )
    def _mirror_captured_binding(self, event):
        """Show a binding the live gamepad stored in the open dialog.

        Without this, OK would copy the dialog's stale value back over the
        captured one.
        """
        if self._model is None:
            return

        setattr(self._model, event.name, event.new)
        self._show_prompt("", 0)

    def _show_prompt(self, text, timeout_ms):
        """Show ``text`` on the tab; a non-empty prompt clears itself."""
        if self._model is not None:
            self._model.capture_prompt_ = text

        if self._prompt_timer is None:
            self._prompt_timer = QTimer()
            self._prompt_timer.setSingleShot(True)
            self._prompt_timer.timeout.connect(lambda: self._show_prompt("", 0))

        if text:
            self._prompt_timer.start(timeout_ms)
        else:
            self._prompt_timer.stop()
