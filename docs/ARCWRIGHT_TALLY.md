# Arcwright — Known Issues, Best Practices & Roadmap
## The Living Tally

**Version:** 1.0.2 (Current)
**Last Updated:** 2026-03-28
**Purpose:** Internal tracking + release planning + customer communication

This document is the single source of truth for:
1. What is broken in Arcwright and being fixed (Category 1)
2. What works but requires specific AI behavior (Category 2)
3. What capability is missing and being added (Category 3)

Every session that hits a problem feeds this document.
Every release is planned from this document.
Every marketing update references this document.

---

## HOW TO READ THIS DOCUMENT

### User Experience Column
This describes exactly what a customer experiences — not the
technical cause. Written from the customer's perspective.
Use this for marketing copy and release notes.

### AI Experience Column
This describes what the AI does when it hits this problem.
Use this for AI Guide updates and skill files.

### Resolution Column
- 🔴 OPEN — not yet fixed
- 🟡 IN PROGRESS — being worked on
- 🟢 FIXED — resolved in listed version
- 📋 DOCUMENTED — added to AI Guide / best practices

---

## CATEGORY 1 — ARCWRIGHT FIXES
### Broken commands that need C++ fixes

These are failures where the command exists, the AI calls
it correctly, but the result is wrong or missing.
The user experiences these as "nothing works" moments.

| # | Command | What Breaks | User Experience | AI Experience | Fix Version | Status |
|---|---|---|---|---|---|---|
| F001 | setup_scene_lighting | Hardcodes intensity=2, ignores all params | New level is completely black. AI tries lighting, fails, rebuilds from scratch. User wastes 1-2 hours on day one. | AI calls command with correct params, gets intensity=2 regardless, scene stays black, enters workaround loop | v1.0.3 | 🔴 OPEN |
| F002 | take_screenshot | Captures editor viewport wireframe, not PIE window | Screenshots during testing show wireframe icons or black — useless for verification or recording | AI reports screenshot taken but image is black. Cannot verify visual results. Retries indefinitely. | v1.0.3 | 🔴 OPEN |
| F003 | play_in_editor | Returns before PIE is fully loaded | AI takes screenshot immediately after PIE start — black image. Thinks PIE failed. | AI calls play_in_editor, immediately calls take_screenshot, gets black result, enters confusion loop | v1.0.3 | 🔴 OPEN |
| F004 | run_console_command | Param name conflicts with internal function | Console commands silently fail or error with confusing message | AI tries to use console commands as fallback for other broken commands, also fails | v1.0.3 | 🔴 OPEN |
| F005 | set_actor_property | Light intensity/color not always applied to spawned actors | Spawned lights appear with default values — often white and dim | AI sets property, reports success, property not actually applied | v1.0.3 | 🔴 OPEN |
| F006 | verify_all_blueprints | Sometimes reports 0 errors when errors exist | AI reports "all clean" but engine shows compile errors | AI trusts the response without cross-checking compile output | v1.0.3 | 🔴 OPEN |

---

## CATEGORY 2 — BEST PRACTICES
### Commands that work but require specific AI behavior

These are NOT bugs. The commands work correctly when used
properly. The AI needs specific instructions to use them
in the right sequence or with the right approach.
The user experiences these as "it worked eventually" moments
— or never finds out why it worked the third time.

| # | Topic | What Goes Wrong | User Experience | Correct Approach | Documented In | Status |
|---|---|---|---|---|---|---|
| P001 | Blueprint component property sequence | Setting properties before first compile silently fails | Widgets and actors appear with wrong defaults. Colors are white. Components have wrong sizes. | 1. add_component ALL components 2. compile_blueprint FIRST 3. set_component_property AFTER compile 4. compile again | SKILL_003, AI Guide §5 | 📋 DOCUMENTED |
| P002 | Default event node recreation | Duplicate BeginPlay/Overlap/Tick nodes become Event None | Blueprint logic never fires. Actor does nothing in PIE. AI spent time wiring logic that silently fails. | Never add BeginPlay/Overlap/Tick via add_nodes_batch. Wire directly to node_0/node_1/node_2. | AI Guide §5.1, CLAUDE.md Lesson 1 | 📋 DOCUMENTED |
| P003 | Blueprint _C suffix for spawning | Spawning without _C creates plain actor with no BP logic | Spawned actors do nothing — no movement, no overlap, no behavior. AI thinks BP is broken. | Always use full path with _C suffix: /Game/Path/BP_Name.BP_Name_C | AI Guide §5.1, Quick Start | 📋 DOCUMENTED |
| P004 | hex: color prefix | Colors applied without hex: prefix look washed out | UI colors are wrong — dark navy appears grey, amber appears pale yellow | Always use hex:#RRGGBB prefix. Arcwright converts sRGB to Linear automatically. | AI Guide §5.2, Quick Start | 📋 DOCUMENTED |
| P005 | Widget FillHeight totals | FillHeight values in VerticalBox not totaling 1.0 | Widget layout breaks — panels overlap or collapse. AI keeps adjusting sizes. | FillHeight values across all VerticalBox children must total exactly 1.0 | AI Guide §5.3, CLAUDE.md Lesson | 📋 DOCUMENTED |
| P006 | PIE screenshot 5-second delay | Screenshotting too fast after PIE start gives black image | AI reports screenshot taken but image unusable for verification | Always wait minimum 5 seconds after play_in_editor before take_screenshot | SKILL_002, AI Guide §2.4 | 📋 DOCUMENTED |
| P007 | Lighting on new levels | Every new blank level has zero lighting | Scene is black in PIE. AI thinks rendering is broken. Hours lost. | Run setup_default_lighting (v1.0.3) or BP_NeonLighting workaround at session start | SKILL_001, AI Guide startup | 📋 DOCUMENTED |
| P008 | Content path format | Using filesystem paths instead of /Game/ paths | AI references C:\Projects\... instead of /Game/... — asset not found errors | Always use /Game/ paths for content. Never filesystem paths. | AI Guide §6.5, CLAUDE.md | 📋 DOCUMENTED |
| P009 | Save after every change | Not saving means changes lost on crash | AI builds 20 things, UE crashes, all lost. Session has to restart. | save_all after every meaningful change. save_level after spawning actors. | AI Guide §5.5, Quick Start | 📋 DOCUMENTED |
| P010 | Compile before PIE testing | Uncompiled Blueprint changes don't appear in PIE | AI changes Blueprint logic, runs PIE, sees old behavior, thinks command failed | Always compile_blueprint before play_in_editor. Uncompiled = old version in PIE. | AI Guide §4.1, Quick Start | 📋 DOCUMENTED |
| P011 | Check assets exist before creating | Creating asset that already exists corrupts it | Random Blueprint corruption. Properties reset. Logic disappears. | Always find_assets before create_blueprint. If exists — modify, don't recreate. | AI Guide §3.2 | 📋 DOCUMENTED |
| P012 | Verify commands with read-back | Commands report success but silently fail | AI builds 10 elements, discovers element 3 was wrong, whole build is corrupted | After every action: read back from UE to confirm. Never trust the response alone. | AI Guide §2.2, Quick Start | 📋 DOCUMENTED |

---

## CATEGORY 3 — MISSING COMMANDS
### Capabilities that don't exist yet and need new commands

These are workarounds the AI uses because no command exists.
The user experiences these as "why is this so complicated?"
moments — something that should be one line takes 10 steps.

| # | Missing Command | What AI Does Instead | User Experience | Planned Command | Target Version | Status |
|---|---|---|---|---|---|---|
| M001 | setup_default_lighting | Creates BP_Lighting actor with SkyLight + DirectionalLight components manually | Setting up basic lighting takes 8+ steps. New users always fail here. Day-one blocker. | setup_default_lighting {scene_type: outdoor/indoor/dark} | v1.0.3 | 🔴 OPEN |
| M002 | set_view_mode | Attempts run_console_command which fails | Cannot switch between lit/unlit/wireframe for debugging | set_view_mode {mode: lit/unlit/wireframe/detail_lighting} | v1.0.3 | 🔴 OPEN |
| M003 | set_ambient_light | No workaround — ambient control not possible | Cannot fine-tune scene ambient lighting | set_ambient_light {intensity, color} | v1.0.3 | 🔴 OPEN |
| M004 | wait_for_pie_ready | Manual sleep/delay before every PIE interaction | Every PIE session needs awkward timing. Screenshots frequently black. | Add wait_for_ready param to play_in_editor | v1.0.3 | 🔴 OPEN |
| M005 | batch_spawn_actors | Spawns actors one at a time in a loop | Spawning 20 actors takes 20 round trips. Slow and error-prone. | batch_spawn_actors [{class, label, x, y, z}...] | v1.0.4 | 🔴 OPEN |
| M006 | set_level_post_process | No post process control | Cannot set bloom, tone mapping, exposure for cinematics | set_level_post_process {bloom, exposure, saturation, contrast} | v1.0.4 | 🔴 OPEN |
| M007 | get_build_errors | Must parse output log manually | AI reads raw log trying to find errors — misses things | get_build_errors — returns structured error list with file, line, message | v1.0.3 | 🔴 OPEN |
| M008 | teleport_player_smooth | Hard cuts only, no interpolation | Camera teleporting looks jarring in recordings | teleport_player_smooth {x,y,z, duration_seconds} | v1.0.4 | 🔴 OPEN |
| M009 | set_time_of_day | No dynamic sky control | Cannot demonstrate day/night scenes | set_time_of_day {hour: 0-24, transition_seconds} | v1.0.4 | 🔴 OPEN |
| M010 | apply_material_by_name | Must know full asset path | AI guesses wrong paths for materials | apply_material_by_name {actor, material_name} — searches project automatically | v1.0.4 | 🔴 OPEN |
| M011 | create_post_process_volume | No way to create PPV | Advanced visual effects impossible without PPV | create_post_process_volume {bounds, settings} | v1.0.4 | 🔴 OPEN |
| M012 | get_actor_screenshot | No per-actor screenshot | Cannot capture specific actor for verification | get_actor_screenshot {actor_name} — frames and captures target actor | v1.0.4 | 🔴 OPEN |

---

## RELEASE PLANNING

### v1.0.3 — Stability Release
**Theme:** Fix the day-one blockers
**Target:** 4-6 weeks after v1.0.2 approval

Fixes from Category 1:
- F001: setup_scene_lighting — fix hardcoded intensity
- F002: take_screenshot — use PIE viewport when PIE active
- F003: play_in_editor — add wait_for_ready param
- F004: run_console_command — fix param name conflict
- F005: set_actor_property — fix light property application
- F006: verify_all_blueprints — cross-check compile output

New commands from Category 3:
- M001: setup_default_lighting
- M002: set_view_mode
- M003: set_ambient_light
- M004: wait_for_pie_ready (part of play_in_editor fix)
- M007: get_build_errors

**Customer headline:**
"v1.0.3 — Lighting, screenshots, and PIE testing now
work reliably from the first session on any new project."

### v1.0.4 — Power Release
**Theme:** Scale and cinematics
**Target:** 8-10 weeks after v1.0.2 approval

New commands from Category 3:
- M005: batch_spawn_actors
- M006: set_level_post_process
- M008: teleport_player_smooth
- M009: set_time_of_day
- M010: apply_material_by_name
- M011: create_post_process_volume
- M012: get_actor_screenshot

**Customer headline:**
"v1.0.4 — Batch operations, post-process control, and
cinematic camera tools for demo recordings and presentations."

---

## MARKETING COPY BY VERSION

### v1.0.3 Release Post (X.com)
```
Arcwright v1.0.3 is live.

The big fix: lighting, screenshots, and PIE testing
now work on the first session of any new project.

v1.0.2 had a day-one blocker — blank levels were black,
screenshots captured editor wireframes, not the game.

Fixed. Properly.

New commands:
→ setup_default_lighting (outdoor/indoor/dark modes)
→ set_view_mode (lit/unlit/wireframe)
→ get_build_errors (structured error output)

All updates free. Always.
```

### v1.0.4 Release Post (X.com)
```
Arcwright v1.0.4 is live.

Batch everything. Control everything. Record everything.

→ batch_spawn_actors — 50 actors in one command
→ set_time_of_day — dynamic sky for any scene
→ teleport_player_smooth — cinematic camera moves
→ set_level_post_process — bloom, exposure, tone
→ get_actor_screenshot — frame and capture any actor

The AI demo recording workflow just got a lot cleaner.

Free update. On FAB now.
```

---

## HOW TO ADD NEW ENTRIES

When Claude Code hits a problem in any session:

STEP 1 — Identify the category:
  Is the command broken? → Category 1 (F-series)
  Is the sequence wrong? → Category 2 (P-series)
  Does the command not exist? → Category 3 (M-series)

STEP 2 — Add to the correct table with:
  - Next available number in series
  - Command name (or topic for P-series)
  - What breaks / what's wrong
  - User experience (customer language)
  - AI experience (technical language)
  - Resolution / correct approach
  - Target version
  - Status: 🔴 OPEN

STEP 3 — If Category 2, also:
  - Create SKILL_XXX.md in knowledge/skills/
  - Add to AI Guide
  - Add to CLAUDE.md lessons

STEP 4 — If Category 1 or 3, also:
  - Add to Claude Code fix file for next version
  - Update release planning section

STEP 5 — Update "Last Updated" date at top

---

## SEEKING NEW IMPROVEMENTS PROACTIVELY

Beyond logging problems as they occur, actively seek
improvements in these areas each release cycle:

### Workflow Analysis
After every 5 sessions, ask:
  - What did the AI do in 3+ steps that should be 1?
  - What did the AI have to look up every time?
  - What sequence is always the same? (candidate for compound command)

### Common AI Failure Patterns to Watch For
  - AI re-reads the same docs repeatedly (missing context)
  - AI retries same command 3+ times (broken command)
  - AI uses 10 commands to do something (missing compound command)
  - AI asks for clarification on same thing repeatedly (missing default)
  - AI produces wrong visual result (color/scale/units issue)

### Compound Command Candidates
These are sequences that should become single commands:

  setup_gameplay_ready — 
    health_check + setup_default_lighting + 
    verify_all_blueprints + run_map_check
    (session startup in one command)

  create_patrol_enemy {name, path, patrol_radius, detection_range} —
    create_blueprint + add_components + setup_ai + 
    create_behavior_tree + link_all
    (full enemy in one command)

  create_game_hud {name, path, health=true, ammo=true, 
                   minimap=false, objectives=true} —
    create_widget + build standard HUD layout
    (full HUD in one command)

  deploy_test_level —
    verify_all_blueprints + run_map_check + 
    setup_default_lighting + play_in_editor + 
    wait_for_ready + take_screenshot
    (full test cycle in one command)

### Community Sourcing
When Arcwright has customers:
  - Monitor GitHub Issues for reported problems
  - Classify each issue as F/P/M immediately on report
  - F-series issues get milestone tag for next patch
  - P-series issues get AI Guide update within 48 hours
  - M-series issues go to roadmap voting

---

## CUSTOMER-FACING VERSION OF THIS DOCUMENT

A simplified public version lives at:
github.com/Divinity-Alpha/Arcwright/docs/KNOWN_ISSUES.md

It contains:
  - Active issues with workarounds
  - Planned fixes and target versions
  - Changelog of resolved issues

Format for customers:

## Active Issues

### Black screen on new levels (workaround available)
**Affects:** All new projects, v1.0.2
**Workaround:** See SKILL_001 in docs/skills/
**Fix:** v1.0.3 — setup_default_lighting command

### Screenshots black in PIE (workaround available)
**Affects:** All screenshot usage, v1.0.2
**Workaround:** Wait 5 seconds after play_in_editor
**Fix:** v1.0.3 — auto-detects PIE viewport

---
Last updated: 2026-03-28
