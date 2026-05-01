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

## Phase 10: Megaplan Audit & Polish (COMPLETED)

### 10A: Baseline snapshot ✅
- [x] `docs-megaplan-findings.md` создан
- [x] `mkdocs build --strict` проходит

### 10B: Fact-check (all 42 pages) ✅
- [x] `architecture/` — все сигнатуры сверены с кодом (scr_checkUIBlocking, scr_game_state_*, scr_global_handle_dev_spawn, scr_roomFromName, scr_global_on_room_change, scr_global_transition_safety)
- [x] `systems/input.md` — scr_input_pressed/down/repeater/rebind/rebind_slot сигнатуры подтверждены
- [x] `systems/ui.md` — scr_checkUIBlocking подтверждена
- [x] `systems/music.md` — play_music/stop_music/pause_music/API подтверждены
- [x] `systems/interaction.md` — scr_interaction подтверждена
- [x] `systems/dialogue-portraits.md` — scr_parse_emote/map_emotions подтверждены
- [x] `systems/cutscenes/*` — cutscene_load_json, start_cutscene, cutscene_register_chatterbox_functions подтверждены
- [x] `systems/cutscenes/undefscene/*` — CameraShakeNode, AutoFacingNode, AutoWalkNode в editor-app подтверждены
- [x] `gameplay/controls.md` — F1-F12 debug hotkeys сверены с scr_global_debug_hotkeys, scr_debug_activation_check, scr_player_debug_ghost
- [x] `code-reference/` — справочные страницы без конкретных сигнатур, факт-чек тривиально пройден
- [x] `getting-started/` — справочные страницы, факт-чек пройден

### 10C: Text polish ✅
- [x] Убраны временные маркеры из `undefscene/ui.md` (3 шт: "больше не", "теперь" ×2)
- [x] Убран "теперь" из `cutscenes/api.md`
- [x] Голое "Важно:" → `!!! warning` в `cutscenes/actors.md`
- [x] Blockquote "Важно:" → `!!! tip` в `interaction.md`
- [x] Голое "Примечание:" → `!!! note` в `cutscenes/examples.md`
- [x] Финальная проверка: 0 оставшихся "теперь", "больше не", "Важно:", "Примечание:", TODO/FIXME

### 10D: Structural polish ✅
- [x] `tags:` frontmatter добавлен ко всем 38 страницам (исключая index.md, 404.md, tags.md, glossary.md, _snippets/abbr.md)
- [x] Grid cards добавлены: `architecture/overview.md`, `systems/cutscenes/overview.md`, `gameplay/overview.md`
- [x] Content tabs добавлены: `cutscenes/examples.md` (JSON/Builder/Yarn), `input.md` (rebind/rebind_slot)
- [x] Collapsible `???+ note` для таблицы globals в `music.md`
- [x] Abbr-определения: `_snippets/abbr.md` создан (GML, NPC, UI, SFX, BPM, OGG, RF, IPC, FPS, JSON, Yarn), `pymdownx.snippets` подключён в mkdocs.yml с auto_append
- [x] Code `title=` добавлен в `gml-scripts.md` (4 блока) и `initialization.md` (1 блок)

### 10E: Navigation ✅
- [x] Все 42 .md страницы включены в mkdocs.yml nav
- [x] `404.md` добавлен в nav

### 10F: Final verification ✅
- [x] 0 временных маркеров
- [x] 0 TODO/FIXME
- [x] 0 голых "Важно:" / "Примечание:"
- [x] Все страницы имеют tags frontmatter
- [x] mkdocs.yml включает pymdownx.snippets + abbr

