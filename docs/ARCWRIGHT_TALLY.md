# Arcwright — Known Issues, Best Practices & Roadmap
## The Living Tally

**Version:** 1.0.3 (Current) — 1.0.2 (FAB pending update)
**Last Updated:** 2026-03-28
**Purpose:** Internal tracking + release planning + customer communication

---

## CATEGORY 1 — ARCWRIGHT FIXES
### Broken commands that need C++ fixes

| # | Command | What Breaks | User Experience | AI Experience | Fix Version | Status |
|---|---|---|---|---|---|---|
| F001 | setup_scene_lighting | Hardcodes intensity=2, ignores all params | New level is completely black. Day-one blocker. | AI calls with correct params, gets intensity=2 regardless | v1.0.3 | 🟢 FIXED (setup_default_lighting added) |
| F002 | take_screenshot | Captures editor viewport wireframe not PIE window | Screenshots are black or show editor chrome | AI reports taken but image is black | v1.0.3 | 🟢 FIXED (PIE viewport detection) |
| F003 | play_in_editor | Returns before PIE fully loaded | AI screenshots immediately, gets black result | AI calls play_in_editor, immediately screenshots, black | v1.0.3 | 🟢 FIXED (wait_for_ready param) |
| F004 | run_console_command | Param name conflicts, requires PIE | Console commands silently fail | AI uses as fallback, also fails | v1.0.3 | 🟢 FIXED (editor+PIE dual world) |
| F005 | set_component_property LightColor | hex: prefix not working on component light color | Light colors always wrong | AI sets hex:#4a9eff, color not applied | v1.0.3 | 🟢 FIXED |
| F006 | get_actor_properties | Only accepts actor_label param | AI cannot read back actor state | AI calls command, gets error | v1.0.3 | 🟢 FIXED |
| F007 | verify_all_blueprints | Only searches /Game/Arcwright/Generated/ | AI reports "all clean" but errors exist in other paths | AI trusts response without cross-checking | v1.0.3 | 🟢 FIXED (searches all /Game/) |
| F008 | ANY command with invalid path | Editor crashes on bad LoadObject | Typo crashes UE5, loses session work | Bad path kills editor, connection lost | v1.0.3 | 🟢 FIXED |

---

### F008 — P0 CRASH ON BAD INPUT
**Discovered:** Test suite Run 1, 2026-03-28
**Reproduction:** Call get_blueprint_details or compile_blueprint with a path that does not exist
**Result:** Editor crashes entirely — not an error response
**Impact:** Every user who makes a typo in any path can crash UE5 and lose their session
**Cascade:** In test suite, one crash caused 21 subsequent tests to fail (CONNECTION_REFUSED)
**Real stress test failure count:** 1 crash caused all 21 failures — not 21 separate bugs

**Root cause:** C++ asset loading code is not wrapped in null checks or try/catch.
A missing asset causes a null pointer dereference or unhandled assertion.

**Fix pattern — apply to every command that loads an asset:**
```cpp
UObject* Asset = LoadObject<UObject>(nullptr, *AssetPath);
if (!Asset)
{
    TSharedPtr<FJsonObject> Resp = MakeShareable(new FJsonObject);
    Resp->SetStringField(TEXT("status"), TEXT("error"));
    Resp->SetStringField(TEXT("error"), FString::Printf(
        TEXT("Asset not found: %s"), *AssetPath));
    return Resp;
}
// Only proceed if Asset is valid
```

**Commands requiring this fix (audit all of these):**
- get_blueprint_details
- compile_blueprint
- set_component_property
- add_component
- get_widget_tree
- set_widget_property
- add_widget_child
- get_data_table_rows
- add_data_table_row
- spawn_actor_at
- set_actor_property
- get_actor_properties
- All behavior tree commands
- All material commands
- All animation blueprint commands

**This must be fixed before any other v1.0.3 work.**

---

## CATEGORY 2 — BEST PRACTICES
### Commands that work but require specific AI behavior

| # | Topic | What Goes Wrong | User Experience | Correct Approach | Documented In | Status |
|---|---|---|---|---|---|---|
| P001 | Blueprint component property sequence | Setting properties before first compile silently fails | Components have wrong defaults. Colors white. Sizes wrong. | 1. add_component ALL 2. compile FIRST 3. set_component_property AFTER | SKILL_003 | 📋 CONFIRMED by test suite |
| P002 | Default event node recreation | Duplicate BeginPlay/Overlap/Tick = Event None | Blueprint logic never fires | Never add BeginPlay/Overlap/Tick via add_nodes_batch. Wire to node_0/1/2. | AI Guide §5.1 | 📋 DOCUMENTED |
| P003 | Blueprint _C suffix for spawning | Spawning without _C = plain actor, no BP logic | Spawned actors do nothing | Always use full path with _C suffix | AI Guide §5.1 | 📋 CONFIRMED by test suite |
| P004 | hex: color prefix | Colors without hex: look washed out | UI colors wrong | Always use hex:#RRGGBB prefix | AI Guide §5.2 | 📋 DOCUMENTED |
| P005 | Widget FillHeight totals | Values not totaling 1.0 | Widget layout breaks silently | FillHeight values must total exactly 1.0 | AI Guide §5.3 | 📋 DOCUMENTED |
| P006 | PIE screenshot 5-second delay | Screenshot too fast = black image | Screenshots unusable | Wait 5 seconds after play_in_editor | SKILL_002 | 📋 CONFIRMED by test suite |
| P007 | Lighting on new levels | No lighting = black everything | Scene is black in PIE | setup_default_lighting at session start | SKILL_001 | 📋 CONFIRMED by test suite |
| P008 | Content path format | Using filesystem paths instead of /Game/ | Asset not found errors | Always use /Game/ paths | AI Guide §6.5 | 📋 DOCUMENTED |
| P009 | Save after every change | Unsaved changes lost on crash | Work lost on UE5 crash | save_all after every meaningful change | AI Guide §5.5 | 📋 DOCUMENTED |
| P010 | Compile before PIE | Uncompiled changes not in PIE | AI sees old behavior in PIE | Always compile before play_in_editor | AI Guide §4.1 | 📋 DOCUMENTED |
| P011 | Check assets before creating | Overwriting existing asset corrupts it | Random BP corruption | find_assets before create_blueprint | AI Guide §3.2 | 📋 DOCUMENTED |
| P012 | Verify with read-back | Commands report success but silently fail | Build is wrong, AI doesn't know | After every action read back from UE to confirm | AI Guide §2.2 | 📋 DOCUMENTED |

---

## CATEGORY 3 — MISSING COMMANDS
### Capabilities that don't exist yet

| # | Missing Command | What AI Does Instead | User Experience | Target Version | Status |
|---|---|---|---|---|---|
| M001 | setup_default_lighting | Creates BP_Lighting actor manually (8+ steps) | Day-one blocker for every new project | v1.0.3 | 🟢 ADDED |
| M002 | set_view_mode | run_console_command (fails) | Cannot switch lit/unlit/wireframe | v1.0.3 | 🟢 ADDED |
| M003 | set_ambient_light | No workaround | Cannot control ambient lighting | v1.0.4 | 🔴 OPEN |
| M004 | play_in_editor wait_for_ready | Manual sleep(5) before every screenshot | Awkward timing, frequent black screenshots | v1.0.3 | 🟢 ADDED |
| M005 | get_build_errors | Parses raw output log manually | AI reads raw log, misses things | v1.0.3 | 🟢 ADDED |
| M006 | batch_spawn_actors | Loops spawn_actor_at one at a time | 20 actors = 20 round trips, slow | v1.0.4 | 🔴 OPEN |
| M007 | set_level_post_process | No workaround | Cannot set bloom/tone for cinematics | v1.0.4 | 🔴 OPEN |
| M008 | teleport_player_smooth | Hard cut only | Jarring in recordings | v1.0.4 | 🔴 OPEN |
| M009 | set_time_of_day | No workaround | Cannot demonstrate day/night | v1.0.4 | 🔴 OPEN |
| M010 | apply_material_by_name | Must know exact full asset path | AI guesses wrong paths | v1.0.4 | 🔴 OPEN |
| M011 | create_post_process_volume | No workaround | Advanced visual effects impossible | v1.0.4 | 🔴 OPEN |
| M012 | get_actor_screenshot | No per-actor capture | Cannot visually verify specific actor | v1.0.4 | 🔴 OPEN |


---

## TEST SUITE RESULTS HISTORY

### Run 3 — 2026-03-28 — v1.0.3 Final ✓ SHIPPED
**GPU:** RTX 5070 Ti (CUDA device 0) ✓
**Version:** 1.0.3
**Release:** https://github.com/Divinity-Alpha/Arcwright/releases/tag/v1.0.3

| Category | Tests | Passed | Failed | Warned |
|---|---|---|---|---|
| Regression | 36 | 36 | 0 | 0 |
| Stress | 26 | 25 | 0 | 1 |
| Discovery | 15 | 1 | 10 | 4 |
| **Total** | **77** | **62** | **10** | **5** |

Pass rate: 80.5% — all failures attributable to known open issues (F001-F004).
Regression 36/36 CLEAN. Stress 25/26 CLEAN (0 crashes, 0 timeouts). 
Discovery failures all cascade from PIE (F002/F003 — v1.0.4 scope).
F008/F005/F006 all verified passing.
Commits: 8308f35 (F008) · 2332dd3 (F005+F006)

---

### Run 2 — 2026-03-28 — Post F008 Fix
**Version:** 1.0.3-dev

| Category | Tests | Passed | Failed | Warned |
|---|---|---|---|---|
| Regression | 36 | 34 | 2 | 0 |
| Stress | 26 | 25 | 0 | 1 |
| Discovery | 15 | 1 | 10 | 4 |
| **Total** | **77** | **60** | **12** | **5** |

Stress: 21 failures → 0. F008 confirmed fixed.

---

### Run 1 — 2026-03-28 — Baseline v1.0.2

| Category | Tests | Passed | Failed | Warned |
|---|---|---|---|---|
| Regression | 36 | 34 | 2 | 0 |
| Stress | 26 | 5 | 21 | 0 |
| Discovery | 15 | 1 | 10 | 4 |
| **Total** | **77** | **42** | **31** | **4** |

21 stress failures = 1 P0 crash cascading (F008).
3 unique bugs found: F008 + F005 + F006.

---

## RELEASE PLANNING

### v1.0.3 — SHIPPED ✓ 2026-03-28
**GitHub:** https://github.com/Divinity-Alpha/Arcwright/releases/tag/v1.0.3

Fixed: F008 (crash on bad path) · F005 (LightColor hex) · F006 (get_actor_properties params)
Test results: Regression 36/36 · Stress 25/26 · Strict includes PASS

---

### v1.0.4 — Lighting + PIE Release
**Theme:** Fix remaining day-one blockers
**Target:** 6-8 weeks after v1.0.3
**Gate:** Discovery suite 12/15 or better

Priority fixes:
- F001/M001: setup_default_lighting (outdoor/indoor/dark modes)
- F002: take_screenshot — capture PIE viewport not editor viewport
- F003: play_in_editor — add wait_for_ready param
- F004: run_console_command — fix param name conflict
- M002: set_view_mode command
- M004: wait_for_pie_ready

New power features:
- M006: batch_spawn_actors
- M007: set_level_post_process
- M008: teleport_player_smooth
- M009: set_time_of_day
- M010: apply_material_by_name
- M011: create_post_process_volume
- M012: get_actor_screenshot

---

## CUSTOMER-FACING KNOWN ISSUES
**Public version:** github.com/Divinity-Alpha/Arcwright/docs/KNOWN_ISSUES.md

### Fixed in v1.0.3
- ✅ Editor crash on invalid asset path
- ✅ LightColor hex: prefix on components
- ✅ get_actor_properties param name

### Active Issues in v1.0.3

**Lighting on new blank levels**
New blank levels have no lighting — PIE and screenshots appear black.
Workaround: docs/skills/SKILL_001_level_lighting.md
Fix: v1.0.4 setup_default_lighting command

**PIE screenshots black if taken immediately**
Screenshots within 5 seconds of play_in_editor are black.
Workaround: wait 5 seconds after play_in_editor
Fix: v1.0.4 wait_for_ready param
