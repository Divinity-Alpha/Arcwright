# SKILL 004 — Strict Includes for FAB Submission
**Category:** Plugin Packaging
**Status:** Process established
**Reliability:** High when process is followed
**Discovered:** FAB submission rounds r1-r6

## Problem
FAB build server compiles without unity builds.
Local builds hide missing includes through unity build
merging. Plugin compiles locally but fails on FAB server.

## Root Cause
Unity builds merge .cpp files — missing includes get
pulled in transitively. FAB compiles each file
independently with -StrictIncludes. Local builds never
reveal the problem.

## Correct Pre-Submission Process
1. Add bUseUnity = false to Arcwright.Build.cs
2. Clean all intermediates
3. Build.bat -DisableUnity -NoHotReload
4. Check: zero errors required
5. RunUAT BuildPlugin -StrictIncludes (test package)
6. Check: zero errors required
7. Remove bUseUnity = false
8. RunUAT BuildPlugin (final package — no -StrictIncludes)
9. Zip excluding Binaries/Intermediate/Saved/Build

## Commonly Affected Files
Headers that commonly need explicit includes under strict mode:
- FJsonObject -> Dom/JsonObject.h
- FJsonValue -> Dom/JsonValue.h
- FAssetData -> AssetRegistry/AssetData.h
- UEdGraphPin -> EdGraph/EdGraphPin.h
- EMaterialDomain values -> MaterialDomain.h
- ENGINE_MAJOR_VERSION -> Misc/EngineVersionComparison.h
- TCondensedJsonPrintPolicy -> CondensedJsonPrintPolicy.h
- FPackageName -> Misc/PackageName.h

## Rule
Run strict includes test before EVERY FAB submission.
No exceptions. This is what cost 5 review rounds.

## Verification Checklist
Process confirmed working — v1.0.2 r6 approved
