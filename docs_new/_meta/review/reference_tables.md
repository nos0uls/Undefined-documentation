# Фактчек: reference/gml-scripts.md + reference/objects-and-events.md (ревизия кода 7ee444a)

Источники: `scripts/**/*.gml`, `objects/*/*.yy` в $P; `_meta/scripts.txt`, `_meta/objects.txt`, `_meta/nav_plan.md`, `_meta/gen_reference.py` в $D. Кодовая ревизия совпадает (`git rev-parse HEAD` = `7ee444a` = CODE_REV.txt).

Метод: `gen_reference.py` запущен повторно — обе страницы пересобрались **байт-в-байт** (diff пуст), значит таблицы воспроизводимы и на 100% соответствуют инвентарям `scripts.txt`/`objects.txt`. Дополнительно `scripts.txt` сверен с кодом построчно: все 888 объявлений `function` в 351 файле совпадают (единственное расхождение — строка `///`-комментария в исключаемой библиотеке TGMX_4_TweenState.gml, на страницу не влияет). Ниже — выборочная проверка сигнатур/описаний против кода и всех ссылок.

## gml-scripts.md — сигнатуры и назначение (выборка)

| Строка | Утверждение | Вердикт |
|---|---|---|
| 20 | «Всего функций: 414 в 127 файлах» | OK — в таблицах ровно 414 строк функций и 127 секций `### scripts/`; из 359 каталогов `scripts/` исключены 231 библиотечный + 1 без функций (`currentENUMS`) = 127 |
| 28 | `scr_play_sfx(_sound_or_key, _volume = 1, _pitch = 1, _fallback_sound = undefined)` — UI-звук с учётом `global.__sfx_volume` | OK — scr_SFXPlay.gml:1-11,35 (desc и сигнатура дословно из `/// @desc`) |
| 29 | `scr_SFXPlay(_action, _volume = 1, _pitch = 1)` — legacy-алиас, fallback `ui_snd_select` | OK — scr_SFXPlay.gml:45-61 |
| 35 | `scr_anim(_sprite, _framespeed)` — создаёт obj_anim в точке вызывающего | OK — scr_anim.gml:1-9 |
| 41 | `scr_callMenuInit()` — обработка клавиши меню | OK — scr_callMenuInit.gml:4 |
| 47 | `scr_checkItemSkip()` — считает пустые слоты инвентаря | OK — scr_checkItemSkip.gml:4-8 (описание дословно из `/// @desc`; рядом в коде пометка DELETE_CANDIDATE) |
| 53 | `scr_checkPlayerFacing(_target_x, _target_y)` | OK — scr_checkPlayerFacing.gml:8 |
| 59–61 | `scr_checkUIBlocking` / `scr_ui_objects_list` / `scr_checkUIBlocking_raw` | OK — scr_checkUIBlocking.gml:15,51,70; `raw` действительно вызывается из `scr_checkUIBlocking` (строки 18,28,36) |
| 67 | `scr_collision_resolve()` — solid-группы obj_collider + par_decor + par_interactable | OK — scr_collision_resolve.gml:7,11-12 (`resolve_solid(par_decor/par_interactable)`, obj_collider — в `resolve_solid`-вызове выше по файлу) |
| 73 | `scr_constants()` | OK — scr_constants.gml:13 |
| 79 | `Script312()` — пустой стаб | OK — scr_cutscene_animate.gml:4 (`function Script312(){}`) |
| 85 | `CutsceneAction() constructor` | OK — scr_cutscene_classes.gml:64 |
| 108 | `__cutscene_find_active_textbox()` — выбор «живого» окна textboxTest_scribble | OK — scr_cutscene_classes.gml (desc из `/// @desc`) |
| 110 | `__cutscene_find_dialogue_ctrl(_manager)` — описание | **WRONG** — текст обрывается на «(см.»: `shorten()` режет по первой «. » внутри «(см. …)» (источник scr_cutscene_classes.gml:627-632). Исправлено через `DESC_OVERRIDES` |
| 143 | `ActionWait(frames) constructor` | OK — scr_cutscene_classes.gml:1753 |
| 147 | `ActionFollowPath(target_ref, points_array, speed, _use_collision = false, auto_facing = true)` | OK — scr_cutscene_classes.gml (сигнатура из `function`-строки) |
| 150 | `ActionMove(target_ref, _target_x, _target_y, speed, use_collision = false)` | OK — scr_cutscene_classes.gml:2306 |
| 155 | `ActionDialogue(_dialogue_file, _node_title = undefined, _block_queue = true, _auto_advance = false)` | OK — scr_cutscene_classes.gml:2505 |
| 182 | `ActionTween(target_ref, _property_name, to_value, frames, easing = __CUTSCENE_EASE_LINEAR, from_value = undefined, _target_kind = __CUTSCENE_KIND_INSTANCE)` | OK — scr_cutscene_classes.gml:3319 |
| 185 | `ActionCameraShake(frames = __CUTSCENE_DEFAULT_EFFECT_FRAMES, _magnitude = 4, _magnitude_x = undefined, _magnitude_y = undefined, _decay = false, _frequency = 1)` | OK — scr_cutscene_classes.gml:3422 |
| 205 | `ActionWaitForInteract(target_ref, timeout_frames = 0, timeout_action = …, interact_action = …)` | OK — scr_cutscene_classes.gml:4536 |
| 211 | `ActionPartialControl(_control_type, whitelist_array, allowed_actions_array = undefined)` → partial-control.md | OK — scr_cutscene_classes.gml:4813 |
| 216 | `scr_room_entry_check()` — точка вызова из obj_globalManager/Step_0 | OK — obj_globalManager/Step_0.gml:29-31 |
| 222 | `scr_cutscene_make()` → ссылка «Док-страница» | **WRONG** — текст ссылки отображается сырым путём `[../architecture/overview.md](…)` (нет лейбла в `PAGE_LABELS`). Цель существует. Исправлено: лейбл «Обзор архитектуры» |
| 229 | `ActionMusicPlay(_snd_asset, _fade_sec, _volume = 1.0, _persist_room_change = true)` | OK — scr_cutscene_music.gml:32 |
| 250 | `scr_debug_activation_check()` — F12, 5 нажатий за 2 с | OK — scr_debug_activation_check.gml:1-16 |
| 256–257 | `draw_text_outlined` / `draw_debug_collider` | OK — scr_debug_draw_helpers.gml:9,29 |
| 263 | `scr_defaultLoad()` | OK — scr_defaultLoad.gml:11 |
| 269 | `emote_show(_target, _sprite = undefined, _duration = 60, _offset_x = 0, _offset_y = -24, _scale = 1)` | OK — scr_emote_system.gml:24 |
| 275–276 | `emote_step()` / `emote_draw_gui(_camx, _camy, _scale, _offset_x, _offset_y)` — вызов из Step/Draw GUI менеджера | OK — scr_emote_system.gml:149,185; obj_globalManager/Draw_64.gml:160 |
| 282–286 | `scr_entity_state_get/set`, `scr_world_flag_get(room_name, flag, _default = false)` | OK — scr_entity_state.gml:6,27,89 |
| 292 | `scr_format_playtime(seconds)` | OK — scr_format_playtime.gml:5 |
| 300–301 | `scr_game_state_load/save` | OK — scr_game_state.gml:77 (save), load объявлен выше в том же файле |
| 307–308 | `scr_room_is_dev_navigation_excluded` / `scr_get_next_game_room(direction)` | OK — scr_get_next_game_room.gml:9,25 |
| 314–315 | `__debug_jump_room` / `scr_global_debug_hotkeys` | OK — scr_global_debug_hotkeys.gml |
| 327 | `scr_global_handle_notifications()` | OK — scr_global_handle_notifications.gml:1-6 (описание из `/// @desc`, обрыв на «notification_active/…» — штатное усечение `…`) |
| 345 | `scr_global_on_room_change(prev_room, new_room)` | OK — scr_global_on_room_change.gml:9 |
| 375–388 | Сигнатуры `scr_input*` (down/pressed/repeater/rebind/rebind_slot/keys_hint и пр.) | OK — scr_inputApi.gml:304,348,453 и соседние `function`-строки |
| 394–395 | `scr_inventory_init()` / `scr_stats_recalc()` | OK — scr_inventory_init.gml |
| 407 | `scr_key_to_string(key)` | OK — scr_key_to_string.gml |
| 413 | `scr_layer_ensure_instances()` → rooms.md | OK — scr_layer_ensure_instances.gml:4 |
| 426–427 | `scr_menu_volume_push(target = 0.8)` / `scr_menu_volume_pop()` | OK — scr_menu_volume_guard.gml:4 |
| 433–435 | `scr_music_init`, `__music_handoff_to_prev`, `__music_fade_lerp` | OK — scr_music_init.gml:4,930,976 |
| 469 | `scr_p3r_menu_nav(_index, _count, _wrap, _actions, _allow_horizontal = false)` | OK — scr_p3r_menu_nav.gml:9 |
| 490–491 | `scr_parse_emote` (6 параметров) / `__parse_emote_resolve_display` | OK — scr_parse_emote.gml:23,132 |
| 497 | `scr_player_animation(ui_blocking, movement_inputs)` | OK — scr_player_animation.gml:6 |
| 529 | `scr_player_process_mutually_exclusive_inputs(_up, _down, _left, _right)` | OK — scr_player_process_mutually_exclusive_inputs.gml |
| 541–542 | `scr_player_slope_resolve(_slope)` / `scr_player_cell_blocked_by_slope(_tx, _ty, _exclude)` | OK — scr_player_slope_resolve.gml:5,68 |
| 554 | `scr_resetGameToDefault()` — очистка данных + `game_end` | OK — scr_resetGameToDefault.gml:3 |
| 560 | `scr_roomFromName(_name)` — id комнаты или -1 | OK — scr_roomFromName.gml:10 |
| 572 | `scr_saveLoad(_change_room = true)` | OK — scr_saveLoad.gml:21 |
| 581 | `scr_saveSave()` | OK — scr_saveSave.gml:15 |
| 587–597 | `scr_settings_*` блок (parse_real/safe_volume/load/save/apply/reset/deep_copy/apply_and_save/resetInputToDefault/misc_items/buildInputMap) | OK — scr_settingsManager.gml:363,381 и соседние; «настроек .» — дословно из `/// @desc` (пробел перед точкой в исходнике) |
| 633–645 | `scr_ui_list_controller` / `scr_ui_nav_vertical` / `scr_ui_read_actions` | OK — scr_ui_list_controller.gml:9, scr_ui_nav_vertical.gml:8, scr_ui_read_actions.gml:4 |
| 665 | `c_begin(_id = "")` | OK — c_begin.gml:1 |
| 671–709 | Блок `c_cmd.gml`: `__get_active_mgr`, `c_tween`, `c_walk*`, `c_var_lerp_*` и др. | OK — c_cmd.gml:122,224,230,282,318 и соседние `function`-строки |
| 715–805 | Стабы `c_cmd_x`, `c_delaycmd`, `c_delaywalk`, `c_pan*`, `c_shake`, `c_instance` — «тело зачищено» | OK — в коде все эти функции действительно `{}` (c_cmd_x.gml:5, c_pan.gml:5 и др.) |
| 733,739,745,781,787,799,805 | `c_depth`, `c_end`, `c_facing`, `c_play`, `c_setxy`, `c_speaker`, `c_wait` | OK — c_depth.gml:7, c_end.gml:4, c_facing.gml:1, c_play.gml:1, c_setxy.gml:1, c_speaker.gml:1, c_wait.gml:1 |
| 813 | `cutscene_init_action_factory()` | OK — cutscene_action_factory.gml:1 |
| 831–845 | `cutscene_add` + мёртвые обёртки `cutscene_tween/fade_*/…` | OK — cutscene_add.gml:6; тела обёрток зачищены (DELETE_CANDIDATE) |
| 911–914 | `cutscene_load_engine_settings` и `__cutscene_*` хелперы | OK — cutscene_load_engine_settings.gml:12 |
| 920–934 | `cutscene_load_json` + `__cutscene_json_*` блок | OK — cutscene_load_json.gml:7 и далее по файлу |
| 964 | `cutscene_set_facing(_target_ref, _direction)` | OK — cutscene_set_facing.gml:7 |
| 990–996 | `Item/WeaponItem/ArmorItem/FoodItem` constructor + `(de)serialize` | OK — constructorsForInventory.gml:5,26,49,73,109,139,155 |
| 1002–1077 | `*_scribble` эмуляции (draw_text/string_*) — DELETE_CANDIDATE | OK — draw_text_scribble.gml:23, string_height_scribble.gml:10 и др.; это проектные эмуляции, а не библиотека Scribble — в таблице правомерно |
| 1014,1020–1021 | `interactionWithMainCast`, `scr_interaction`, `interactionWithNPCsOrObjects` | OK — interactionWithMainCast.gml:8, interactionWithNPCsOrObjects.gml:20,120 |
| 1027,1033,1039 | `map_emotions`, `playableCharacterInfo` (constructor), `readDialogue` | OK — map_emotions.gml:6, playableCharacterInfo.gml:10, readDialogue.gml:8 |
| 1045–1047 | `item_database_register`, `item_database`, `inventory_add` | OK — script_items.gml:10,22,50 |

## gml-scripts.md — исключения и полнота

| Строка | Утверждение | Вердикт |
|---|---|---|
| 16–18 | Исключены библиотеки (Chatterbox/Scribble/TweenGMS), `scr_test_*`, макрос-файлы | OK — grep по странице: ни одной функции/секции `Chatterbox*`, `__Chatterbox*`, `IsChatterbox`, `scribble*`, `__scribble*`, `TGMX_*`, `scr_test_*`, `scr_stress_tests`; в `scripts/` ровно 231 библиотечный каталог + `currentENUMS` без функций; вся остальная не-библиотечная часть (128−1=127 секций, 414 функций) присутствует |
| — | Полнота относительно `scripts.txt` | OK — страница байт-в-байт воспроизводится генератором из `scripts.txt`; все 414 не-библиотечных объявлений попали в таблицы |
| — | Актуальность `scripts.txt` коду | OK — все 888 `function`-объявлений в 351 файле совпадают с кодом построчно; расхождение лишь в строке `///`-комментария исключаемого TGMX_4_TweenState.gml |

## objects-and-events.md — сверка с objects.txt + .yy

| Строка | Утверждение | Вердикт |
|---|---|---|
| 23–27 | `par_*` (5 объектов): родители, persistent=нет, спрайты, события | OK — objects.txt; точечно по .yy: par_depth (parent null, spriteId `spr_rmChanger`, Create+Step), par_interactable (Create + Room Start/End) |
| 33–39 | Системные менеджеры (7): `o_SharedTweener`, `obj_changingRoomsController`, `obj_globalManager`, `obj_Init`, `obj_music_ctrl`, `obj_saveManager`, `obj_settingsManager` | OK — objects.txt (persistent-флаги и наборы событий совпадают, включая 7 событий `o_SharedTweener`) |
| 47–69 | «Игрок и мир» (23 объекта) | OK — objects.txt; точечно по .yy: obj_player (persistent true, `spr_Chara_walking_D`, Create/Step/Begin/End/CleanUp), obj_pointMarker (persistent true, `spr_interact`, Create), npc2 (parent npc1, `npc247`, 0 событий), bush (`bush2`, 0 событий) |
| 75–84 | «UI и меню» (10 объектов, включая 5 `obj_p3r_*` по 11 событий и `textboxTest_scribble`) | OK — objects.txt; obj_menuBGSpriteChanger spriteId `_1` подтверждён .yy |
| 90–92 | «Катсцены» (3): obj_actor, obj_cutsceneManager (persistent, 7 событий), obj_dummy | OK — objects.txt |
| 98–102 | «Debug и прочее» (5): obj_cutsceneTest, obj_devLoader, obj_menuTest (10 событий), obj_sound_test, screenshot (persistent) | OK — objects.txt; screenshot.yy подтверждает persistent true + CleanUp |
| — | Полнота: 53 объекта | OK — в `objects/` ровно 53 `.yy`, все 53 есть в таблице, ни один не пропущен и не лишний |

## Ссылки (обе страницы)

| Утверждение | Вердикт |
|---|---|
| Все 24 уникальные цели `](…)` на док-страницы из обеих таблиц существуют в `docs_new/` и перечислены в `nav_plan.md` | OK — проверено существованием файлов: systems/ (10), cutscenes/ (6), architecture/ (5), reference/ (3 — включая glossary.md) |
| Лейбл ссылки для `../architecture/overview.md` | **WRONG** (см. строку 222) — сырой путь вместо «Обзор архитектуры»; исправлено |

## Итог

- **WRONG: 2** — обрыв описания `__cutscene_find_dialogue_ctrl` (строка 110) и сырой путь в лейбле ссылки (строка 222). Оба исправлены на уровне `gen_reference.py` (`DESC_OVERRIDES`, `PAGE_LABELS`) и страница перегенерирована.
- **UNVERIFIABLE / MISSING: 0.**
- Остальные проверенные строки (50+) — OK; воспроизводимость генератора подтверждена.
