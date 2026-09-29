# Фактчек `undefscene/nodes.md` + `ui.md` + `formats.md` + `room-visual-editor.md` — ревизия кода 7ee444a

Источник истины: `$E` = `Undefscene/editor-app` (только чтение). Cross-check JSON-экшенов и runtime-поведения: `$P` (только чтение) + `$D/docs_new/_meta/json_actions.txt`. Ссылки между страницами проверены по `_meta/nav_plan.md` — все целевые файлы существуют.

Ключевые факты из $E:
- `NODE_REGISTRY` (`src/renderer/src/editor/nodes/nodeRegistry.ts:64-1993`): **84 типа нод** в палитре; `start` — служебная, не входит в реестр и палитру (создаётся автоматически: `runtimeTypes.ts:137,216`, `useSceneIO.ts:250-260`). Суммарно 85 — совпадает с доком.
- Категории и счётчики: flow=3 (+start=4), movement=9, actor=6, visual=11, dialogue=9, camera=12, logic=19, audio=15 — все совпали с таблицей в nodes.md.
- Экспортёр (`compiler/exporters.ts:3-17`): выводит ровно `schema_version:1`, `cutscene_id` (slug из title, fallback `untitled`), `settings.fps:30` (жёстко, не настраивается), `actions`. **Никаких `skippable`/`debug`/`end` экспортёр не пишет.**
- Компилятор (`compiler/core.ts:218-232,374-379`): перед каждой именованной нодой (включая `start`, у которой `name='Start'`) эмитится `{type:'mark_node'}`; `start` эмитится действием, `end` — **никогда не эмитится** (ветка return без push).
- Runtime-загрузчик (`$P` `cutscene_load_json.gml`): читает `cutscene_id`, `settings.fps` (1–240, иначе `default_fps` из engine settings, строки 93-126), `settings.skippable` (дефолт `true`, строка 111), флаг `debug` берётся только из `actions[0]` если это `start` (строки 151-157); `"start"` пропускается, `"end"` завершает обход (`break`, строки 170-175).
- Хоткеи холста редактора захардкожены (`useEditorShortcuts.ts:107-346`): Ctrl+A/Z/Y/Shift+Z/S/N/O/E/P, Delete, Ctrl+C/X/V. Через `useHotkeys` реально подключены только 3 действия (`useEditorCallbacks.ts:256-268`, `EditorShell.tsx:339`): `toggle_inspector`, `zen_mode`, `toggle_all_dock_panels`. `focus_left/right/bottom_dock` и `fit_view` из списка в Preferences **не имеют обработчиков** (grep по actionId — пусто). Fit View захардкожен на Space и Ctrl+0/Numpad0 (`FlowCanvasKeyboardShortcuts.tsx:29-47`).
- ПКМ по ноде/ребру — мгновенное удаление, контекстного меню нет (`FlowCanvas.tsx:934-937,1124-1126`); pan — ПКМ-drag (`panOnDrag=[2]`, `FlowCanvas.tsx:51,1378`); MMB/`+`-кнопка создают `dialogue` (`useNodeOperations.ts:339`, `FlowCanvas.tsx:1300-1306`).
- Лейблы полей в UI идут через `t('nodes.fields.'+key)` (`NodeInspector.tsx:147,151`), поэтому часть имён в инспекторе отличается от registry-лейблов: `actor_name`→«Actor Name», `actor_sprite`→«Actor Sprite», `sound`→«Sound / Key», `target` у `goto`→«Target» (`ru.ts:414-470`, `en.ts`).
- RVE — отдельное native-окно без `alwaysOnTop` (`windowManager.ts:65-116`); открытие только через View → Visual Editing (`TopMenuBar.tsx:317-318`); кнопки в тулбаре/панелях нет.
- RVE: pan — **ЛКМ**-drag по пустому месту когда инструмент не выбран (`RoomVisualEditorModal.tsx:959-989`); ПКМ в окне не обрабатывается вообще. Snap к сетке — чекбокс «Snap to Grid» (шаг `PATH_GRID_STEP=20`, `usePathEditorLogic.ts:5`, `RoomVisualEditorModal.tsx:359-361`), **Ctrl ничего не делает**. Хоткеи: B/G toggle pencil/eraser, Ctrl+E импорт пути, Ctrl+Z/Y undo/redo черновика пути, Esc закрывает окно (`RoomVisualEditorModal.tsx:430-567`).
- RVE импорт пути: при выбранной ноде **заменяет её** на `follow_path` (сохраняя target/speed/collision), без выбора — предлагает создать новую (`useVisualEditing.ts:202-286`). Импорт актёров пишет `x`/`y` в существующие `actor_create`, матчинг по id маркера = id ноды; виртуальные маркеры (`isVirtual`, выбранный target/player) не импортируются (`useVisualEditing.ts:289-346`, `RoomVisualEditorModal.tsx:1207,1238`).
- `.usc.json` = `schemaVersion, title, nodes, edges, notes, selection(null), lastSavedAtMs` (`runtimeTypes.ts:225-430`, `useSceneIO.ts:66-77`). Состояние панелей там **не хранится** — layout лежит отдельно (`useLayoutState.ts`, IPC `layout`).
- Автосейв: интервал 1–120 мин, дефолт 10 (`usePreferences.ts:203-204,283-292`); для сохранённой сцены — ротация `<stem>.autosave-N<ext>` рядом с файлом (до 5), для несохранённой — файл `autosave-<timestamp>.usc.json` в служебной папке приложения, не «в памяти» (`ipc.ts:1431-1498`, `useSceneIO.ts:165-187`).
- `run_function` экспортирует `args` (не `arguments`) — `compilers/logic.ts:37-55`; runtime читает `args` (`json_actions.txt:22`).
- `tween` экспортирует `end_value`/`start_value_override` без переименования (`logic.ts:184-195`); runtime дополнительно принимает `to_value`/`from_value` (`json_actions.txt:54`).
- `wait_until` компилируется в `guard_global` с `if_false:'wait_until_true'`, `stop_when:'timeout'`+`end_timeout` или `'none'` (`logic.ts:5-26`).
- `ActionHalt.update` возвращает `true` сразу — нода мгновенная, очередь не блокирует (`$P` `scr_cutscene_classes.gml:3040-3048`).
- Цвета заметок: acting=синий(200), camera=фиолетовый(280), sound=зелёный(150), todo=янтарный(45-50), warning=красный(0) — `base.css:40-49`.
- Пункты меню: File → …, Export to Game..., Preferences... (НЕ Edit), Exit (`TopMenuBar.tsx:246-289`); Help → Advanced → Show Runtime JSON/Open DevTools/Disable HW Accel/Choose Screenshot Output Folder/VE Tech Mode/Cleanup Dev Data/Reset Severity Overrides (строки 160-225); Help → Check for Updates, About, Tutorial (343-350). Кнопки Undo/Redo — справа в верхней панели, не в левом доке (654-678).
- Preferences секции: General (язык/тема/акцент), Canvas (grid/zoom/minimap threshold/node names/parallel ports/dock preview/фон), Editor (autosave/liquid glass/path labels/screenshot folder), Keyboard (`PreferencesModal.tsx:155-292`).
- `settings.skippable` и `debug` на `start` — движок читает и применяет, но экспортёр их не пишет → только ручная правка JSON.

## nodes.md

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 11 | «Всего 85 нод; Start создаётся автоматически… в палитру не входит» | OK — 84 в `NODE_REGISTRY` (nodeRegistry.ts:1988-1993) + `start` (runtimeTypes.ts:137,216; не в реестре → не в палитре, NODE_TYPES=keys(registry):1997) |
| 17-26 | Таблица категорий: цвета и счётчики (4/9/6/11/12/9/19/15) | OK — `NODE_COLORS` (nodeRegistry.ts:5-15) и раскладка по `category` совпали построчно |
| 33 | «одна Start без входящих связей» | OK — ровно 1 обязательна (validators/graphChecks.ts:51-66; compile error без неё core.ts:85-91); входа у ноды нет структурно (nodes/flow.tsx:15 `hasInput={false}`) |
| 36 | «хотя бы одна End без исходящих» | OK — `missingEndNode` error (graphChecks.ts:67-74) + compile error (core.ts:94-97); выхода нет (flow.tsx:25 `hasOutput={false}`) |
| 39-43 | Wait: поле `seconds` | OK (nodeRegistry.ts:66-72, default 1) |
| 45-46 | Двойной клик по ребру ставит задержку | OK — dbl-click фокусирует поле «Wait on edge» в Inspector (FlowCanvas.tsx:1128-1133, EdgeInspector.tsx:21-47) |
| 48-56 | Room Change: room/player_x/player_y/actors(JSON) | OK (nodeRegistry.ts:1954-1967; actors — JSON-текст, парсится при экспорте: compilers/logic.ts:270-290) |
| 60-68 | Move: target/x/y/speed_px_sec/collision | OK (nodeRegistry.ts:73-103, дефолты 60/'false') |
| 70-76 | Set Position | OK (104-120) |
| 78-87 | Move Relative | OK (1675-1704) |
| 89-96 | Set Position Relative | OK (1706-1721) |
| 98-107 | Move Relative Direction: direction l/r/u/d | OK (1526-1567, options:1542) |
| 109-118 | Move Direct: value/use_speed | OK (1569-1612, use_speed — select 'false'/'true') |
| 120-129 | Follow Path: target/points/speed_px_sec/collision/autofacing | OK с уточнением: `points` — не обычное поле инспектора, а спец-редактор списка точек в Inspector (NodeInspector.tsx:251-348) + импорт из Visual Editing (useVisualEditing.ts:202-286); fields-список: target/speed/collision/autofacing (nodeRegistry.ts:1727-1755), `points` в defaultParams (1758). Уточнено |
| 131-140 | Jump: height default 16, easing-опции | OK (1049-1074) |
| 142-147 | Halt: поле target | OK (1075-1088) |
| 149-150 | «Halt … блокирует очередь выполнения катсцены для данной ветки — не ставьте после неё другие ноды» | **WRONG** — `ActionHalt.update` возвращает `true` в первый же кадр ($P scr_cutscene_classes.gml:3048); действие мгновенное, очередь не блокируется. Исправлено |
| 154-162 | Actor Create: actor_name/x/y/actor_sprite/copy_target | Частично WRONG — поля верны (nodeRegistry.ts:121-151), но лейблы в UI: `actor_name` показывается как «Actor Name» (не «Key»), `actor_sprite` — «Actor Sprite» (не «Sprite / Object») — i18n перекрывает registry-лейблы (ru.ts:419-421, en.ts:419-421, NodeInspector.tsx:147). Исправлено |
| 164-169 | Actor Destroy | OK (152-159) |
| 171-183 | Attach To Target: 9 полей | OK (161-224, дефолты совпали) |
| 185-191 | Detach | OK (226-245) |
| 193-201 | Lerp Property + список свойств | OK (247-263, options:257) |
| 203-209 | Set Emotion + список эмоций | OK (265-279, options:275) |
| 213-221 | Animate | OK (281-310) |
| 223-231 | Set Animation Frame | OK (312-346) |
| 233-239 | Set Depth + «режим manual» | OK (673-687; $P classes:727-728 `depth_mode='manual'`) |
| 241-247 | Set Facing | OK (689-709, options:705) |
| 249-255 | Auto Facing | OK (711-730) |
| 257-263 | Auto Walk | OK (732-751) |
| 265-271 | Flip | OK (1090-1109) |
| 273-280 | Spin | OK (1111-1126, speed default 10) |
| 282-293 | Shake Object: 7 полей | OK (1128-1179, дефолты mag 4/decay false/freq 1) |
| 295-305 | Emote: 7 полей | OK (1015-1047, offset_y default −24) |
| 307-313 | Set Visible | OK (1181-1200) |
| 317-323 | Camera Pan | OK (436-452) |
| 325-331 | Camera Pan To Object | OK (454-475) |
| 333-340 | Camera Pan (Speed): x/y = px/frame | OK (477-490, лейблы «Velocity X (px/frame)») |
| 342-347 | Camera Center | OK (491-500) |
| 349-357 | Camera Track | OK (394-417) |
| 359-366 | Camera Track Until Stop до `move_active==false` | OK (419-434; $P classes:4514-4523) |
| 368-378 | Camera Shake | OK (501-558) |
| 380-386 | Fade In | OK (753-762, seconds 0.5/color black) |
| 388-394 | Fade Out | OK (763-771) |
| 396-407 | Tween: поля | OK части; **WRONG** в тексте про export: `end_value`→`to_value` и `start_value_override`→`from_value` — наоборот, экспортируются как `end_value`/`start_value_override` без переименования (compilers/logic.ts:184-195); runtime принимает и то и другое ($P factory:523, json_actions.txt:54). Исправлено |
| 409-417 | Set Property + «JSON-строка парсится» | OK (626-668; value парсится JSON.parse: logic.ts:78-90; target скрыт при kind=camera: 644) |
| 419-428 | Tween Camera: legacy + поля | OK (1765-1794; legacy-комментарий в коде:1764) |
| 432-440 | Dialogue: file/node/block_queue/auto_advance | OK (348-358; runtime требует `.yarn` в file: $P factory:157-163) |
| 442-447 | Wait For Dialogue: dialogue_controller | OK (360-373; $P factory:166) |
| 449-450 | Wait Talk = алиас wait_for_dialogue | OK (375-392; normalize $P cutscene_load_json.gml:229) |
| 452-457 | Set Dialogue Speed «символов в секунду» | OK (1878-1883, default 1.0; $P classes:2738-2740 docstring) |
| 459-460 | Wait Typing без полей | OK (1885-1890) |
| 462-469 | Dialogue Control: 3 флага | OK (1892-1901; $P factory:183-187) |
| 471-472 | warning stay_open+Wait for Dialogue | OK по семантике (совместимо с $P classes — окно держится открытым) |
| 474-488 | Set Portrait Next/Now + эмоции | OK (1903-1945, options:1919,1941) |
| 490-491 | Clear Dialogue без полей | OK (1947-1952) |
| 495-502 | Parallel/Join: branches/joinId/pairId — editor-only | OK (1863-1876; фильтрация при экспорте — комментарий nodeRegistry.ts:1795-1799; пара автосоздаётся — useNodeOperations) |
| 504-509 | Branch: condition = имя функции, не выражение | OK (1248-1261; $P factory:298-332 — advisory whitelist по именам) |
| 511-518 | Branch Flag + операторы | OK (1263-1290, options:1279; value default 'true':1287) |
| 520-525 | GoTo Node: target = метка или имя ноды; «(поле Target Mark)» | Частично WRONG — семантика OK (1232-1246, registry label «Target Mark»; каждая именованная нода получает mark_node: core.ts:218-222; runtime goto→имя метки: $P factory:149-155), но в UI поле отображается как «Target» (i18n `nodes.fields.target`→'Target', ru.ts:414). Исправлено |
| 527-528 | warning о циклах | OK (совет, совместимо с семантикой goto) |
| 530-535 | Mark Node: name | OK (1216-1230, label «Mark Name») |
| 540-553 | Guard Global: 9 полей + опции | OK (1466-1515, options:1483,1491) |
| 555-556 | warning global[var] vs global.flag | OK ($P guard_global читает `global[$ var]`, json_actions.txt:93) |
| 558-565 | Wait Until: 3 поля | OK (1384-1411). Дополнено: при экспорте превращается в `guard_global` (logic.ts:5-26) — добавлено примечание |
| 567-568 | note о проверке раз в кадр | OK совместимо (guard_global polls var — $P factory:1133+) |
| 570-578 | Wait Interact: 4 поля + continue/abort_parallel | OK (1343-1382, options:1366,1373; семантика подтверждена $P classes:4526-4545 docstring) |
| 580-587 | Partial Control: control_type 0/1/2, allowed_actions/whitelist JSON-или-запятые | OK (1314-1341; парсинг list/JSON: logic.ts:95-137; whitelist показывается всегда — условия нет, но семантика «тип 1» верна по коду рантайма) |
| 589-595 | Run Function: «args … при export становится `arguments`» | **WRONG** — экспортируется как `args` без переименования (compilers/logic.ts:37-55); runtime читает `args` ($P json_actions.txt:22 — поля `function|function_name|fn|args`). Исправлено |
| 597-603 | Set Flag | OK (1413-1435) |
| 605-610 | Set Plot | OK (1517-1524) |
| 612-621 | Spawn Entity | OK (1437-1455, persistent default false) |
| 623-628 | Destroy Entity | OK (1457-1464) |
| 630-639 | Schedule Action: 5 полей + опции action_type | OK (1614-1670, options:1630-1639; вложенный action собирается из action_type+action_params: logic.ts:139-174) |
| 641-652 | Checkpoint State: 7 полей | OK (1800-1831) |
| 654-663 | Restore State + on_missing | OK (1833-1861, options:1851) |
| 665-670 | Instant Mode | OK (1202-1214) |
| 672-673 | «экспортируется как instant_mode → set_instant» | OK ($P normalize: cutscene_load_json.gml — instant_mode→set_instant; editor пишет тип ноды `instant_mode`) |
| 677-811 | Все 15 audio-нод и поля | OK построчно (773-1013; дефолты: music_duck 0.3/0.3, crossfade 0.5/1, play_music fade 0.5/persist true, music_pitch step 0.1:864) |
| 820 | sources-комментарий | OK после обновления («84 типа + start» — верно) |
| — | MISSING: хоткеи RVE/глобальные на этой странице не требуются; спец-поле `points` у Follow Path — уточнено выше | MISSING→добавлено в текст |

## ui.md

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 14 | «Левая панель — палитра + кнопки Save/Undo/Redo + Template Library + Bookmarks» | **WRONG** — левый док по умолчанию: Actions + Bookmarks (useLayoutState.ts:17); Templates скрыт (`panel.templates` mode 'hidden', строки 92-100); Save-кнопки нет вообще, Undo/Redo — иконки справа в верхней панели (TopMenuBar.tsx:660-677). Исправлено |
| 16 | «Правая панель — Inspector, Logs, Notes и Yarn Preview» | **WRONG** — правый док: Text + Inspector; Logs — нижний док; Notes скрыт (useLayoutState.ts:17-18,71,40-49). Исправлено |
| 18 | «…через меню панелей или кнопки на тулбаре» | Частично WRONG — меню Panels есть (TopMenuBar.tsx:230-239), «кнопок на тулбаре» для панелей нет. Исправлено |
| 20 | «панель полностью скрывается («Zen-режим»)» | Неточно — dock сворачивается до узкой полосы с кнопкой раскрытия (DockingLayout.tsx:205-209,271); Zen — отдельное действие, скрывающее все доки (useEditorCallbacks.ts:198-220). Исправлено |
| 26 | MMB по пустому месту → Dialogue | OK (FlowCanvas.tsx:968-999, useNodeOperations.ts:339; кнопка «+» делает то же: FlowCanvas.tsx:1300-1306,1432-1436) |
| 27 | Drag из палитры | OK (ActionsPanel.tsx:79-84 NODE_PALETTE_DRAG_MIME; клик по пункту палитры тоже добавляет ноду: 85-89 — дополнено) |
| 28 | ПКМ+движение — панорама | OK (panOnDrag=[2], FlowCanvas.tsx:51,1377-1378) |
| 29 | Рамка выделения ЛКМ | OK (selectionOnDrag + Partial, FlowCanvas.tsx:1384-1386) |
| 31 | «Удалить ноду/ребро — Правый клик → Delete» | Неточно — ПКМ по элементу удаляет сразу, без меню (FlowCanvas.tsx:934-937,1124-1126); Delete-клавиша работает для выделенных (useEditorShortcuts.ts:195-216). Исправлено |
| 32 | Соединение от handle | OK (xyflow onConnect) |
| 33 | Двойной клик по ребру — задержка | OK (FlowCanvas.tsx:1128-1133, EdgeInspector.tsx:22) |
| 34 | Condition на ребре в Inspector | OK (EdgeInspector.tsx:48-114) |
| 38 | «обязательные поля … экспорт покажет предупреждение» | OK (missingRequiredParam — severity warn, validators/nodeChecks.ts:121-139; ошибки блокируют экспорт: useSceneIO.ts:86-101) |
| 42 | Dialogue → Text/Yarn Preview | OK (TextPanel.tsx:39+; превью грузится для выбранной `dialogue` с `file`: useEditorState.ts:243-297) |
| 43 | Follow Path → Path Preview | OK (inspector/NodeInspector.tsx:4,352 FollowPathPreview) |
| 47-55 | Logs: Error блокирует/Warn/Tip; клик фокусирует | OK — severities 'error'/'warn'/'tip' (LogsPanel.tsx:13-14); экспорт блокируется error'ами (useSceneIO.ts:86-101); клик → select+focus (useEditorCallbacks.ts:281-292 → FlowCanvas setCenter:683-692). Уточнено: валидация непрерывная, не только «перед экспортом» |
| 57-67 | Notes + цвета категорий | Частично WRONG — категории верны (NotesPanel.tsx:30), но цвета перепутаны: camera=фиолетовый, sound=зелёный (base.css:42-45). Исправлено |
| 69-71 | Bookmarks «по именованным нодам, двойной клик центрирует» | **WRONG** — панель = список всех нод, **одиночный** клик выбирает и центрирует (BookmarksPanel.tsx:25, undefscene_a.md; useEditorCallbacks.ts:481-492). Исправлено |
| 73-75 | Template Library «Save as Template» | **WRONG** — панель называется «Templates»/«Шаблоны», кнопка «Save Selection», вставка — «Insert» (TemplateLibraryPanel.tsx:114,159-183; название: ru.ts:837/en.ts:845). Исправлено |
| 77-79 | Runtime JSON панель | OK (panel.runtime_json, useLayoutState.ts:82-91; включается также Help→Advanced→Show Runtime JSON, TopMenuBar.tsx:165-172) |
| 83-85 | Visual Editing «отдельное окно, кнопкой на панели» | Частично WRONG — отдельное native-окно и Alt+Tab верно (windowManager.ts:63-94), но открывается только через View → Visual Editing (TopMenuBar.tsx:317-318); кнопки «на панели» нет. Исправлено |
| 89-99 | Таблица инструментов RVE | Частично WRONG — «Draw Path» и «Undo Point» как отдельные инструменты не существуют; undo последней точки = Ctrl+Z (RoomVisualEditorModal.tsx:473-478); остальные (Pencil/Eraser/Clear/Import Path/Select/Place/Play/Import Actors) верны (RoomVisualEditorSidebar.tsx:217-262,310-359). Исправлено |
| 100 | Play — только превью | OK с нюансом — граф не трогает, но по окончании маркер актёра в RVE остаётся в финальной точке (RoomVisualEditorModal.tsx:890-905). Уточнено |
| 104-106 | «Ctrl — привязка к сетке 20px, Shift+Ctrl — оба режима» | **WRONG** — Ctrl в RVE не используется; snap включается чекбоксом «Snap to Grid» (RoomVisualEditorModal.tsx:359-361,166-176 sidebar; шаг PATH_GRID_STEP=20: usePathEditorLogic.ts:5). Shift→прямая линия верно (937,408). Исправлено |
| 113 | «Edit → Preferences (или кнопка в левом dock)» | **WRONG** — Preferences в меню **File** (TopMenuBar.tsx:281-285) + хоткей Ctrl+P (useEditorShortcuts.ts:187-192); кнопки в доках нет. Исправлено |
| 117-119 | General: Language/Theme/Accent, мгновенная смена | OK (PreferencesGeneralSection.tsx:35-126) |
| 123-125 | Canvas: MiniMap вкл/выкл, Zoom Speed, Grid Size | Частично — MiniMap управляется числом-порогом, не тумблером (PreferencesCanvasSection.tsx:57-76); остальное OK (25-56). Исправлено |
| 127-129 | Background: attach/mode/opacity | OK (PreferencesCanvasSection.tsx:109-223; attach = canvas|viewport) |
| 131-136 | Auto-save описание | Частично WRONG — для новых сцен пишется **файл** `autosave-<ts>.usc.json` в служебной папке приложения, не «в памяти» (ipc.ts:1486-1498); backup-ротация `<stem>.autosave-N` рядом со сценой до 5 шт (ipc.ts:1461-1484); интервал дефолт 10 мин (usePreferences.ts:204). Исправлено |
| 138-140 | Keyboard Shortcuts с переназначением | OK — UI переназначения есть (PreferencesKeyboardSection), но фактически подключены только toggle_inspector/zen_mode/toggle_all_dock_panels (useEditorCallbacks.ts:256-268). Уточнено |
| 144-159 | Таблица горячих клавиш | Частично WRONG — путь меню «Edit→Preferences» неверен (File); строки Focus Left/Right/Bottom Dock (Ctrl+1/2/3) — обработчиков нет, хоткей мёртвый (grep actionId → только 3 wired); добавлены отсутствующие: Ctrl+O, Ctrl+P, Ctrl+A, Ctrl+C/X/V, Delete, Ctrl+Shift+Z, Ctrl+0 (useEditorShortcuts.ts:124-345, FlowCanvasKeyboardShortcuts.tsx:29-47). Исправлено |
| 161-162 | Работает независимо от раскладки | OK (по e.code: useEditorShortcuts.ts:116-121) |
| 164-172 | Mini Map threshold 0/-1/>0, default 500 | OK (FlowCanvasMiniMap.tsx:16-22, usePreferences.ts:196) |
| 174-180 | Docking: 3 края + drag за заголовок + Reset Layout | OK (layoutTypes.ts:2, DockingLayout.tsx:191,526 floating; reset: useEditorCallbacks.ts:307-311; меню View→Reset Layout) |
| 182-186 | Auto-update при запуске + portable только уведомляет + Help→Check for Updates | OK (main/updater.ts:155-164 packaged-only,89-96 portable-флаг; TopMenuBar.tsx:344) |
| 188-192 | Welcome Setup: язык+акцент, Esc | OK (+тема: WelcomeSetupModal.tsx:95-158; только первый запуск: useEditorState.ts:154-161). Дополнено про тему |
| 194-202 | Toast-уведомления | Частично — Exported/Update/Screenshot/Log copied есть (en.ts:605-614); «Saved» — это индикатор в верхней панели, не toast (TopMenuBar.tsx:655-659, useSceneIO не пушит toast на save). Исправлено |
| 204-210 | Help → Advanced: DevTools/Runtime JSON/HW Accel | OK (TopMenuBar.tsx:160-225; там же Choose Screenshot Output Folder и др.) |
| 216-219 | Ссылки «См. также» | OK — все файлы в nav_plan.md |

## formats.md

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 15-18 | Два формата; `.usc.json` хранит «граф, позиции нод, состояние панелей» | Частично WRONG — панелей в файле нет; хранятся граф+позиции+notes+title (runtimeTypes.ts:225-430, useSceneIO.ts:66-77; layout отдельно). Исправлено |
| 22-28 | Таблица команд | OK (TopMenuBar.tsx:246-289; фильтры ipc.ts:1405,1502) |
| 30-31 | Предупреждение о потере несохранённого | OK (useSceneIO.ts:198-204) |
| 35 | «Export for Engine» | **WRONG** — пункт «Export to Game...»/«Экспорт в игру...» (en.ts:39, ru.ts:39, TopMenuBar.tsx:277). Исправлено |
| 37 | Сохранять в `datafiles/cutscenes/` | OK (конвенция рантайма: cutscene_load_json.gml — читает `cutscenes/*.json` из Included Files) |
| 45-46 | schema_version / cutscene_id | OK (exporters.ts:5-12; slug-правила совпали; schema_version движком не читается — уточнено) |
| 48 | settings.fps: 1–240, иначе default_fps | OK по движку ($P cutscene_load_json.gml:99-126); дополнено: экспортёр всегда пишет 30 (exporters.ts:13) |
| 49 | settings.skippable default true | OK по движку ($P:111 — читается и применяется), но экспортёр его **не пишет** (exporters.ts:13-15) → уточнено: задаётся ручной правкой JSON |
| 50 | actions array | OK ($P:135-149 обязателен) |
| 52-64 | Пример JSON | **WRONG** — экспортёр не пишет `skippable`, `debug`, `end`; перед `start` идёт `mark_node` для именованной стартовой ноды (core.ts:218-232). Пример переписан под реальный вывод + примечание о ручных полях |
| 67 | «start первый; может нести debug; end завершает список» | OK по движку ($P:151-157 debug только из actions[0]=start; :174-175 `end`→break), с оговоркой что экспортёр их не эмитит — дополнено |
| 68 | mark_node перед каждой именованной нодой | OK (core.ts:218-222,374-378) |
| 69 | Список legacy-алиасов | OK + MISSING: не хватало `destroy_entity`/`destroy`→`actor_destroy` и `emote`→`show_emote` ($P normalize:223-235; json_actions.txt:19-20,76). Дополнено |
| 71-75 | Обратный импорт Open Scene | OK (useSceneIO.ts:206-239: .usc.json → parseRuntimeState, иначе reverseCompile; ошибки → отказ) |
| 77-78 | «include_globals/include_instances ожидаются как JSON-строки; нативные массивы игнорируются» | **WRONG** — reverseCompile принимает и строки, и массивы (массивы сериализуются в текст инспектора) (reverseCompile.ts:620-628). Исправлено |
| 82-87 | Ссылки «См. также» | OK — все файлы в nav_plan.md |

## room-visual-editor.md

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 10 | RVE поверх скриншота локации | OK (RoomVisualEditorModal/Canvas) |
| 14-17 | Две задачи: актёры→Actor Create, путь→Follow Path | OK (useVisualEditing.ts:202-346) |
| 19 | «видно в Alt+Tab и остаётся поверх других приложений» | Частично WRONG — Alt+Tab да, `alwaysOnTop` не установлен (windowManager.ts:71-84). Исправлено |
| 23 | Open Project (.yyp) обязателен | OK (availableRooms из resources.rooms + screenshot bundles: useVisualEditing.ts:123-155) |
| 25 | «View → Visual Editing или кнопка на панели инструментов» | Частично WRONG — кнопки нет, только меню (TopMenuBar.tsx:317-318). Исправлено |
| 26 | Выбор комнаты в выпадающем списке | OK (RoomVisualEditorToolbar.tsx:37-47) |
| 28 | Автозагрузка скриншотов + «Нет комнат со скриншотами» | OK (en.ts:153 visualEditingNoScreenshotRooms; sidebar:150) |
| 32 | «выберите актёра из списка или укажите вручную» | Частично WRONG — это обычный select без ручного ввода (RoomVisualEditorSidebar.tsx:274-294); список = actor_create-ноды графа (+виртуальные target/player если их нет). Исправлено |
| 33-36 | Размещение + «координаты в x/y выбранных нод» | Неточно — координаты пишутся в actor_create-ноды по соответствию маркер↔нода (по id), не «выбранные» (useVisualEditing.ts:316-337). Исправлено |
| 38-39 | Режим выбора для перетаскивания маркера | OK (Sidebar Select:310-322; drag: Modal:963-977) |
| 43-47 | Карандаш/Shift-прямые/Ластик G/Импорт пути | OK (Modal:496-545,937; Sidebar:217-261) |
| 51-57 | Таблица кнопок пути | OK + MISSING: Ctrl+Z/Ctrl+Y undo/redo черновика пути (Modal:473-488) — добавлено |
| 61-64 | Координаты мира без пересчёта | OK (zoom/offset → world: useViewportControls.ts:79-84; округление при импорте: useVisualEditing.ts:204-207) |
| 66-67 | «Импорт требует выбранной ноды, иначе предложит создать новую» | Неточно — для пути: выбранная нода будет **заменена** на follow_path (с подтверждением), без выбора — создание новой; для актёров новые ноды не создаются вообще (useVisualEditing.ts:216-286,289-346). Исправлено |
| 71-80 | Клавиши: B/G/Ctrl+E/Shift/колесо/ПКМ-пан/кнопки/«По размеру» | Частично WRONG — B/G/Ctrl+E/Shift OK (Modal:496-545); колесо-зум OK (useViewportControls.ts:101-109); **«Правая кнопка мыши — перемещение камеры» неверно: pan = ЛКМ-drag по пустому месту** (Modal:959-989), ПКМ не обрабатывается. Кнопки Zoom-/Zoom+/Fit/Reset есть (Toolbar:58-84). Исправлено |
| 82 | «Панель Сетка тайлов: сетка, привязка, смещение» | Неточно — контролы живут в секции Path Tools: Show Grid/Snap to Grid/Grid Offset X/Y (offsets видны при включённом snap) (Sidebar:158-202); шаг 20px фиксированный. Исправлено |
| 86-87 | Screenshot Output Folder в Edit→Preferences→General | **WRONG** — путь File→Preferences, секция **Editor** (PreferencesModal.tsx:166,241-282); также Help→Advanced→Choose Screenshot Output Folder. Исправлено |
| 89-90 | «Импорт актёров неактивен … выбрана нода Actor Create с ключом» | WRONG по причине — импорт не зависит от выбора; неактивен когда нет реальных (не виртуальных) маркеров, т.е. нет actor_create-нод в графе (Modal:1207,1238; useVisualEditing:301-303). Исправлено |
| 92-93 | «Путь не импортируется … предложит создать новую» | Неточно — при выбранной любой ноде предложит заменить её на follow_path; новую создаёт только без выбора (useVisualEditing.ts:216-283). Исправлено |
| 95-99 | Ссылки «См. также» | OK — все файлы в nav_plan.md |
| — | MISSING: Esc закрывает окно; Reset-кнопка viewport; Path Size Multiplier; speed-индикатор у follow_path | MISSING → добавлено в страницу |

## Итог

- **WRONG/неточности (исправлены):**
  - nodes.md: блокировка Halt (не блокирует); `args`→`arguments` (экспортируется `args`); Tween `to_value`/`from_value` (экспортируются `end_value`/`start_value_override`); UI-лейблы полей (Actor Name/Actor Sprite/Target/Sound·Key вместо Key/Sprite·Object/Target Mark/Track).
  - formats.md: «Export for Engine»→«Export to Game»; `settings.skippable`/`debug`/`end` не пишутся экспортёром (пример и таблица исправлены, добавлена пометка о ручной правке); `.usc.json` не хранит панели; обратный импорт checkpoint-полей принимает и массивы; добавлены недостающие алиасы.
  - ui.md: состав панелей по умолчанию; «кнопка в левом dock»/«кнопка на панели» для Visual Editing; ПКМ-удаление без меню; Bookmarks — список всех нод, одиночный клик; Templates («Save Selection», скрыта); цвета заметок camera/sound; Ctrl-магия в RVE (нет — snap чекбоксом); путь Preferences (File→, Ctrl+P); мёртвые хоткеи Focus Dock убраны, добавлены реальные (Ctrl+O/P/A/C/X/V, Delete, Ctrl+Shift+Z, Ctrl+0); автосейв-файлы; MiniMap-порог вместо тумблера; «Saved» — индикатор, не toast.
  - room-visual-editor.md: убраны «поверх других окон» и «кнопка на панели»; pan — ЛКМ, не ПКМ; импорт пути заменяет выбранную ноду (не «предложит создать при другой ноде»); импорт актёров не зависит от выбора, виртуальные маркеры не импортируются; сетка в секции Path Tools; путь к Screenshot Output Folder; добавлены Ctrl+Z/Y, Esc, Reset.
- **OK без правок:** все 84 ноды присутствуют и описаны с верными полями/дефолтами/опциями; счётчики категорий и цвета; большинство семантических описаний (глубина-manual, camera_track_until_stop→move_active, waittalk-алиас, instant_mode→set_instant, goto→mark_node, block_queue и пр.).
- **UNVERIFIABLE:** внешних URL нет; все утверждения проверены по $E/$P.
- Ограничение user-facing соблюдено: `.tsx`, `requestAnimationFrame`, `userData`, имена компонентов в итоговом тексте страниц не используются (упоминания только в этом отчёте).
