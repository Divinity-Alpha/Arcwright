# SKILL 002 — PIE Screenshots
**Category:** Testing and Verification
**Status:** FIXED in v1.0.3
**Reliability:** High
**Discovered:** NeonBreach session

## v1.0.3 Fix
- `play_in_editor` now has `wait_for_ready` param (default `true`) — polls until PIE is loaded
- `take_screenshot` now auto-detects PIE viewport and captures game view instead of editor
- `take_screenshot` accepts `delay_ms` param for additional stabilization
- No longer requires manual 5-second delay

## Problem
take_screenshot captures editor viewport (wireframe icons)
not the PIE game window. Always black or shows editor chrome.

## Root Cause
take_screenshot uses wrong viewport reference when PIE is
running. Should use GEditor->PlayWorld viewport when PIE
is active, but uses editor viewport instead.

## Current Workaround
1. play_in_editor
2. Wait minimum 5 seconds before ANY screenshot
3. teleport_player to desired location
4. Wait 1 additional second
5. take_screenshot
NEVER screenshot within 5 seconds of PIE start.

## Correct Solution — v1.0.3
- take_screenshot auto-detects PIE state
- Uses PIE viewport when GEditor->PlayWorld != nullptr
- Adds delay_ms param (default 0, recommend 2000 for new levels)
- play_in_editor adds wait_for_ready param

## Verification Checklist
- [ ] 5-second delay workaround confirmed working
- [ ] v1.0.3 fix implemented and tested
