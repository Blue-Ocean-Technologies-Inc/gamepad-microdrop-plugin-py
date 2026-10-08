# gamepad-microdrop-plugin

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)
[![Template](https://img.shields.io/badge/template-microdrop--plugin--template%40v0.1.1-blue)](https://github.com/Blue-Ocean-Technologies-Inc/microdrop-plugin-template)

MicroDrop gamepad plugin, packaged as an installable conda package:

- `gamepad_controls/` — frontend-only: device-viewer electrode
  selection/stepping driven by a game controller. No backend group —
  installing this package is what brings `pygame` in.

`microdrop_plugin.toml` declares the single toggleable plugin group
(`gamepad_ui`); MicroDrop discovers it through the `microdrop.plugins` entry
point. See `docs/PLUGIN_DEVELOPMENT.md` in the MicroDrop source tree for the
plugin model.

## What it does

Adds a game controller to Microdrop's device viewer, as a device viewer
layer (`DEVICE_VIEWER_LAYERS`, layer contract 0.2.0):

- D-pad: step the actuated electrodes (hold B: split, Y: add, X: remove)
- A: clear all electrodes; Select: find liquid; Start: toggle realtime mode
- a joystick icon in the status bar shows the controller state
- the **Gamepad** preferences tab remaps buttons (Rebind captures the next
  press) and sets the debounce timings; `MICRODROP_GAMEPAD_*` environment
  variables still override the stored values

Needs a Microdrop whose device viewer provides layer contract 0.2.0 (the
release that removed its built-in gamepad, #783). With any other contract
version Microdrop logs a warning and mounts the layer anyway. Gamepad
settings saved by an older Microdrop move onto this plugin's preferences node
(`microdrop.gamepad_controls`) the first time Microdrop's device viewer starts
(Microdrop releases carrying #783 or later).

To get the gamepad back after upgrading Microdrop, open **Browse Plugins**,
install `gamepad-microdrop-plugin` from the `microdrop-plugins` channel, and
enable the `gamepad_ui` group. That group toggle replaces the old
`gamepad_enabled` preference.

## Build

```bash
pixi build
```

(uses `pixi-build-python`; the wheel force-includes the manifest as package
data of `gamepad_controls`).
