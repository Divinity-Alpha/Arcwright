# Arcwright — Known Issues

**Version:** 1.0.3
**Last Updated:** 2026-03-28

---

## Active Issues

### Black screen on new levels (workaround available)
**Affects:** All new projects, v1.0.2+
**What happens:** New blank levels have no lighting. PIE shows a completely black screen.
**Workaround:** Create a lighting Blueprint manually at the start of every new session:
1. `create_blueprint` with SkyLight + DirectionalLight components
2. Set SkyLight intensity to 3.0, DirectionalLight intensity to 10.0
3. Spawn the Blueprint at (0, 0, 500)
4. See `docs/skills/SKILL_001_level_lighting.md` for full steps

**Fix:** v1.0.4 — `setup_default_lighting` command (outdoor/indoor/dark modes)

### Screenshots capture editor viewport, not PIE (workaround available)
**Affects:** All screenshot usage during PIE, v1.0.2+
**What happens:** `take_screenshot` captures the editor wireframe view instead of the game window.
**Workaround:** Wait a minimum of 5 seconds after `play_in_editor` before calling `take_screenshot`. Never screenshot within 5 seconds of PIE start.

**Fix:** v1.0.4 — auto-detects PIE viewport

### PIE returns before fully loaded
**Affects:** PIE testing workflow, v1.0.2+
**What happens:** `play_in_editor` returns success before the PIE session is fully loaded. Immediate commands against PIE may fail or return stale data.
**Workaround:** Add a delay after `play_in_editor` before interacting with the PIE session.

**Fix:** v1.0.4 — `wait_for_ready` parameter on `play_in_editor`

### Console command parameter conflict
**Affects:** `run_console_command`, v1.0.2+
**What happens:** Some console commands silently fail due to an internal parameter name conflict.
**Workaround:** None currently available for affected commands.

**Fix:** v1.0.4

### Light properties not always applied to spawned actors
**Affects:** Spawned light actors, v1.0.2+
**What happens:** `set_actor_property` for intensity and color on spawned lights may not take effect.
**Workaround:** Set light properties via Blueprint component properties before spawning, rather than on the placed actor.

**Fix:** v1.0.4

### verify_all_blueprints may report false clean
**Affects:** Blueprint verification, v1.0.2+
**What happens:** `verify_all_blueprints` sometimes reports 0 errors when compile errors exist.
**Workaround:** Cross-check with `get_message_log` and `get_output_log` after compilation.

**Fix:** v1.0.4

---

## Best Practices (Not Bugs)

These are correct behaviors that require specific usage patterns:

| Topic | Rule |
|---|---|
| Component properties | Always `compile_blueprint` before `set_component_property`. Properties set before first compile silently fail. |
| Default event nodes | Never recreate BeginPlay/Overlap/Tick via `add_nodes_batch`. Wire directly to `node_0`/`node_1`/`node_2`. |
| Blueprint spawning | Always use the `_C` suffix: `/Game/Path/BP_Name.BP_Name_C`. Without it, Blueprint logic won't run. |
| Widget colors | Always use `hex:#RRGGBB` prefix. Arcwright auto-converts sRGB to linear. |
| Save frequently | Call `save_all` after every meaningful change. UE crashes lose unsaved work. |
| Compile before PIE | Always `compile_blueprint` before `play_in_editor`. Uncompiled changes don't appear in PIE. |
| Check before create | Always `find_assets` before `create_blueprint`. Overwriting existing assets can corrupt them. |
| Verify with read-back | After every action, read back from UE to confirm. Don't trust the command response alone. |

See `docs/ARCWRIGHT_AI_GUIDE.md` for full details on all best practices.

---

## Planned Fixes

### v1.0.4 — Stability + Power Release
- Fix `setup_scene_lighting` hardcoded intensity (F001)
- Fix `take_screenshot` to use PIE viewport (F002)
- Add `wait_for_ready` to `play_in_editor` (F003)
- Fix `run_console_command` parameter conflict (F004)
- Fix `set_actor_property` for light properties (F005)
- Fix `verify_all_blueprints` false positives (F006)
- New: `setup_default_lighting` command
- New: `set_view_mode` command
- New: `get_build_errors` command
- New: `batch_spawn_actors`
- New: `set_level_post_process`
- New: `teleport_player_smooth`

---

## Resolved Issues

### v1.0.3 (2026-03-28)

**F008 — Editor crash on bad asset path (P0)**
Any invalid asset path previously crashed UE5 entirely. Now returns a clean error response. ~110 asset loading calls protected with null checks and path sanitization.

**F007 — LightColor hex: prefix on components**
`hex:#RRGGBB` now works correctly for `LightColor` on all light component types (PointLight, SpotLight, DirectionalLight). Also accepts `LightColor` in PascalCase. Also accepts JSON `{r,g,b}` objects.

**F009 — get_actor_properties param flexibility**
Now accepts `actor_name`, `label`, `name`, or `actor_label`. Previously only accepted `actor_label`.
