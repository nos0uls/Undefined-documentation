# Фактчек: architecture/rooms.md (ревизия кода 7ee444a)

Источники: `_meta/rooms.txt`, `rooms/*/*.yy`, `Undefinedtale888.yyp`, скрипты/объекты в $P.

| Строка | Утверждение | Вердикт |
|---|---|---|
| 11 | 16 комнат; `rm_init` служебная; 4 меню-комнаты; 3 связанные игровые локации; порядок задаёт `RoomOrderNodes` | OK — rooms/ содержит 16 комнат; меню = `rm_roomMenu`/`rm_savesSelect`/`rm_settings`/`rm_devLoad` (obj_Init/Create_0.gml:181-186); игровые = `rm_playground`/`rm_road_curve`/`rm_uphill_school` |
| 17–32 | Порядок `RoomOrderNodes` (16 имён) | OK — Undefinedtale888.yyp:770-785, совпадает 1:1 |
| 34 | Старт в `rm_init`; F5/F6 → `scr_get_next_game_room()` идёт по `room_next`/`room_previous`, пропуская `scr_room_is_dev_navigation_excluded()` = `__service_menu_rooms` + `rm_init` + `SCREENSHOTS` | OK — scr_get_next_game_room.gml:9-19,22-36; scr_global_debug_hotkeys.gml:50-56 |
| 40 | `rm_init` 1280×980, слой `Instances` есть, `obj_Init` → `room_goto(rm_roomMenu)`; слои `Instances`, `Background` | OK — rm_init.yy:13-16,33-38; obj_Init/Create_0.gml:348-350 |
| 41 | `rm_roomMenu` 1280×960; `obj_menu` запускает `music_menu` через `global.play_music`; слои `Assets_1`, `Instances`, `Instances_1`, `Background` | OK — rm_roomMenu.yy; obj_menu/Create_0.gml:16-18 |
| 42 | `rm_savesSelect` 1280×960; `obj_saveManager`; слои `Instances`, `Instances_1`, `Background` | OK — rm_savesSelect.yy (инстансы: `obj_saveManager`, `obj_menuBGSpriteChanger`) |
| 43 | `rm_settings` 1280×960; `obj_settingsManager`; слои `Instances`, `Instances_1` (без Background) | OK — rm_settings.yy |
| 44 | `rm_devLoad` 320×240; `obj_devLoader` из `RoomCreationCode`; слои `Instances`, `Background` | OK — rm_devLoad.yy (0 инстансов); rm_devLoad/RoomCreationCode.gml:6 |
| 45 | `DevRoom1` 543×240; `obj_player`, `obj_asher`, тесты; слои `Instances_1`, `Instances`, `Assets_2`, `Background` | OK — DevRoom1.yy (10 инстансов) |
| 46 | `rm_playground` 471×320; слои `Assets_1`, `Instances`, `Tiles_3`, `Tiles_4`, `Tiles_2`, `Tiles_1`, `Background` | OK — rm_playground.yy:21-89; оговорка: `Tiles_4` вложен в `Tiles_3`, в таблице указан плоско |
| 47 | `rm_road_curve` 500×340; слоя `Instances` нет; NPC, `obj_asher`, `obj_save`, `obj_sign`, `obj_sheepFountain`, 2×`objRoomChanger`; слои `collis`, `depth`, `Instances_1`, `tree`, `Tiles_3`–`Tiles_6` (вложенные), `road`, `Assets_1`, `Tiles_1` | OK — rm_road_curve.yy:51-139 (39 инстансов) |
| 48 | `rm_uphill_school` 542×240; `Instances` нет; `obj_player`, `obj_asher`, скамейки, триггер; 11 слоёв в указанном порядке | OK — rm_uphill_school.yy:27-85 (15 инстансов; `obj_asher` имеет `ignore:true`, но в .yy есть) |
| 49 | `rm_after_tunnel` 519×240; `Instances` нет; 14 `obj_visualObject`, коллайдеры на `depth`; слои `Tiles_1`, `depth`, `road`, `grass`, `Background` | OK — rm_after_tunnel.yy (35 инстансов, все на `depth`) |
| 50 | `rm_curver` 540×340; `Instances` нет; слой `Trees` пуст; слои `Trees`, `path`, `grass`, `Background` | OK — rm_curver.yy |
| 51 | `rm_idk` 320×240; `Instances` нет; `bush`+`obj_lantern` на `depth`; 7 слоёв в указанном порядке | OK — rm_idk.yy |
| 52 | `rm_cutsceneTest` 2000×1800; `Instances` есть; `obj_cutsceneTest`, `obj_player`, `obj_save` | OK — rm_cutsceneTest.yy |
| 53 | `roomForDialogueTesting` 400×320; `Instances` есть; `textboxTest_scribble` | OK — roomForDialogueTesting.yy |
| 54 | `rm_sound_test` 320×240; `Instances` есть; `obj_sound_test` | OK — rm_sound_test.yy |
| 55 | `SCREENSHOTS` 1366×768; `Instances` есть; `screenshot` из `RoomCreationCode`, очищает `screenshots/` | OK — SCREENSHOTS.yy (0 инстансов); SCREENSHOTS/RoomCreationCode.gml:5; screenshot/Create_0.gml:55-124 (`file_find_first`/`file_delete`) |
| 57–58 | Пять комнат без слоя `Instances`: `rm_after_tunnel`, `rm_curver`, `rm_idk`, `rm_road_curve`, `rm_uphill_school` | OK — rooms.txt + raw .yy |
| 64–71 | Код `scr_layer_ensure_instances()` | OK — scr_layer_ensure_instances.gml:4-10 (в файле табы, в доке пробелы — допустимо) |
| 73–74 | `layer_exists`/`layer_create(0)`; возврат `"Instances"` для `instance_create_layer`; ленивое создание | OK — scr_layer_ensure_instances.gml:5-9 |
| 75 | Список вызовов: `obj_cutsceneManager` (`c_begin`, `cutscene_load_json`), `textboxTest_scribble` (`readDialogue`), dev-спавн `obj_player`, `obj_pointMarker`, менеджеры (`obj_music_ctrl`, `obj_globalManager`, `obj_saveManager`, `obj_inGameMenu`), `RoomCreationCode` `rm_devLoad`/`SCREENSHOTS` | OK (неполный) — все перечисленные верны: c_begin.gml:28, cutscene_load_json.gml:129, readDialogue.gml:13, scr_global_handle_dev_spawn.gml:48, obj_player/Create_0.gml:309 + scr_player_marker_update.gml:14, obj_Init/Create_0.gml:280,322, obj_save/Step_0.gml:50, obj_settingsManager/Create_0.gml:243. Не упомянуты: `obj_settingsManager` (obj_inGameMenu/Step_0.gml:76), `obj_face` (textboxTest_scribble/Create_0.gml:10), `obj_anim` (scr_anim.gml:11), `textboxTest_scribble` из scr_cutscene_classes.gml:2534, scr_global_debug_hotkeys.gml:84, scr_stress_tests (не документируется) |
| 77 | В `rm_road_curve` новый слой `Instances` (depth 0) ляжет между `tree` (−200) и `Tiles_3` (−100) | **WRONG** — rm_road_curve.yy: depth 0 > −100, слой окажется позади `Tiles_3`: между `Tiles_3` (−100) и `road` (300), на одном уровне с вложенным `Tiles_6` (0) |
| 81–95 | «Ключевые инстансы» — все 15 пунктов | OK — сверено с per-room counts; `npc2` наследник `npc1` (npc2.yy:13-15); `obj_asher` наследник `par_interactable` (obj_asher.yy:15-18) |
| 99 | Свойства `objRoomChanger`: `room_name`, `x_position`/`y_position` (`-1` = позиция триггера), `eyes_glow`; снимок в `pending_*` при Collision; persistent `obj_changingRoomsController` в Step | OK — objRoomChanger.yy properties; Collision_obj_player.gml:14-24; Step_0.gml:2-26; obj_changingRoomsController.yy:17 `persistent:true` |
| 101–106 | Карта переходов: playground→road_curve (35,100); road_curve→uphill_school (40,140); road_curve→playground (220,210); uphill_school→road_curve (414,269) | OK — rm_playground.yy:26-29; rm_road_curve.yy:71-74 и 79-81; rm_uphill_school.yy:43-46 |
| 108–115 | Mermaid-диаграмма | OK — соответствует таблице переходов |
| 117 | `rm_init`→`rm_roomMenu` — жёсткий `room_goto` в конце Create при `room == rm_init`; остальное — `objRoomChanger`, сейв (`obj_saveManager` → `room_goto(rm_devLoad)` при devload-фокусе), F5/F6 | OK — obj_Init/Create_0.gml:344-350; obj_saveManager/Step_0.gml:154-156 |
| 121 | `rm_init`: единственный инстанс — persistent `obj_Init`; строит `global.rooms_by_name`, `global.__service_menu_rooms`; исключена из F5/F6 и DEV-LOAD фильтром | OK — obj_Init.yy:15 `persistent:true`; Create_0.gml:181-211; obj_devLoader/Create_0.gml:14,23 |
| 125–127 | Ссылки: `initialization.md`, `../systems/room-transitions.md`, `overview.md` | OK — все файлы существуют в docs_new/, перечислены в nav_plan.md |

## Итог

- **WRONG: 1** — строка 77 (позиция нового слоя `Instances` по depth в `rm_road_curve`).
- Остальное подтверждено; правка — одна строка + опционально дополнение списка вызовов (стр. 75).
