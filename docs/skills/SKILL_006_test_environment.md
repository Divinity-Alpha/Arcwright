# SKILL 006 — Test Environment Pollution
**Category:** Testing
**Status:** Documented
**Discovered:** v1.0.3 continuous fix loop

## Problem
Discovery test suite showing 10/15 failures after
all known bugs were fixed. Tests appeared broken
but commands were working correctly.

## Root Cause
Accumulated game content from NeonBreach development
sessions (actors, blueprints, widgets) caused
interference with PIE sessions in the test project.
PIE would crash due to content conflicts, then
cascade into all downstream screenshot tests.

## Rule
The test project (ArcwrightTestBed) must be kept
clean. After any development or demo session that
uses the test project, run cleanup before testing:

1. Delete /Game/NeonBreach/ and /Game/Demo/
   from the test project entirely
2. delete_actor on any stray spawned actors
3. save_all and restart UE5
4. Run test suite on fresh clean level

## Better approach
Maintain TWO separate projects:
- ArcwrightTestBed — tests only, never used for demos
- ArcwrightDemo — NeonBreach and other demos

Never run tests in a project that has been used
for development or demo work.

## Verification Checklist
- [ ] Created separate ArcwrightTestBed project
- [ ] Created separate ArcwrightDemo project
- [ ] Run 5 baseline on clean ArcwrightTestBed
- [ ] Discovery target 12/15 confirmed on clean project
