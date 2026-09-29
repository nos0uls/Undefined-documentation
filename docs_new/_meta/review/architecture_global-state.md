# Ревью: architecture/global-state.md

Код-ревизия: `7ee444a` ($P, read-only). Источник имён: `_meta/globals.txt` (187 уникальных). Метод: точечная сверка ~70 глобалов по коду (init, писатели, читатели, сейв) + полный diff имён страницы против globals.txt.

## Покрытие

- Все 187 имён из `globals.txt` учтены: 177 реальных глобалов в таблицах (включая сгруппированные строки `menu_particle_color_1/2/3`, `__dev_spawn_x/__dev_spawn_y`, `__next_spawn_x/y/facing`, `__window_prev_x/y/w/h`), 10 артефактов без `first_write` — в таблице «Динамические и мёртвые имена». Пропусков нет.
- Все `__`-имена (57) перечислены в сворачиваемом списке раздела «Приватные глобалы», по подсистемам корректно.
- Все 20 глобалов-функций музыкального API присутствуют, строки определений сверены по `scr_music_init.gml`.

## Таблица проверки

Строка — номер строки в `docs_new/architecture/global-state.md`.

| Строка | Утверждение | Статус |
|--------|-------------|--------|
| 13 | 187 имён, init-центр `obj_Init` + `scr_constants`/`scr_music_init`/`scr_inventory_init` | OK (globals.txt:4; obj_Init/Create_0.gml:32,266,342) |
| 17-19 | Легенда колонок, `function`-глобалы, `__`-конвенция | OK |
| 23 | `scr_constants` «запрещает» запись в поля — по соглашению, записей нет | OK (scr_constants.gml:8-9; writes=1 по globals.txt) |
| 27 | `DIR` — struct {RIGHT:0,LEFT:1,UP:2,DOWN:3}, scr_constants:14 | OK (scr_constants.gml:14-19) |
| 28 | `SETTINGS_STATE` {ROOT,CATEGORY,REBIND,CONFIRM_RESET}, :21 | OK (scr_constants.gml:21-26) |
| 29 | `P3R_COLORS` lazy, scr_p3r_palette:6, читают `obj_p3r_*` Draw | OK (scr_p3r_palette.gml:4-6; obj_p3r_*/Draw_64:4) |
| 30 | `default_settings` — top-level scr_settingsManager:11, до obj_Init | OK (scr_settingsManager.gml:8-11) |
| 31 | `input_repeater_defaults` {delay,interval}, obj_Init:97 | OK (:97 `{delay:200, interval:120}`) |
| 32 | `ui_snd_select` sound, :103; читают obj_devLoader, scr_SFXPlay | OK (:103 snd_text_ch1; obj_devLoader/Step_0:12,20; scr_SFXPlay:36-37,64) |
| 33 | `ui_sfx_map` struct ключ→sound, :108; читает scr_SFXPlay | OK (:108-115; scr_SFXPlay:17-19) |
| 34 | `__service_menu_rooms` array имён, :181; читает is_menu_room | OK (:181-186, :191-192) |
| 35 | `rooms_by_name` struct имя→room, :202; читает obj_devLoader | OK (:202-211; obj_devLoader/Create_0:11-15) |
| 36 | `game_state_file` string, :69 | OK; **MISSING** читатель `scr_resetGameToDefault` (scr_resetGameToDefault.gml:16) |
| 37 | `settings_file` string, :35 | OK (:35-36; scr_settingsManager.gml:95,100,222) |
| 38 | `menu_particle_color_1/2/3` colour, scr_p3r_particles:9-11, lazy | OK (scr_p3r_particles.gml:8-11) |
| 39 | `TGMX` struct, TGMX_System:121 | OK (TGMX_System.gml:121) |
| 40 | `_scribble_debug` struct, __scribble_system:233, только `GM_build_type=="run"` | OK (__scribble_system.gml:231-233) |
| 46 | `input_map` — rebuild при ребинде scr_inputApi:472,560, scr_settingsManager:336; выводится из player_settings | OK (scr_inputApi.gml:472,560; scr_settingsManager.gml:336) |
| 47 | `__input_repeat_state` — пишет scr_inputApi:390-395, сброс scr_settings_step_rebind | OK (scr_inputApi.gml:390-395; scr_settings_step_rebind.gml:84-86) |
| 48 | `__gamepad_axis_prev` {up,down,left,right}, :99; пишет :143,173 | OK |
| 49 | `__gamepad_axis_pressed` :100; пишет :144,172; читает :262-264 | OK |
| 55 | `obj_player` instance, :126 (noone); пишут Create_0:235, CleanUp_0:11; читают `__get_player_instance`, obj_save, obj_sound_test | OK (obj_cutsceneManager/Create_0.gml:321-325; obj_player/Create_0.gml:235, CleanUp_0.gml:11; obj_save/Step_0:12-13; obj_sound_test/Step_0:15-16) |
| 56 | `inventory` array[8], scr_inventory_init:5; слот строка 6 | OK (scr_inventory_init.gml:5; scr_saveSave.gml:66-68) |
| 57 | `equipped_weapon` struct/undefined, init :16; слот строка 7 | OK (scr_inventory_init.gml:16; scr_item_apply_use:17; obj_inGameMenu/Step_0:175; scr_saveLoad:228-229; scr_saveSave:77,81-82) |
| 58 | `equipped_armor` init :17; слот строка 8 | OK (scr_inventory_init.gml:17; scr_item_apply_use:24; scr_saveLoad:230-231; scr_saveSave:78,83-84) |
| 59 | `stat_hp` real, :23; слот stats.hp | OK init/сейв; **MISSING** писатель `scr_item_apply_use` (scr_item_apply_use.gml:36 — лечение едой) |
| 60 | `stat_maxhp` :24 | OK (scr_inventory_init.gml:24; scr_saveLoad:241; scr_saveSave:112) |
| 61-62 | `stat_base_atk`/`stat_base_def` :25/:26, писатель scr_saveLoad:252/:254 | OK (scr_saveLoad.gml:252-255) |
| 63-64 | `stat_atk`/`stat_def` через scr_stats_recalc (scr_inventory_init:72/:73), saveLoad:242/:243 | OK |
| 65-66 | `stat_lv` :27, `stat_gold` :28 | OK |
| 67 | `player_name` "CHARA" :32, слот stats.name | OK (scr_inventory_init.gml:32; scr_saveLoad:246; scr_saveSave:122) |
| 68 | `item_count` real, obj_inGameMenu/Create_0:38, производная inventory | OK (:38-40; script_items.gml:78; scr_test_framework:109,136) |
| 69 | `__item_database_registry` struct имя→factory, script_items:12 lazy | OK (script_items.gml:11-14,22) |
| 75 | `flag` struct, :330; пишут ActionSetFlag (4608), scr_saveLoad:232; слот строка 9 | OK; **MISSING** сброс `scr_defaultLoad` (scr_defaultLoad.gml:27 `global.flag = {}`) |
| 76 | `plot` real, :331; ActionSetPlot (4626), scr_saveLoad:233; слот строка 10 | OK; **MISSING** сброс scr_defaultLoad:28 |
| 77 | `entity_state` struct "room:eid"→record, :339; scr_entity_state_set/get, restore в par_interactable; слот строка 11 | OK (scr_entity_state.gml:6-33; par_interactable/Create_0.gml:42,71; scr_saveLoad:234; scr_saveSave:103-107); **MISSING** сброс scr_defaultLoad:29 |
| 78 | `room_flags` — только сбросы (obj_Init:29, scr_saveLoad:326, scr_defaultLoad:31), подсистема мертва (scr_room_entry_check — заглушка) | OK (scr_cutscene_classes.gml:5034-5035 — пустое тело; записей вне сбросов нет) |
| 79 | `global_emote_system` {active_emotes:[]}, :262; scr_emote_system | OK (scr_emote_system.gml:63,152-188; scr_test_asserts:478-511) |
| 80 | `current_sprite` sprite, scr_inventory_init:57; пишут textboxTest Step_0:71/Step_1:16, obj_face/Step_2:4, scr_cutscene_classes:2885; читает Draw_64 | OK (obj_face/Step_2.gml:4,25,33,44,57 — :4 репрезентативно; textboxTest_scribble/Draw_64:123,142) |
| 81 | `current_voice` sound, :58; пишут Step_0:72, classes:2886; читает Create_0 | OK (Create_0:27,110) |
| 82-83 | `camera_x`/`camera_y` real, scr_inventory_init:43-47; пишут obj_globalManager/Step_2:8-9, camera-действия, obj_cutsceneManager:732-737; читают scr_test_asserts:211-212 | OK (obj_globalManager/Step_2.gml:8-9; obj_cutsceneManager/Create_0.gml:732-737; scr_cutscene_classes.gml:714-715,1007-1008,4314-4487; scr_test_asserts:211-212) |
| 89 | `game_state` struct, :71 (scr_game_state_load); пишут obj_saveManager, scr_global_quick_save, obj_globalManager/Other_3; game_state.dat | OK (obj_saveManager/Step_0:79-81,142-144; scr_global_quick_save:27-30; Other_3:5-9; scr_game_state.gml:22,77) |
| 90 | `current_save_slot` string, :222; пишут obj_saveManager, quick_save:21, resetGame:27; читают saveSave:16, saveLoad:23 | OK (obj_saveManager/Step_0:75,130,136,211; scr_global_quick_save:21; scr_resetGameToDefault:27; scr_saveSave:16; scr_saveLoad:23) |
| 91 | `last_played_save_slot` string, :219; game_state.dat | OK (obj_saveManager/Step_0:77,140,214; scr_global_quick_save:26; obj_Init:219,225) |
| 92 | `__save_slot_names` array, :234; читают obj_Init (цикл), obj_saveManager/Create_0:5-6 | OK |
| 93 | `__save_slot_metadata_cache` struct, :235; обновления obj_saveManager:104,195, quick_save:38; читатель Create_0:36-38 | OK (obj_saveManager/Step_0:104,195; scr_global_quick_save:38; Create_0:36-38) |
| 94 | `__save_playtime_seconds` real, :75; тик obj_globalManager/Step_0:68, scr_saveLoad:220, scr_defaultLoad:26; слот строка 5 | **WRONG** (читатели): `scr_save_read_metadata` (scr_saveLoad.gml:391-427) читает шапку ФАЙЛА, не глобал — вхождений `global.__save_playtime_seconds` в нём нет. Реальные читатели: scr_saveSave:62,145 |
| 95 | `__total_playtime_seconds` real, :78-80; тик Step_0:69; читают Other_3 (→game_state), obj_settingsManager; game_state.dat | OK (Step_0:69; Other_3:7; obj_settingsManager/Create_0:152, Step_0:61-64; scr_settingsManager:432) |
| 96 | `player_settings` struct, :85 (scr_loadSettings); пишут scr_settingsManager:393, resetGame:23, toggle_fullscreen, debug_activation_check; player_settings.dat | OK (scr_settingsManager.gml:393; scr_resetGameToDefault:23; scr_global_toggle_fullscreen:9-10; scr_debug_activation_check:29; obj_settingsManager/Create_0:211 — не указан, минорно) |
| 97 | `clean_state` bool, :23; пишет resetGame:20; читают Other_3:4, obj_settingsManager | OK (Other_3.gml:4; obj_settingsManager/Create_0:136, Draw_64:115) |
| 98 | `__init_done` bool, :354; читают obj_Init:8, obj_globalManager/Step_0:7 | OK |
| 104 | `__dev_spawn` bool, :119; пишут obj_devLoader, debug_hotkeys (F5/F6), scr_saveLoad:344, obj_cutsceneTest | OK (obj_devLoader/Step_0:24; debug_hotkeys:16; scr_saveLoad:344; obj_cutsceneTest:68,160,197); **MISSING** scr_defaultLoad:64 |
| 105 | `__dev_spawn_x`/`__dev_spawn_y` real, :120-121 | OK-неточность типа: писатели ставят и `undefined` (obj_devLoader/Step_0:29-30, debug_hotkeys:17-18) → тип `real / undefined`; **MISSING** scr_defaultLoad:65-66 |
| 106 | `__dev_spawn_facing` — намеренно не инициализируется (Create_0:122-125), первая запись obj_cutsceneTest/Step_0:71; писатели devLoader:31, hotkeys:19, saveLoad:347, defaultLoad:67; читатель handle_dev_spawn:16 | OK — все цитаты точные |
| 107 | `__next_spawn_*` real/undefined, :129-131; пишут scr_saveLoad:289-291, scr_defaultLoad:44-46 (+сброс :71-73); читатель obj_player/Create_0:37-48,197-220 consume-once | OK — все цитаты точные |
| 108 | `__transition_safety_frames` real, :134; on_room_change:78 (=16), декремент transition_safety | OK (on_room_change:78; transition_safety:5-6,64) |
| 109 | `is_menu_room` function, :189; читают globalManager/Step_0:66, on_room_change, quick_save | OK (Step_0:66 — гейт playtime; on_room_change:19-21; quick_save:14; также scr_callMenuInit:6 — не указан, минорно) |
| 115 | `menu_return_focus` real, :166; пишут settings_step_root:42, obj_settingsManager:259; читатель obj_menu/Create_0:3-5 consume-once | OK — все цитаты точные |
| 116 | `ingame_menu_return_index` real, :167; писатель obj_settingsManager:242; читатель obj_inGameMenu/Create_0:20-23 consume-once | OK (Create_0:242 INGAME_MENU_OPT_INDEX; inGameMenu:20-23) |
| 117-120 | `__ui_blocking_*` bool, :171-174; dirty ставит obj_globalManager каждый Step, пересчёт scr_checkUIBlocking | OK (obj_globalManager/Step_0:14-15; scr_checkUIBlocking:24-38) |
| 121-122 | `__menu_shader_depth`/`__menu_shader_prev_enabled`, :146-147; push/pop scr_menu_shader_guard | OK (scr_menu_shader_guard:4-22) |
| 123 | `__menu_volume_depth` — init scr_music_init:130 (а не first_write guard:14); push/pop scr_menu_volume_guard | OK (scr_music_init.gml:130; scr_menu_volume_guard:5,14,23-25) |
| 124 | `__window_prev_x/y/w/h` real, :60-63; пишет scr_settingsManager:277-280 | OK (+читают :299-303) |
| 125 | `__window_borderless_active` bool, :64; пишет :293,305 | OK (+читает :276) |
| 126 | `show_notification` function, :284; вызывают inventory_add и др.; рендер globalManager/Draw_64 | OK (script_items.gml:82-83 внутри inventory_add:50; Draw_64:48,57; также obj_cutsceneTest, obj_p3r_title, obj_saveManager, obj_inGameMenu) |
| 132 | `cutscene_active` bool, :151; пишут cutsceneManager :644/:701, scr_saveLoad:310, obj_cutsceneTest | OK (:644=true, :701=false; saveLoad:310; cutsceneTest:121) |
| 133 | `active_cutscene_id` string, :152; `obj_cutsceneManager:643` («""» при финале) | **WRONG** (неточность): :643 присваивает id при СТАРТЕ катсцены; `""` ставится на :699 (также :258, scr_saveLoad:312). Писатель верный, атрибуция строки неверна |
| 134 | `active_cutscene_manager` instance, :153; :613 (id)/:700 (noone); читают c_play, scr_inputApi:90 | OK (c_play:16,18-19; scr_inputApi:90-91; stress_tests:463,501) |
| 135 | `cutscene_camera_override` bool, :154; пишут cutsceneManager:664,724, `screenshot` (Create_0/**Step_0**) | **WRONG**: screenshot пишет в Create_0 (:68, :308) и CleanUp_0 (:5), НЕ в Step_0. Читатели scr_checkUIBlocking:78, cutsceneManager — OK; также obj_player/Step_2:3 и сброс scr_saveLoad:311 (не указаны, минорно) |
| 136 | `__cutscene_build_mgr` instance, :155; пишут c_begin:30, c_end, scr_saveLoad:317-320; читают c_cmd, c_play | OK (c_begin:30; c_end:48-49; saveLoad:316-320 — диапазон точнее 316-320; c_cmd:3-4; c_play:3-4,18-19; также obj_cutsceneManager:618-619) |
| 137 | `__cutscene_action_factory` struct/undefined, :156 + lazy factory:1243; читатель cutscene_load_json:211-212 | OK (cutscene_action_factory.gml:2,1243; cutscene_load_json:211-212) |
| 138 | `__interacted_targets` array, :157; пишут interactionWithNPCsOrObjects:93, obj_save/Step_0:30; сброс saveLoad:323, defaultLoad:32; читатель ActionWaitForInteract (4574-4597) | OK — все цитаты точные (+scr_test_asserts:734-763) |
| 139 | `__cutscene_checkpoints` struct, :162; писатель ActionCheckpointState (4880); сброс cutsceneManager:751, cleanup_old_checkpoints; читатель ActionRestoreState (4936) | OK (functions: 4848/4880/4936; write :4921; remove :4871; cutsceneManager:305,751) |
| 140 | `__cutscene_attachments` array, :163; attach-действия; читатель __cutscene_update_attachments (3703) | OK (function :3703; push :3831; также сброс obj_cutsceneManager:297 — не указан, минорно) |
| 141 | `__cutscene_chatterbox_registered` bool, :269; писатель c_cmd:211, читатель c_cmd:145 | OK |
| 142 | `__actor_forced_emotion` struct, lazy classes:2828,3241; пишут ActionSetPortraitNext (2815), ActionSetEmotion (3216); сброс cutsceneManager:722; читатели textbox Step_0:46-49 (consume-once), test_asserts:627 | OK — все цитаты точные (writes :2835,:3243; remove :49) |
| 143 | `music_persist_track` sound/noone, scr_music_init:35; писатель scr_cutscene_music:51; сброс cutsceneManager:757; читатель on_room_change:39-43 | OK (music_init:35; cutscene_music:51; cutsceneManager:757; on_room_change:39-43; также restore classes:1063) |
| 149 | Заголовок «Состояние музыкального движка (**46** глобалов)» | **WRONG**: в таблице 45 строк (44 `music_*` состояния + `room_music_override`; `music_persist_track` — в разделе катсцен, `music_phase_next` — функция в API-таблице) |
| 152 | `music_current` sound/noone, init :30 | OK |
| 153 | `music_instance` — placeholder obj_Init:54 + :31 | OK |
| 154 | `music_volume` real 0..1, :45; пишет fade-логика + update | OK (update_current:35,46,52,60,121,161) |
| 155 | `music_volume_target` :46,124; пишут set_music_volume_fade, duck_music, stop_music | OK (init :46, :124; writes music_init:418+, update:37,59,162) |
| 156-157 | `music_fade_duration` :49, `music_fade_timer` :50 | OK |
| 158 | `music_fade_from` :51; читатель __music_fade_lerp | OK (lerp — scr_music_init:976) |
| 159 | `music_volume_override` real (-1=из настроек), :52; читатель __music_get_settings_volume | OK (init :52; write :408; read :144) |
| 160 | `music_pitch` :55 | OK |
| 161 | `music_paused` bool, :76 | OK |
| 162-169 | `music_prev_*` (instance/volume/fade_duration/fade_timer/fade_from, layer2_instance/volume/fade_from), init :58-65 | OK (fade_previous:9-11,14-15,19-23) |
| 170-175 | `music_intro_instance` :68, `music_loop_asset` :69, `music_intro_layered_*` :70-73 | OK |
| 176-180 | `music_duck_*` :91-95; duck_multiplier читает __music_get_settings_volume | OK (read :149; interp update:12-14) |
| 181-188 | `music_layer2_*` :100-101, `music_layered_mode` :102, `music_layer_*` :103-107 | OK (layered_mode читает play_music_fade :197) |
| 189 | `music_phase_manager` struct с методами clear/set_sequence/play_index/play/next/set_intensity/stop, :793 | OK (music_init:793-903 — все 7 методов подтверждены) |
| 190-194 | `music_default_fade` :79, `crossfade_lead` :80, `phase_fade_default` :82, `phase_stop_fade` :84, `autorestart_fade` :86 | OK (autorestart читается update:38-39) |
| 195 | `music_default_game_track` sound, :114 (music_SchoolRoutine); читатель on_room_change | OK (on_room_change:30) |
| 196 | `room_music_override` undefined, :117 — мёртвое имя, зарезервировано | OK (music_init:115-117; mentions=1, читателей нет) |
| 204-223 | Таблица API-функций: строки init 177/190/274/251/457/644/325/738/513/539/569/617/382/404/718/909/918/51→142/157/625 — все сверены | OK (grep по scr_music_init.gml). Вызывающие Action* — через __cutscene_music_call (scr_cutscene_music.gml:11-21): :41,:43,:46,:71,:73,:91,:106,:117,:125,:143,:191,:204,:223,:238,:261,:279 — подтверждены |
| 206 | `play_music` — вызывают on_room_change:54, obj_p3r_title:65, obj_menu:18 | OK |
| 208 | `play_music_immediate` — on_room_change:51, ActionMusicPlay (fade 0), restore | OK (on_room_change:51; cutscene_music:41) |
| 212 | `stop_music` — ActionMusicStop, stop_layered_music fallback, phase_manager.stop, scr_test_runner, obj_sound_test | OK (cutscene_music:73; music_init:900; test_runner:32-33; sound_test:25,107) |
| 215 | `duck_music`/`unduck_music` — ActionMusicDuck/Unduck; obj_cutsceneManager:743 (cleanup-unduck) | OK (cutscene_music:191,204; Create_0:741-743) |
| 217 | `set_music_volume_fade` — ActionMusicVolume, scr_applySettings:331, obj_settingsManager:195 | OK; **MISSING** вызов из ActionMusicPlay (scr_cutscene_music:46 при аргументе volume) |
| 219-220 | `play_music_phase_sequence`/`music_phase_next` — ActionMusicPhaseSequence, obj_sound_test | OK (sound_test:27,101) |
| 221 | `__music_get_settings_volume` — placeholder obj_Init:51 → impl music_init:142 | OK |
| 229 | `__current_master_volume` real, obj_Init:45; пишут applySettings, menu_volume_guard, obj_settingsManager; читает scr_music_init (audio_master_gain) | OK (:45; settingsManager:313; volume_guard:11,30; obj_settingsManager:181; music_init:134-135) |
| 230 | `__music_volume` :46; пишут applySettings:319, obj_settingsManager:189; читают get_settings_volume, music_init:124-125 | OK (music_init:124-125,147; settingsManager:319; Create_0:189) |
| 231 | `__sfx_volume` :47; пишут applySettings:320, obj_settingsManager:203; читает scr_SFXPlay:44 | OK (settingsManager:320; Create_0:203; SFXPlay:44) |
| 237 | `debug` bool, :39,89; пишут applySettings:269, debug_activation_check (F12×5), resetGame:21; косвенно в player_settings.debug_enabled | OK (settingsManager:269; activation_check:5-39 — 5 нажатий за 2 сек; resetGame:21; obj_Init:89) |
| 238-240 | `debug_show_info`/`colliders`/`hitbox` :138-140; F1/F2/F3 через scr_toggle_debug_flag; читатели Draw_64:63/94/101 | OK (hotkeys:32-41; toggle_debug_flag:11-12 — dynamic `global[$ flag_name]`; Draw_64:63,94,101) |
| 241 | `debug_show_music` :40; F9 (hotkeys:67); читатель obj_music_ctrl/Draw_64:3 | OK |
| 242-243 | `__debug_activation_count`/`timer` :142-143; scr_debug_activation_check | OK (activation_check:5-26) |
| 244 | `__cutscene_test_return` struct, obj_cutsceneTest/Step_0:298,334 | OK (:298 `{`, :334 `{`; reads :64-66,156-158,193-195) |
| 245-248 | `__test_results` array :6 / `__test_current_name` string :9 / `__test_current_failed` bool :12 / `__test_state_snapshot` struct :94 — scr_test_framework | OK (test_framework.gml:6,9,12,94) |
| 249 | `__test_positions` **array**, scr_test_asserts:43 | **WRONG** (тип): struct — `global.__test_positions = {}` с ключами `[$ string(_target)]` (scr_test_asserts.gml:43-44; также scr_test_framework.gml:26,72) |
| 250-255 | `__test_guard_var` any :268; `__test_stress_global` any :137; `__test_flag_branch_passed`/`__test_dot_guard_passed` :669/:670; `__test_goto_*` :873/:874 | OK — все строки точные |
| 259 | Конвенция `__` + исключения (__next_spawn_*, __dev_spawn*, __interacted_targets) | OK |
| 264-273 | Полный список `__`-имён по подсистемам (включая «__test_* (11 имён)», `_scribble_debug`) | OK — 57 `__`-имён, все учтены; `__test_*` ровно 11 |
| 277-282 | Механизмы динамических имён: variable_global_get/set в снапшотах (classes:859-868,1083-1094), dot-пути (4067-4127), `global[$ flag_name]` (toggle_debug_flag:11-12), variable_global_get(_fn_name) (factory:103-104, cutscene_music:11-21) | OK — все строки и механизмы подтверждены |
| 286-292 | Таблица артефактов: `__next_spawn_`/`stat_`/`equipped_` (комментарии obj_player:35, saveSave:6,109, inGameMenu:172), `json` (guard_global.json, test_catalog:81), `name` (inventory_init:30), `thing`/`value` (TGMX_7_Properties:891,992), `settings` (inputApi:452), `settings_closing` (reset_settings_flag:1), `roomNeed` (F-583: saveLoad:292, defaultLoad:8, saveManager:135) | OK — все 10 артефактов, все цитаты точные |
| 294-301 | «См. также» — ссылки по nav_plan | OK (все целевые страницы существуют в nav_plan) |

## Итог

- **WRONG (5):** `__save_playtime_seconds` читатель `scr_save_read_metadata`; тип `__test_positions` (array→struct); `screenshot` Step_0→CleanUp_0 в `cutscene_camera_override`; атрибуция `""` при финале `active_cutscene_id` (:643→:699); счётчик «46 глобалов»→45 в заголовке музыкальной таблицы.
- **MISSING (мелкие пропуски писателей/читателей):** `stat_hp` ← `scr_item_apply_use`; `flag`/`plot`/`entity_state` ← сброс `scr_defaultLoad`; `__dev_spawn*` ← `scr_defaultLoad:64-66`; `set_music_volume_fade` ← ActionMusicPlay; `game_state_file` ← `scr_resetGameToDefault`; `__dev_spawn_x/y` тип real→`real / undefined`; `__cutscene_attachments` сброс obj_cutsceneManager:297; `active_cutscene_id`/`cutscene_camera_override` сбросы scr_saveLoad:311-312.
- **UNVERIFIABLE:** нет — все проверенные утверждения подтверждаются кодом.
- Покрытие: полное (187/187).
