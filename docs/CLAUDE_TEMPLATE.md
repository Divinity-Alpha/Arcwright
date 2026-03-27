# [PROJECT NAME] — Claude Code Context
> Replace everything in [brackets] with your project details.
> Delete this line when done.

**Doc Version:** 1.0  
**Project:** [Your Game Name]  
**Engine:** UE 5.7  
**Plugin:** Arcwright v1.0.2  

---

## Arcwright Connection

**MCP Server:**
```
C:/Program Files/Epic Games/UE_5.7/Engine/Plugins/Marketplace/Arcwright/Scripts/mcp_server/server.py
```

**TCP Port:** 13377  
**Verify connection:** `{"command": "health_check", "params": {}}`  
**Expected:** `{"status": "ok", "data": {"version": "1.0.2"}}`

---

## Project

**Project Path:** `C:/Projects/[ProjectName]/`  
**Content Root:** `/Game/[ProjectName]/`  
**UE Version:** 5.7  

**Key Paths:**
```
Blueprints:  /Game/[ProjectName]/Blueprints/
UI Widgets:  /Game/[ProjectName]/UI/
Data Tables: /Game/[ProjectName]/Data/
AI/BT:       /Game/[ProjectName]/AI/
Materials:   /Game/[ProjectName]/Materials/
Characters:  /Game/[ProjectName]/Characters/
```

---

## Current State

### What's Built and Working
- [ ] [List completed systems here]
- [ ] [e.g., "BP_PlayerCharacter — movement, jump, sprint"]
- [ ] [e.g., "DT_Weapons — 20 rows, all stats complete"]

### What's In Progress
- [ ] [e.g., "Enemy AI — BT exists, patrol works, combat not wired"]

### Outstanding Items
- [ ] [e.g., "Inventory system — not started"]
- [ ] [e.g., "Main menu UI — HTML design done, not translated yet"]

---

## Architecture

**C++/Blueprint Split:**
[Describe which systems are C++ vs Blueprint]

**Subsystems:**
[List any custom subsystems and what they manage]

**Naming Conventions:**
```
Blueprints:   BP_[Name]          (BP_Enemy, BP_Door, BP_Pickup)
Widgets:      WBP_[Name]         (WBP_HUD, WBP_Inventory, WBP_MainMenu)
Data Tables:  DT_[Name]          (DT_Weapons, DT_EnemyStats)
Materials:    M_[Name]           (M_RockWet, M_GrassDry)
Behavior Trees: BT_[Name]        (BT_EnemyPatrol, BT_BossPhase)
Blackboards:  BB_[Name]          (BB_Enemy, BB_Boss)
```

---

## Strategic Rules

1. **Verify before reporting** — read back from UE5 before claiming success
2. **Compile before testing** — always compile before PIE
3. **Save after every change** — save_all is never optional
4. **PIE test gameplay features** — don't trust compile success alone
5. **Use hex: prefix for all colors** — hex:#RRGGBB triggers sRGB→Linear
6. **FillHeight must total 1.0** — in all VerticalBox hierarchies
7. **Default event nodes pre-exist** — never recreate node_0/1/2
8. **_C suffix for spawning** — /Game/.../BP_Name.BP_Name_C
9. **[Add your project-specific rules here]**

---

## Autonomous Operation

**Session Startup:**
```
1. health_check (launch UE5 if not running)
2. Kill crash reporter loop (background)
3. verify_all_blueprints → note pre-existing issues
4. run_map_check → note pre-existing warnings
5. Confirm correct level is open
6. Begin work
```

**Stop and Ask Only For:**
- Irreversible deletion of significant content
- Creative decisions only the developer can make  
- 3 consecutive failures with no new approach

**Everything else: attempt → verify → fix → report.**

---

## Check and Confirm Protocol

Every action: **ACTION → VERIFY → CONFIRM → NEXT**

```
Blueprint:  create → get_blueprint_details → compile → verify_all
Actor:      spawn → find_actors → get_actor_properties → PIE screenshot  
Widget:     create → add elements → get_widget_tree → read colors → PIE screenshot
Data:       create table → add rows → get_data_table_rows → verify count
```

---

## Critical Rules (Arcwright)

```
Colors:    Always hex:#RRGGBB — never raw float values for sRGB colors
Widgets:   Design canvas 1920×1080. FillHeight totals = 1.0 exactly.
Blueprints: node_0=BeginPlay, node_1=Overlap, node_2=Tick. Never recreate.
Spawning:  /Game/Path/BP_Name.BP_Name_C — _C suffix required for BP logic
Paths:     /Game/... not C:/Projects/... 
Saving:    save_all after every meaningful change. save_level after actors.
```

---

## Session End Protocol

```
1. Compile all modified Blueprints
2. verify_all_blueprints → must be 0 errors
3. run_map_check → note any new warnings
4. save_all + save_level
5. get_output_log → confirm clean
6. Report: what was built, what was tested, what was saved
```

---

## Notes and Lessons Learned

[Add project-specific gotchas and discoveries here as you work]

- [e.g., "The inventory widget needs WBP_ItemSlot reparented to BP_InventorySlot or drag/drop breaks"]
- [e.g., "Enemy pathfinding needs NavMeshBoundsVolume to cover the entire playable area"]

---

*Arcwright AI Guide: github.com/Divinity-Alpha/Arcwright/docs/ARCWRIGHT_AI_GUIDE.md*  
*Quick Start: github.com/Divinity-Alpha/Arcwright/docs/ARCWRIGHT_QUICK_START.md*  
*Docs: arcwright.app*
