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

## Status

Scaffold only (issue #622). `GamepadControlsPlugin` is importable and its
group toggles cleanly, but it does not yet drive the device viewer: the
gamepad interaction, stepping, and preference logic currently lives in
Microdrop's `device_viewer` package and moves here once issue #650 (the
device viewer's pluggable interaction-layer contract) lands, so this plugin
can reimplement it without importing `device_viewer` internals.

## Build

```bash
pixi build
```

(uses `pixi-build-python`; the wheel force-includes the manifest as package
data of `gamepad_controls`).
