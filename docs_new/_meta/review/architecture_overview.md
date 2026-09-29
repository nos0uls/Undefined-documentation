# Review: architecture/overview.md

Фактчек по коду ревизии 7ee444a. Источники: `_meta/objects.txt`, `_meta/globals.txt`,
`_meta/nav_plan.md`, `objects/*/*.gml`, `objects/*/*.yy`, `scripts/*/*.gml`, `wc -l`.

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 21 | Инициализация: `obj_Init/Create_0.gml`, `scr_constants` | OK — obj_Init/Create_0.gml:32 вызывает `scr_constants()`; оба файла существуют |
| 22 | Глобальное состояние/UI-блокировка: `obj_globalManager/*`, `scr_checkUIBlocking` | OK — объект и скрипт существуют; кэш-блокировка — scr_checkUIBlocking.gml:15-36 |
| 23 | Ввод: `scr_inputApi`, `scr_buildInputMap` (в `scr_settingsManager`), `global.input_map` | OK — scr_buildInputMap определён в scr_settingsManager.gml:442; input_map создаётся в obj_Init/Create_0.gml:94 |
| 24 | Игрок: `obj_player/*`, `scr_player_*`, `par_actor` | OK — 9 скриптов scr_player_* существуют; obj_player parent = par_actor (objects.txt:354) |
| 25 | Коллизии/depth: `par_depth` (`depth = -y`), `obj_collider`, `obj_slopeCollider`, `scr_collision_resolve`, `scr_player_slope_resolve` | OK — все существуют; `depth = -y` — par_depth/Step_0.gml:40 (auto-режим FSM) |
| 26 | Переходы: `objRoomChanger`, `obj_changingRoomsController`, `scr_room_fade_update` | OK — scr_room_fade_update вызывается из obj_changingRoomsController/Step_0.gml:2 |
| 27 | Диалоги: `textboxTest_scribble`, `readDialogue`, `obj_face`, `datafiles/Dialogues/*.yarn` | OK — все существуют; в datafiles/Dialogues/ лежат fountain/testChoices/testDialogue/testDialogueBlue.yarn |
| 28 | Взаимодействие: `par_interactable`, `scr_interaction` (`interactionWithNPCsOrObjects`), `obj_pointMarker` | OK — scr_interaction — функция в interactionWithNPCsOrObjects.gml:20; par_interactable и obj_pointMarker существуют |
| 29 | Катсцены: `obj_cutsceneManager`, `scr_cutscene_classes`, `cutscene_action_factory`, `c_begin`/`c_play`/`c_end`, `cutscene_load_json` | OK — все скрипты существуют (scripts/c_begin, c_play, c_end, cutscene_load_json) |
| 30 | Инвентарь/статы: `scr_inventory_init`, `script_items`, `scr_stats_recalc` | OK — scr_stats_recalc — функция внутри scr_inventory_init.gml:67 (не отдельный скрипт, но существует) |
| 31 | Сейвы: `scr_saveLoad`, `scr_saveSave`, `scr_game_state`, `obj_saveManager`, `obj_save` | OK — все существуют; obj_saveManager/Step_0.gml:76,131 зовёт scr_saveSave/scr_saveLoad |
| 32 | Музыка/SFX: `scr_music_init`, `obj_music_ctrl`, `scr_SFXPlay`, `scr_global_on_room_change` | OK — все существуют |
| 33 | UI/меню: `obj_menu`, `obj_inGameMenu`, `obj_settingsManager`, `obj_p3r_*`, `scr_ui_*`, `scr_p3r_*` | OK — 5 объектов obj_p3r_*; scr_ui_* (3 шт.) и scr_p3r_* (6 шт.) существуют |
| 34 | Debug: `scr_global_debug_hotkeys`, `scr_debug_activation_check`, `obj_devLoader`, `screenshot`, `scr_test_*`, `scr_stress_tests` | OK — все существуют |
| 40–44 | Mermaid: `obj_Init` создаёт `obj_globalManager`, `obj_music_ctrl`; строит `input_map`; грузит `testDialogue.yarn`; заполняет инвентарь | OK — obj_Init/Create_0.gml:321-323 (GM), :279-281 (MC), :94 (input_map), :275 (ChatterboxLoadFromFile), :342 (scr_inventory_init) |
| 45–47 | Mermaid: GM инвалидирует кэш UIB; смена комнаты → музыка; тикает `cutscene_runtime_step`/`emote_step` | OK — Step_0.gml:13-14 (dirty-флаги), :24-26 (scr_global_on_room_change → треки), :44-45 (emote_step/cutscene_runtime_step — функции в scr_emote_system.gml:149 и scr_cutscene_classes.gml:1518) |
| 48–50 | Mermaid: Player читает input_map, спрашивает UIB, создаёт pointMarker | OK — scr_input_* читают global.input_map (scr_inputApi.gml:12-16); scr_player_ui_blocking.gml:10 → scr_checkUIBlocking; marker создаётся obj_player/Create_0.gml:309 |
| 51–52 | Mermaid: `par_interactable → scr_interaction → readDialogue → textboxTest_scribble`; TB → Chatterbox+Scribble → Yarn | OK — interactionWithNPCsOrObjects.gml:94 → readDialogue; readDialogue.gml:13 создаёт textboxTest_scribble; TB использует Chatterbox (Draw_64.gml:9,41) и scribble_typist (Create_0.gml:20) |
| 53–56 | Mermaid: CS → factory/classes/player; persist/fade → музыка | OK — ActionMusicPlay имеет `_persist`/`_fade` (cutscene_action_factory.gml:655-679); persist-логика — scr_global_on_room_change.gml:33-45; snapshot музыки — scr_cutscene_classes.gml:821-835 |
| 57 | Mermaid: `objRoomChanger` collision → отложенный старт `obj_changingRoomsController` | OK — Collision_obj_player.gml ставит `pending_change`, Step_0.gml создаёт контроллер на `__CUTSCENE_TRANSITION_DEPTH` |
| 58–59 | Mermaid: saveManager/save → scr_saveLoad/scr_saveSave → `save*.txt`, `game_state.dat`; инвентарь сериализуется в сейв | OK — obj_Init/Create_0.gml:69 (`game_state.dat`); слоты `_slot + ".txt"` (:239); inventory_serialize → scr_saveSave.gml:66-67 |
| 71 | Begin Step: `o_SharedTweener`, `obj_player` (Step_1), `textboxTest_scribble`, `obj_menuTest`, `obj_p3r_*`; `__room_born`/`__dedup_survivor`; тик TGMX | OK — objects.txt: Begin Step у o_SharedTweener (:37), obj_player (:360), textboxTest_scribble (:547), obj_menuTest (:243), всех obj_p3r_* (:270,287,304,321,338); метки — obj_player/Step_1.gml:7,11; TGMX-тик — o_SharedTweener/Step_1.gml |
| 72 | Step: перечень объектов и содержимое тиков | OK — все перечисленные имеют Step (objects.txt). GM: dirty-флаги :13-14, gamepad :17, смена комнаты :23, debug :34,38, dev-spawn :41, emote/cutscene :44-45, playtime :62-66, scr_callMenuInit :73. Player: UI-блок → movement → animation → facing → marker → event_inherited (Step_0.gml:6-27). `par_depth` FSM — Step_0.gml:11-43. Замечание: пропуск по `back` — только для `skippable`-катсцен (obj_cutsceneManager/Step_0.gml:7) — уточнено на странице |
| 73 | End Step: `obj_player` (Step_2), `obj_globalManager` (Step_2), `obj_face`, `o_SharedTweener`, `obj_menuTest`, `obj_p3r_*`; камера с клампом и `cutscene_camera_override`; `global.camera_x/y` после движения | OK — objects.txt: End Step у obj_player (:361), obj_globalManager (:186), obj_face (:175), o_SharedTweener (:36), obj_menuTest (:244), obj_p3r_*; камера — obj_player/Step_2.gml:3-15 (exit при `global.cutscene_camera_override`); camera_x/y — obj_globalManager/Step_2.gml:8-10 |
| 74 | Draw: `obj_changingRoomsController`, `obj_cutsceneManager`, `obj_menuBGSpriteChanger`, `obj_menuTest`, `obj_p3r_*`; фейды на `__CUTSCENE_TRANSITION_DEPTH`; фоны меню | OK — все имеют Draw (objects.txt:105,125,233,245 и p3r); `__CUTSCENE_TRANSITION_DEPTH` — objRoomChanger/Step_0.gml:21. MINOR: у `obj_cutsceneTest` тоже есть Draw (objects.txt:139) — тестовый объект, опущен осознанно |
| 75 | Draw GUI: перечень из 15 объектов; «диалоговое окно (Scribble) и портрет» | OK по списку событий (objects.txt). Уточнено: Draw_64 `obj_face` — заглушка `exit;` (файл из одной строки); портрет рисует `textboxTest_scribble` по `global.current_sprite` (Draw_64.gml:123,142), а `obj_face` лишь выбирает спрайт в End Step. MINOR: `obj_cutsceneTest` (Draw GUI, objects.txt:140) опущен — тестовый объект. F9-панель музыки — obj_music_ctrl/Draw_64.gml:2-3 |
| 76 | Draw GUI Begin/End, Pre/Post Draw: `obj_menuTest`, `obj_p3r_*` — «шейдерный блюр фона» | WRONG — набор событий верен (objects.txt:247-250, 274-277 и т.д.), но блюра нет: меню применяет `shd_grayscale` к `application_surface` (obj_inGameMenu/Draw_64.gml:15-19, scr_menu_shader_guard.gml), `obj_p3r_background` рисует surface с `shd_p3r_water` — хроматическая аберрация (Draw_64.gml:62-67). Блюр-шейдера в `shaders/` нет |
| 79–82 | Game End (`Other_3`): `global.__total_playtime_seconds` → `game_state.dat` через `scr_game_state_save`; `obj_cutsceneManager` — Room Start/Room End/CleanUp, persistent | OK — Other_3.gml:4-9; objects.txt:127-129 (Room Start/End, CleanUp), persistent True (:121) |
| 86 | «Из 53 объектов `persistent: true` у девяти» | OK — objects.txt:4 «Объектов: 53»; persistent=True ровно у перечисленных девяти |
| 90 | `obj_Init`: инициализирует в `rm_init`, переходит в `rm_roomMenu`, дедуп по `global.__init_done` | OK — Create_0.gml:8-14 (дедуп), :348-349 (room_goto), :354 (`__init_done` — последняя строка) |
| 91 | `obj_globalManager`: тик; дубли уничтожаются в Create | OK — Create_0.gml:8-11 (`instance_number > 1` → destroy) |
| 92 | `obj_player`: дедуп `__room_born`/`__dedup_survivor`, `global.obj_player` | OK — Create_0.gml:21-23,58-62,72,235; Step_1.gml:7-11 |
| 93 | `obj_pointMarker`: создаётся/уничтожается с игроком (`marker_id`, CleanUp) | OK — Create_0.gml:309-314 (создание), CleanUp_0.gml:2-4 (destroy) |
| 94 | `obj_music_ctrl`: фейды/слои каждый кадр; создаётся из `obj_Init` | OK — Step_0.gml:3-4; obj_Init/Create_0.gml:279-281 |
| 95 | `obj_cutsceneManager`: живёт между комнатами ради переходов внутри катсцены | OK — persistent True + Room Start/End события (objects.txt:121,127-128) |
| 96 | `obj_changingRoomsController`: держит фейд через границу комнаты | OK — persistent True (objects.txt:102); scr_room_fade_update в Step |
| 97 | `o_SharedTweener`: синглтон TweenGMS, тик в Begin/End Step | OK — objects.txt:33-41; Step_1/Step_2 содержат цикл TGMX |
| 98 | `screenshot`: «раннер тайловых скриншотов комнат (debug/CI-инструмент)» | UNVERIFIABLE (частично) — тайловый раннер подтверждён (Create_0.gml:1-3, очередь комнат/тайлов); использование в CI не подтверждено — `.github/` в репо нет. Смягчено до «debug-инструмент» |
| 101–103 | Сирота: `obj_player/Draw_0.gml` на диске, Draw нет в `eventList` | OK — файл objects/obj_player/Draw_0.gml существует; objects.txt:357-362 — Create, Step, Begin Step, End Step, CleanUp без Draw |
| 107–108 | «Четыре из пяти самых больших — внешние библиотеки» | WRONG — из топ-5 внешних три: TGMX_System, __scribble_class_element, __scribble_gen_2_parser; scr_cutscene_classes и cutscene_action_factory — свои. Исправлено на «три из пяти» |
| 110–126 | Таблица `wc -l` (15 файлов, все числа) | OK — все 15 чисел совпадают точно; следующий файл — scr_inputApi 588 < 620, топ-15 полный. «более 130 объявлений function» для scr_cutscene_classes — OK (194 объявления `function X(`, 135 уникальных имён, 69 `constructor`) |
| 121 | `obj_cutsceneManager/Create_0.gml` содержит `start_cutscene`, `finish_cutscene`, `cutscene_step_tick`, трекинг нод | OK — методы в Create_0.gml (mark_node_reached :39 и далее); вызовы — Step_0.gml:8,22 |
| 130–132 | «Все `global.*` объявляет `obj_Init/Create_0.gml`» | WRONG (преувеличение) — по globals.txt: 124 из 187 имён пишутся впервые в цепочке инициализации (obj_Init 71, scr_music_init 41, scr_inventory_init 10, scr_constants 2); остальные ~63 создаются лениво (scr_global_music_update_current 15, scr_stress_tests 5, obj_cutsceneManager 4, TGMX_System 1, obj_face/Step_2 — `global.current_sprite` и др.). Исправлено. «`__init_done` — последняя строка» — OK (:354); «`obj_globalManager` инициализации не содержит» — OK (Create_0.gml без записей `global.*`) |
| 133–134 | «Менеджеры-одиночки … дедуп через `instance_number` в Create» | WRONG (обобщение) — `instance_number`-дедуп есть только у `obj_globalManager` (Create_0.gml:8), `obj_Init` (:10) и `obj_pointMarker` (Create_0.gml:12). `obj_music_ctrl`, `obj_cutsceneManager`, `obj_changingRoomsController` дедупа в Create не имеют — защита `instance_exists` в точках создания (obj_Init/Create_0.gml:279; objRoomChanger/Step_0.gml:10). Исправлено |
| 135–137 | Ввод через карту действий: `scr_input_down`/`pressed`/`repeater`, `global.input_map`, геймпад-слой | OK — функции в scr_inputApi.gml:274,304,348; gamepad — scr_input_gamepad_update :141 |
| 138–140 | UI-блокировка: `scr_ui_objects_list`, флаги катсцены, кэш на кадр через dirty-флаги от `obj_globalManager` | OK — scr_ui_objects_list — scr_checkUIBlocking.gml:51; dirty-флаги — obj_globalManager/Step_0.gml:13-14 |
| 141–142 | Data-driven: `.yarn` (Chatterbox), JSON через `cutscene_action_factory`, Scribble-разметка | OK — datafiles/Dialogues/*.yarn; factory `f[$ "..."]` handlers (82 шт.); scribble_typist в textboxTest_scribble |
| 143–144 | `global.entity_state` → сейв; `global.room_flags` — сессионные | OK — scr_saveSave.gml:100-107, scr_saveLoad.gml:122-137,234; room_flags — obj_Init/Create_0.gml:25-29 («в сейв не входят»), сброс — scr_saveLoad.gml:326 |
| 148–153 | Ссылки «См. также»: initialization.md, global-state.md, object-hierarchy.md, rooms.md, ../systems/input.md, ../cutscenes/overview.md | OK — все файлы существуют в docs_new/ и есть в nav_plan.md |
| 19–34, 148–153 | Все ссылки страницы | OK — все цели существуют (initialization, global-state, object-hierarchy, rooms, systems/*, cutscenes/overview); соответствуют nav_plan.md |

## MISSING / неточности низкого приоритета

- `obj_cutsceneTest` имеет Step/Draw/Draw GUI (objects.txt:135-140), но опущен в таблице кадра — тестовый объект, опускание допустимо.
- `obj_face/Draw_64.gml` — файл-заглушка `exit;`: Draw GUI событие в `eventList` есть, но портрет рисует `textboxTest_scribble` (Draw_64.gml:142 по `global.current_sprite`). Уточнено на странице.
- `screenshot.yy` объявлен persistent, но `screenshot/Create_0.gml:334` при финиш-ветке выставляет `persistent = false` — поведение на странице не требует правки (persistent нужен только на время обхода комнат).

## Итог

- WRONG: 4 (строки 76 «блюр», 107-108 «четыре из пяти», 130-132 «все global.*», 133-134 «дедуп instance_number»).
- UNVERIFIABLE: 1 (строка 98 «CI-инструмент» — CI-часть убрана).
- Остальные утверждения подтверждены по коду и `_meta/*.txt`; ссылки валидны.
