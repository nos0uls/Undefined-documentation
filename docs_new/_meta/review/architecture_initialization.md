# Фактчек: architecture/initialization.md (ревизия кода 7ee444a)

Источники: `objects/obj_Init/Create_0.gml` (354 строки, порядок сверен построчно), `rooms/rm_init/rm_init.yy`, `objects/obj_Init/obj_Init.yy`, `objects/obj_globalManager/{yy,Create_0,Step_0,Step_2,Draw_64,Other_3}`, `scripts/scr_defaultLoad/scr_defaultLoad.gml`, `scripts/scr_get_next_game_room/scr_get_next_game_room.gml`, `Undefinedtale888.yyp`, `scripts/scr_settingsManager/scr_settingsManager.gml`, `scripts/scr_inventory_init/scr_inventory_init.gml`, `scripts/scr_music_init/scr_music_init.gml`, `scripts/scr_constants/scr_constants.gml`, `scripts/c_cmd/c_cmd.gml`, `objects/obj_menu/Create_0.gml`, `objects/obj_saveManager/Step_0.gml`, `objects/obj_player/Create_0.gml`, `scripts/scr_global_debug_hotkeys/scr_global_debug_hotkeys.gml`, `scripts/scr_global_handle_dev_spawn/scr_global_handle_dev_spawn.gml`, `scripts/scr_layer_ensure_instances/scr_layer_ensure_instances.gml`, `scripts/scr_global_toggle_fullscreen/scr_global_toggle_fullscreen.gml`, `scripts/scr_roomFromName/scr_roomFromName.gml`, `scripts/scr_game_state/scr_game_state.gml`, `scripts/scr_saveLoad/scr_saveLoad.gml`, `sounds/`, `objects/obj_music_ctrl/obj_music_ctrl.yy`, `objects/obj_player/obj_player.yy`, `objects/obj_devLoader/Create_0.gml`.

| Строка | Утверждение | Вердикт |
|---|---|---|
| 13 | `rm_init` — первая комната, единственный инстанс `obj_Init`, Create инициализирует `global.*`, persistent-менеджеры, переход в `rm_roomMenu` | OK — Undefinedtale888.yyp:770; rm_init.yy:8-15 (один инстанс); Create_0.gml:348-350 |
| 17 | `rm_init` — первый узел `RoomOrderNodes` | OK — Undefinedtale888.yyp:769-770 |
| 17 | `obj_globalManager`/`obj_music_ctrl` через `instance_create_layer` на слой `"Instances"` (`scr_layer_ensure_instances`) | OK — Create_0.gml:279-281,321-323; scr_layer_ensure_instances.gml:4-9 (возвращает имя `"Instances"`) |
| 30 | Mermaid: `gpu_set_texfilter(false)`, `scr_constants()` | OK — Create_0.gml:20,32 (между ними clean_state/room_flags — упрощение) |
| 31 | Mermaid: `scr_game_state_load()` + `scr_loadSettings()` + `scr_applySettings()` | OK — Create_0.gml:71,85,87 |
| 32 | Mermaid: `scr_buildInputMap()`, кэш метаданных слотов | OK — Create_0.gml:94,234-258 |
| 33 | Mermaid: `scr_music_init()`, `cutscene_register_chatterbox_functions()` | OK — Create_0.gml:266,270 |
| 34 | Mermaid: `ChatterboxLoadFromFile("testDialogue.yarn")` | OK — Create_0.gml:275 |
| 35 | Mermaid: `obj_music_ctrl` persistent | OK — Create_0.gml:279-281; obj_music_ctrl.yy:17 |
| 36 | Mermaid: `obj_globalManager` persistent | OK — Create_0.gml:321-323; obj_globalManager.yy:19 |
| 37 | Mermaid: `global.flag`/`plot`/`entity_state`, `scr_inventory_init()` | OK — Create_0.gml:330-342 |
| 38 | Mermaid: `room_goto(rm_roomMenu)` | OK — Create_0.gml:349 |
| 39 | Mermaid: `obj_menu.Create` → `global.play_music(music_menu)` | OK — obj_menu/Create_0.gml:17-18 (под гардом `music_current != music_menu`) |
| 40 | Mermaid: кнопка «Играть» → `room_goto(rm_savesSelect)` | OK — obj_menu/Create_0.gml:10 |
| 41 | Mermaid: `scr_saveLoad()` либо `scr_defaultLoad()` → `room_goto` | OK — obj_saveManager/Step_0.gml:129-138; scr_saveLoad.gml:341; scr_defaultLoad.gml:58 |
| 42 | Mermaid: Step вызывает `scr_global_handle_dev_spawn()` при `__dev_spawn` | OK — Step_0.gml:43 (вызов безусловный, гард внутри — scr_global_handle_dev_spawn.gml:4) |
| 49 | Размер 1280×980 | OK — rm_init.yy:34,37 (Width 1280, Height 980) |
| 50 | `Instances` depth 0; `Background` depth 100, заливка `0xFF000000` | OK — rm_init.yy:13,16 (colour 4278190080 = 0xFF000000) |
| 51 | `obj_Init` (`inst_369CFEE7`, 640×352) — ровно один | OK — rm_init.yy:9,14 |
| 52 | `enableViews: false` | OK — rm_init.yy:53 |
| 54 | `rm_init` не в `__service_menu_rooms`; `scr_room_is_dev_navigation_excluded` → `true`; F5/F6 и DEV-LOAD пропускают | OK — Create_0.gml:181-186; scr_get_next_game_room.gml:17; obj_devLoader/Create_0.gml:14,23 (также используется objects/screenshot/Create_0.gml:93 — не упомянуто, но и не оспорено) |
| 54 | Переход зашит в конце `obj_Init.Create`: `room_goto(rm_roomMenu)` | OK — Create_0.gml:344-350 |
| 58 | `persistent` в `.yy` и первой строкой Create; без спрайта; единственное событие Create | OK — obj_Init.yy:15,32,5; Create_0.gml:4 |
| 58 | Гард `__init_done`: выход + дедуп; флаг последней строкой | OK — Create_0.gml:8-14,354 |
| 62 | Шаг 1: `gpu_set_texfilter(false)` | OK — Create_0.gml:20 |
| 63 | Шаг 2: `global.clean_state`, `global.room_flags` | OK — Create_0.gml:23,29 |
| 64 | Шаг 3: `scr_constants()` → `global.DIR`, `global.SETTINGS_STATE` | OK — Create_0.gml:32; scr_constants.gml:13-27 |
| 65 | Шаг 4: `settings_file`, `_is_first_launch`, `debug`, `debug_show_music` | OK — Create_0.gml:35-40 |
| 66 | Шаг 5: аудио-дефолты + плейсхолдеры | OK — Create_0.gml:45-54 |
| 67 | Шаг 6: `__window_prev_*`, `__window_borderless_active` | OK — Create_0.gml:60-64 |
| 68 | Шаг 7: `scr_game_state_load()` → `game_state_file`, `game_state`, playtime-счётчики | OK — Create_0.gml:69-81; scr_game_state.gml:22 |
| 69 | Шаг 8: `scr_loadSettings()` → `scr_applySettings()` | OK — Create_0.gml:85-89; scr_settingsManager.gml:80,262 (apply также трогает окно/громкость/debug/input_map) |
| 70 | Шаг 9: `scr_buildInputMap()` → `input_map`, repeater, gamepad-оси | OK с неточностью — Create_0.gml:94 вызывает `scr_buildInputMap(global.player_settings)`; сигнатура требует аргумент (scr_settingsManager.gml:442). `input_map` также создаётся внутри `scr_applySettings` (строка 336) |
| 71 | Шаг 10: `ui_snd_select`, `ui_sfx_map` — все `snd_text_ch1`, «единственный SFX-ассет проекта» | **WRONG** — в проекте есть второй sound-ассет `snd_wobble` (sounds/snd_wobble/snd_wobble.yy), хотя и не вызываемый из кода. Формулировка воспроизводит устаревший код-комментарий Create_0.gml:106 |
| 72 | Шаг 11: `global.__dev_spawn*`, `obj_player`, `__next_spawn_*`, `__transition_safety_frames` | OK с неточностью — `__dev_spawn_facing` намеренно НЕ инициализируется (Create_0.gml:119-125); wildcard `__dev_spawn*` это размывает |
| 73 | Шаг 12: debug-флаги | OK — Create_0.gml:138-147 |
| 74 | Шаг 13: катсцен-глобалы | OK — Create_0.gml:151-163 (все 9 имён на месте) |
| 75 | Шаг 14: `menu_return_focus`, `ingame_menu_return_index`, `__ui_blocking_*`; dirty-флаги «сбрасывает» `obj_globalManager` | OK с неточностью — глобалы верны (Create_0.gml:166-174), но менеджер не «сбрасывает», а инвалидирует: выставляет dirty=`true` (Step_0.gml:14-15) |
| 76 | Шаг 15: `__service_menu_rooms`, `is_menu_room()`, `rooms_by_name` | OK — Create_0.gml:181-211 |
| 77 | Шаг 16: `current_save_slot`/`last_played_save_slot` (приоритет game_state→last_played→"save1"), кэш метаданных | OK — Create_0.gml:218-258; scr_saveLoad.gml:359,372,391 |
| 78 | Шаг 17: `scr_music_init()` → `global_emote_system`; `music_*`; `play_music*` | OK с неточностью — `global.global_emote_system` создан инлайн (Create_0.gml:262), НЕ внутри `scr_music_init`; остальное верно (scr_music_init.gml:30-117,177+) |
| 79 | Шаг 18: `cutscene_register_chatterbox_functions()` → `__cutscene_chatterbox_registered`; `testDialogue.yarn` | OK с неточностью — флаг создаётся инлайн `false` (Create_0.gml:269), функция лишь выставляет `true` (c_cmd.gml:~205); `ChatterboxLoadFromFile` — отдельный вызов (Create_0.gml:275), не часть функции |
| 80 | Шаг 19: `obj_music_ctrl` если ещё нет | OK — Create_0.gml:279-281 |
| 81 | Шаг 20: `show_notification()`, first-launch окно/центрирование/`scr_saveSettings` | OK — Create_0.gml:284-317 |
| 82 | Шаг 21: `obj_globalManager` если ещё нет | OK — Create_0.gml:321-323 |
| 83 | Шаг 22: `scr_inventory_init()` → `flag`/`plot`/`entity_state`; инвентарь 8 слотов, `equipped_*`, `stat_*`, `player_name`, `camera_x/y`, `current_sprite/voice` | ЧАСТИЧНО **WRONG** — `flag`/`plot`/`entity_state` инициализируются инлайн в Create_0.gml:330-339 ДО вызова, а не внутри `scr_inventory_init`; содержимое инвентаря верно (scr_inventory_init.gml:5-58: 8 слотов, 3 предмета, equipped, stat_*, player_name, camera_x/y, current_sprite/voice) |
| 84 | Шаг 23: `room_goto(rm_roomMenu)` при `room == rm_init`, последний вызов | OK — Create_0.gml:348-350 (за ним только присваивание `__init_done`) |
| 85 | Шаг 24: `__init_done = true` | OK — Create_0.gml:354 |
| 88 | `global.default_settings` — единственный глобал вне `obj_Init`; top-level присваивание в scr_settingsManager.gml | OK — scr_settingsManager.gml:7-11; grep по топ-левел `global.` в scripts/ подтвердил единственность; `scr_loadSettings` копирует его как базу (строки 84-88) |
| 92 | «Создаётся из `obj_Init` (шаг 19)» | **WRONG** — `obj_globalManager` создаётся на шаге 21 таблицы (Create_0.gml:321-323); шаг 19 — `obj_music_ctrl` |
| 92–102 | persistent; события yy | OK — obj_globalManager.yy:5-9,19 |
| 96 | Create: дедуп `instance_number>1`; `current_room`; `notification_*`; `cutscene_runtime_tweens/shakes/spins/jumps`; struct `cutscene_runtime_fade` | OK — obj_globalManager/Create_0.gml:8-37 |
| 97 | Step: гард `__init_done`; инвалидация `__ui_blocking_*`; `scr_input_gamepad_update`; детект смены комнаты → `scr_global_on_room_change` + `scr_room_entry_check`; `scr_debug_activation_check`; `scr_global_debug_hotkeys`; `scr_global_handle_dev_spawn`; `scr_global_handle_notifications`; `emote_step`; `cutscene_runtime_step`; Q в debug; `scr_global_transition_safety`; playtime вне меню; `scr_callMenuInit` | OK — Step_0.gml:7-74; scr_global_toggle_fullscreen.gml:4 (клавиша Q); порядок совпадает |
| 98 | End Step: `camera_x/y` из `view_camera[0]`; пропуск без views | OK — Step_2.gml:7-11 |
| 99 | Draw GUI: уведомления, F1/F2/F3, `emote_draw_gui`, `cutscene_runtime_draw_gui` | OK — Draw_64.gml:48-58,63-91,94-98,101-158,160-161 |
| 100 | Game End: `total_playtime_seconds` → `game_state.dat` через `scr_game_state_save`; пропуск при `clean_state` | OK — Other_3.gml:4-10 |
| 102 | Нет Room Start; смена комнаты — сравнение `room != current_room`; спавн через `__dev_spawn` | OK — yy: eventType 7 только num 3 (Game End); Step_0.gml:22-32,43 |
| 105 | `obj_Init` только расстановкой в `rm_init`; программных `instance_create` нет; Step-гард по `__init_done` | OK — grep: `obj_Init` только в rm_init.yy, `instance_create*` для него нет; Step_0.gml:7-9 |
| 109 | `scr_defaultLoad` вызывается из `obj_saveManager/Step_0.gml` при пустом слоте | OK — Step_0.gml:132-137 (`!current_save.exists`); единственный вызов в проекте |
| 111 | Проверка `scr_roomFromName("rm_uphill_school")` + `room_exists`; при битом: снять `__next_spawn_*`, warning, `return false`, меню открыто | OK — scr_defaultLoad.gml:17-18,68-76; obj_saveManager/Step_0.gml:147-153 |
| 112 | Сброс `__save_playtime_seconds`/`flag`/`plot`/`entity_state`/`room_flags`/`__interacted_targets` + `scr_inventory_init()` + Chatterbox в `try` | OK — scr_defaultLoad.gml:26-40 |
| 113 | `__next_spawn_*` = (377,187) `DIR.DOWN`; читает Create `obj_player` | OK — scr_defaultLoad.gml:12-14,44-46; obj_player/Create_0.gml:197-221 |
| 114 | Уничтожает `obj_player` и `obj_changingRoomsController` | OK — scr_defaultLoad.gml:50-56 |
| 115 | `room_goto(rm_uphill_school)` + страховочный `__dev_spawn` | OK — scr_defaultLoad.gml:58-67; handler: scr_global_handle_dev_spawn.gml:4,18-58 |
| 117 | Ссылка `../systems/save-system.md` | OK — nav_plan.md:31 |
| 121 | `scr_get_next_game_room(direction)`: `room_next`/`room_previous`, фильтр `__service_menu_rooms` + `rm_init` + `SCREENSHOTS` | OK — scr_get_next_game_room.gml:9-35; комната SCREENSHOTS существует (rooms/SCREENSHOTS) |
| 121 | Единственный вызов — `__debug_jump_room` в `scr_global_debug_hotkeys` (F5/F6), `__dev_spawn` с undefined-координатами → центр | OK — grep: вызов только scr_global_debug_hotkeys.gml:7; undefined → центр комнаты (строки 17-18, scr_global_handle_dev_spawn.gml:13-14). `obj_devLoader` фильтр использует напрямую, функцию не вызывает — утверждение верно |
| 125 | `obj_player` persistent | OK — obj_player.yy:22 |
| 127 | `__init_done == true` к Create игрока; `room_goto` отложен до конца события | OK — семантика движка + код-комментарий Create_0.gml:345-347 |
| 128–129 | Все `global.*` из таблицы; существуют `obj_globalManager`, `obj_music_ctrl` | OK — Create_0.gml:279-323 (созданы до `room_goto`) |
| 130 | `__next_spawn_*` читаются и обнуляются Create игрока; иначе `DIR.UP` | OK — obj_player/Create_0.gml:197-228 |
| 131 | `global.obj_player = id` «в конце своего Create» | НЕТОЧНО — строка 235 из 320: до unstuck-поиска (263-298) и создания маркера (309-320). Не последняя операция Create |
| 135–141 | Ссылки «См. также»: global-state, rooms, object-hierarchy, save-system, music, input, debug-and-testing | OK — все в nav_plan.md (architecture/:19-21, systems/:25,31-34) |
| 143 | Комментарий sources | OK — все перечисленные файлы читались и подтверждают содержимое |

## Итог

- **WRONG**: 2 места — строка 71 («единственный SFX-ассет»: есть `snd_wobble`), строка 92 («шаг 19» → шаг 21).
- **Частично неточно**: 6 мест — строки 70 (аргумент `scr_buildInputMap`), 72 (`__dev_spawn_facing` не инициализируется), 75 («сбрасывает» → «выставляет»), 78 (`global_emote_system` инлайн), 79 (флаг и `ChatterboxLoadFromFile` — отдельные строки), 83 (`flag`/`plot`/`entity_state` инлайн, не в `scr_inventory_init`), 131 («в конце Create» неточно).
- **UNVERIFIABLE / MISSING**: нет.
