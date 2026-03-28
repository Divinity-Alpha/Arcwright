# SKILL 003 — Blueprint Component Properties
**Category:** Blueprint Building
**Status:** Working — correct approach documented
**Reliability:** High when sequence is followed
**Discovered:** Early Arcwright development

## Problem
Components added via add_component sometimes don't persist
their properties. set_component_property silently fails.

## Root Cause
Properties set before first compile can fail silently.
Blueprint class definition is not fully initialized until
after the first compile.

## Correct Sequence — Always Follow This Order
1. create_blueprint
2. add_component (add ALL components before compiling)
3. compile_blueprint  <- REQUIRED before setting properties
4. set_component_property (safe after compile)
5. compile_blueprint again
6. verify_all_blueprints

## Never Do This
- Set properties before first compile
- Assume properties persisted without read-back
- Skip the verification compile

## Verification Checklist
Confirmed working across 50+ Blueprint builds
