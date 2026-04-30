# Documentation Audit Progress

## Phase 1: Architecture (COMPLETED)
- [x] `architecture/initialization.md` — Expanded sequence diagram, added startup steps table, clarified obj_Init/obj_globalManager roles, added fallback creation code.
- [x] `architecture/global-state.md` — Replaced UI Stack with UI Blocking (scr_checkUIBlocking), added detailed tables for inventory/stats, dialogue face, DEV-LOAD, notifications. Clarified music globals.
- [x] `architecture/objects.md` — Added obj_music_ctrl, expanded descriptions with GML details, added comparison table for obj_Init vs obj_globalManager.
- [x] `architecture/rooms.md` — Updated room descriptions with specific objects and functionalities, added global.rooms_by_name snippet.
- [x] `architecture/overview.md` — Replaced UI Stack with UI Blocking in core principles.

## Phase 2: Core Systems (COMPLETED)
- [x] `systems/input.md` — Added scr_buildInputMap, clarified scr_input_repeater defaults, listed UI objects ignoring cutscene blocking, added scr_input_rebind description.
- [x] `systems/interaction.md` — Updated legacy wrappers table (interactionWithNPCsOrObjects bbox, interactionWithMainCast mask), added tip block.
- [x] `systems/ui.md` — Rewrote UI Stack section → UI Blocking (scr_checkUIBlocking). Added conditions table, function signature, warning about non-existent scr_ui_push/pop.
- [x] `systems/music.md` — Verified current, no changes needed.
- [x] `systems/dialogue-portraits.md` — Verified current, no changes needed.
- [x] `systems/ui-tuning-map.md` — Verified current, no changes needed.

## Phase 3: Cutscenes (COMPLETED)
- [x] `systems/cutscenes/api.md` — Added camera_pan, camera_shake, camera_pan_obj, camera_track, camera_track_until_stop, set_facing (string directions) to JSON action types. Added ActionDialogue safety timeout and path normalization notes.
- [x] `systems/cutscenes/examples.md` — Rewrote Example 1 to reflect JSON-style obj_cutsceneTest with cutscene_load_json(). Added legacy fallback note. Added Yarn Chatterbox registration example.
- [x] `systems/cutscenes/architecture.md` — Verified current, no changes needed.
- [x] `systems/cutscenes/camera.md` — Verified current, no changes needed.
- [x] `systems/cutscenes/debugging.md` — Verified current, no changes needed.
- [x] `systems/cutscenes/actors.md` — Verified current, no changes needed.
- [x] `systems/cutscenes/player_in_cutscene.md` — Verified current, no changes needed.
- [x] `systems/cutscenes/troubleshooting.md` — Verified current, no changes needed.

## Phase 4: Undefscene Editor (COMPLETED)
- [x] `systems/cutscenes/undefscene/faq.md` — Added notes about Ctrl+hotkey fix for non-Latin layouts, React Flow callback stabilization, Select tool (actor markers only), Play button local preview.
- [x] `systems/cutscenes/undefscene/ui.md` — Added Select tool and Play button descriptions in Visual Editing section.
- [x] `systems/cutscenes/undefscene/overview.md` — Verified current (already mentions CameraShakeNode, AutoFacingNode, AutoWalkNode).
- [x] `systems/cutscenes/undefscene/formats.md` — Verified current, no changes needed.
- [x] `systems/cutscenes/undefscene/workflow.md` — Verified current, no changes needed.
- [x] `systems/cutscenes/undefscene/integration.md` — Verified current, no changes needed.
- [x] `systems/cutscenes/undefscene/room-screenshot-pipeline.md` — Verified current, no changes needed.
- [x] `systems/cutscenes/undefscene/validation.md` — Verified current, no changes needed.

## Phase 5: Gameplay (COMPLETED)
- [x] `gameplay/mechanics.md` — Replaced "UI stack" reference with "UI blocking (scr_checkUIBlocking)".
- [x] `gameplay/overview.md` — Verified current, no changes needed.
- [x] `gameplay/controls.md` — Verified current, no changes needed.

## Phase 6: Code Reference (COMPLETED)
- [x] `code-reference/gml-scripts.md` — Verified current, no changes needed.
- [x] `code-reference/events.md` — Verified current, no changes needed.
- [x] `code-reference/functions.md` — Verified current, no changes needed.

## Phase 7: Getting Started (COMPLETED)
- [x] `getting-started/project-structure.md` — Replaced UI Stack with UI Blocking for obj_globalManager description.
- [x] `getting-started/setup.md` — Verified current, no changes needed.
- [x] `getting-started/first-run.md` — Verified current, no changes needed.

## Phase 8: Planning (COMPLETED)
- [x] `planning/reviews/review_2025-12-28.md` — Added clarification about session date.
- [x] `planning/reviews/review_2026-01-15.md` — Verified current (historical document, many items fixed in subsequent refactors).

## Phase 9: Finalization (COMPLETED)
- [x] CSS файл extra.css проверен — чистый, без markdown fence.
- [x] Mermaid диаграммы: уже используются в `architecture/initialization.md` и `architecture/overview.md`.
- [x] Code annotations добавлены в `code-reference/gml-scripts.md` для `scr_applySettings`, `scr_settings_apply_and_save`, `scr_buildInputMap`, `scr_input_rebind_slot`, `scr_facing_to_sprite`, `scr_sprite_to_facing`.
- [x] Content tabs добавлены в `systems/music.md` — `global.play_music` vs `global.play_music_immediate` в табах "С фейдом" / "Без фейда".
- [x] Кастомная страница `docs/404.md` создана.
- [x] `search.highlight` уже включён в `mkdocs.yml`.
- [x] `docs/tags.md` создан, `tags` plugin добавлен в `mkdocs.yml`, навигация обновлена.
- [x] mkdocs.yml navigation обновлена — `tags.md` добавлен.
- [x] Permanent knowledge сохранена в memory (key architectural invariants).

## Key Invariants Discovered (to save in memory)
1. UI blocking is hardcoded in `scr_checkUIBlocking()`, not a dynamic stack. No scr_ui_push/pop exist.
2. `obj_Init` handles cold-start init; `obj_globalManager` handles runtime. Both are persistent.
3. `obj_cutsceneTest` uses JSON via `cutscene_load_json()` as primary path, with legacy fn fallback.
4. ActionDialogue has 600-frame safety timeout to prevent infinite hangs on broken .yarn files.
5. JSON cutscene factory supports camera_pan, camera_shake, auto_facing, auto_walk, set_facing with string directions.
6. Undefscene editor: Select tool works on actor markers only; Play button is local preview only.
7. Undefscene editor hotkeys use `e.code` not `e.key` for layout-agnostic Ctrl+A/C/X/Z.
