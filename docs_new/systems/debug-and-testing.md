---
title: Отладка и тестирование
tags:
  - debug
  - testing
  - rooms
  - ui
  - cutscenes
---

# Отладка и тестирование

Встроенные средства разработчика: скрытая активация `global.debug`, горячие клавиши `F1`–`F10` и `Q`, dev-спавн игрока, режим призрака, прогон скриншотов комнат и внутренний тест-фреймворк катсцен с меню по `F10`.

## Обзор

- **Флаг** `global.debug`: инициализируется в `obj_Init` из `global.player_settings.debug_enabled`, включается комбинацией `F12` ×5 или пунктом настроек.
- **Диспетчер хоткеев**: `scr_global_debug_hotkeys()`, вызывается каждый Step из `obj_globalManager/Step_0` и сразу выходит при `global.debug == false`. `F8` обрабатывается отдельно: `scr_player_debug_ghost()` в `Step_0` `obj_player`, т.к. мутирует инстанс-поля игрока.
- **Dev-спавн**: канал `global.__dev_spawn` + `__dev_spawn_x/y/facing`; применяет `scr_global_handle_dev_spawn()` (Step `obj_globalManager`).
- **Тесты**: каталог `scr_test_catalog()` + раннер в `obj_cutsceneTest` (меню по `F10`).

## Активация `global.debug`

`scr_debug_activation_check()` (`obj_globalManager/Step_0`) считает нажатия `vk_f12`: каждое нажатие инкрементирует `global.__debug_activation_count` и заново взводит `global.__debug_activation_timer = 2.0` (секунды, отсчёт по `delta_time`): окно скользящее, достаточно не делать пауз дольше 2 с между нажатиями; при истечении таймера счётчик сбрасывается. Пять нажатий включают `global.debug`. При активации:

1. `global.player_settings.debug_enabled = true` и `scr_saveSettings()`: debug переживает перезапуск.
2. Если открыт `obj_settingsManager`, синхронизируется `local_settings.debug_enabled`, иначе apply из меню откатил бы флаг.
3. Уведомление `"Debug is active"` через `global.show_notification`.

Второй путь — пункт `debug` в меню настроек (`obj_settingsManager`), переключающий `local_settings.debug_enabled` + `apply_and_save_settings()`. Пункт заблокирован при `global.clean_state == true` («режим тестера» после `scr_resetGameToDefault`), если `global.debug` ещё не включён. Комбинация `F12` `clean_state` не проверяет.

## Горячие клавиши

Все клавиши — `keyboard_check_pressed`, работают только при `global.debug == true` (кроме `F12`).

| Клавиша | Действие | Реализация |
|---------|----------|------------|
| `F12` ×5, паузы < 2 с | Включить `global.debug` | `scr_debug_activation_check` |
| `F1` | Toggle `global.debug_show_info`: оверлей FPS, depth игрока, имя комнаты, позиция | `scr_toggle_debug_flag`, отрисовка в `obj_globalManager/Draw_64` |
| `F2` | Toggle `global.debug_show_colliders`: bbox `obj_collider` (красный) и `par_interactable` (жёлтый) в GUI-координатах | `draw_debug_collider` (`scr_debug_draw_helpers`) |
| `F3` | Toggle `global.debug_show_hitbox`: bbox игрока от текущего спрайта и маркер взаимодействия | `scr_toggle_debug_flag` |
| `F4` | `game_restart()`: полный перезапуск; `obj_Init` в `rm_init` проходит инициализацию заново | инлайн в `scr_global_debug_hotkeys` |
| `F5` | Предыдущая игровая комната | `__debug_jump_room(-1)` |
| `F6` | Следующая игровая комната | `__debug_jump_room(1)` |
| `F7` | Быстрый сейв в текущий слот | `scr_global_quick_save()` (см. [Система сохранений](save-system.md)) |
| `F8` | Toggle режима призрака у игрока | `scr_player_debug_ghost` (Step `obj_player`) |
| `F9` | Toggle `global.debug_show_music`: оверлей музыкального движка | `obj_music_ctrl/Draw_64` |
| `F10` | Меню тестов катсцен `obj_cutsceneTest` | создаёт инстанс на `scr_layer_ensure_instances()`, если его нет в комнате |
| `Q` | Toggle безрамочного окна (`fullscreen_borderless`) | `scr_global_toggle_fullscreen`: отдельный вызов в `obj_globalManager/Step_0` под `global.debug` |

`F5`/`F6` идут через `scr_get_next_game_room(direction)`, который шагает `room_next`/`room_previous` и пропускает служебные комнаты фильтром `scr_room_is_dev_navigation_excluded` (`global.__service_menu_rooms` + `rm_init` + `SCREENSHOTS`). Перед `room_goto` взводится dev-спавн с `undefined`-координатами: игрок окажется в центре целевой комнаты с `facing = DIR.DOWN`.

Переключить любой флаг вручную: `scr_toggle_debug_flag("debug_show_colliders")`: инвертирует `global[$ flag_name]`, при неизвестном имени пишет warning в лог.

## Dev-спавн и `rm_devLoad`

Канал спавна — четыре глобала (дефолты в `obj_Init`):

- `global.__dev_spawn`: флаг «после следующего `room_goto` спавнить игрока»;
- `global.__dev_spawn_x` / `__dev_spawn_y`: `undefined` означает центр целевой комнаты (`room_width/2`, `room_height/2` считаются уже после перехода);
- `global.__dev_spawn_facing`: направление (`global.DIR.*`); дефолта нет: все писатели выставляют его в том же кадре.

`scr_global_handle_dev_spawn()` в Step `obj_globalManager` срабатывает один раз на флаг: если `obj_player` существует, переставляет его (обнуляет `xspd`/`yspd`, фракции, `can_move = true`, спрайт по `scr_sprite_for_facing(facing)`), иначе создаёт инстанс на слое `scr_layer_ensure_instances()`. Писатели канала: `F5`/`F6`, `obj_devLoader`, `scr_saveLoad` (прокидывает `global.__next_spawn_*` из сейва), `scr_defaultLoad`, возврат из теста (`obj_cutsceneTest`).

`rm_devLoad` — комната-меню выбора комнаты для прыжка. `RoomCreationCode` создаёт `obj_devLoader` (не `persistent`), тот собирает список из `global.rooms_by_name` (fallback: обход `room_first`/`room_next`), фильтрует тем же `scr_room_is_dev_navigation_excluded` и сортирует по имени. Список — две колонки, навигация через `scr_ui_read_actions` + `scr_ui_list_controller`; `confirm` взводит dev-спавн (`undefined`-координаты, `DIR.UP`) и делает `room_goto`, `back` возвращает в `rm_savesSelect`. Вход — пункт `DEV-LOAD` в конце списка слотов `obj_saveManager`, виден только в режиме загрузки (не `SAVEMENU_MODE.SAVE`) при `global.debug`.

## Режим призрака (`F8`)

У игрока два канала: `debug_ghost`: ручной toggle по `F8` (`scr_player_debug_ghost`, Step `obj_player`); `transition_ghost`: принудительное окно антизастревания на 16 кадров после смены комнаты (взводит `scr_global_on_room_change`, снимает `scr_global_transition_safety`). Эффективное значение — `ghost_mode = debug_ghost || transition_ghost`; его читает `scr_player_movement` (пропуск коллизий).

!!! warning "F8 не снимает transition-окно"
    `F8` переключает только `debug_ghost`: пока не истекло 16-кадровое окно `transition_ghost`, `ghost_mode` остаётся включённым: защита от застревания не гасится клавишей.

## Скриншоты комнат: `screenshot` и `SCREENSHOTS`

Комната `SCREENSHOTS` в `RoomCreationCode` создаёт объект `screenshot` (`persistent`, переживает `room_goto`). Это state machine, которая проходит все игровые комнаты и пишет каждую тайлами в `working_directory/screenshots/`:

1. `boot`: очищает папку вывода, собирает очередь комнат обходом `room_first`→`room_next`. Фильтр — `scr_room_is_dev_navigation_excluded` плюс `capture_extra_excluded_rooms` = `rm_cutsceneTest`, `roomForDialogueTesting`, `DevRoom1`.
2. При создании включает `global.cutscene_camera_override` (хранит прежнее значение для отката). В каждой комнате: снимает follow-target с `view_camera[0]` (`camera_set_view_target`), считает сетку, пишет meta, прячет игрока (`image_alpha = 0`), ждёт `room_settle_frames = 8` кадров.
3. Комната режется сеткой `capture_rows × capture_cols` по размеру viewport; на каждый тайл: `camera_set_view_pos`, `camera_settle_frames = 2` кадра, затем `screen_save` в Draw GUI (оверлей в кадр не попадает).
4. Файлы: `room_name-rNNN-cNNN.png` + `room_name-meta.json` (`room_name`, `file_prefix`, `room_width/height`, `capture_width/height`, `rows`, `cols`, `naming`): метаданные для сборки полного изображения комнаты в редакторе.
5. `ESC`: abort. По завершении runner возвращается в `entry_room`; при запуске из `SCREENSHOTS` возврата нет: статус висит 120 кадров, затем инстанс удаляется. Clean Up восстанавливает `cutscene_camera_override`, camera target и состояние игрока.

## Тест-фреймворк катсцен

!!! note "Внутренний инструмент"
    `scr_test_*` — инструментарий разработчика, а не игровая механика: тесты крутятся в живой сессии и мутируют глобальное состояние (для изоляции есть snapshot/restore).

### Компоненты

| Скрипт | Содержимое |
|--------|------------|
| `scr_test_framework` | База: `scr_test_init(name)`, `scr_test_assert(cond, msg)`, `scr_test_assert_true`, `scr_test_assert_eq`, `scr_test_current_failed`, `scr_test_results_clear`, `scr_test_print_summary`, `scr_test_snapshot_state` / `scr_test_restore_state` |
| `scr_test_asserts` | Доменные ассерты: позиция/facing/visible/depth/спрайт/переменные актёра, `actor_exists`, `flag`/`plot`, камера (at/centered/tracking/shake), музыка (playing/stopped/paused/volume/pitch/duck/intensity), эмоции, диалог (open/closed/speed/flags/emotion), `mark_node`, fade, произвольный global, очередь interact. Плюс хелперы `scr_test_remember_position`, `scr_test_simulate_action_press`, `scr_test_simulate_interact`, `scr_test_set_global_var`, `scr_test_set_skippable`, `scr_test_rapid_restart` |
| `scr_test_runner` | Очередь Run All: `scr_test_runner_build_all()`, `scr_test_runner_build_category(category)`, `scr_test_runner_start_test(item)`: для `fn`-теста вызывает функцию напрямую, для `json`: `cutscene_load_json` + `start_cutscene` |
| `scr_test_catalog` | `scr_test_catalog()`: массив записей `{ id, label, json|fn, category, desc, expect_fail? }` |
| `scr_stress_tests` | GML-стресс-тесты: строят менеджеров катсцен программно из `Action`-структур для ассертов посреди проигрывания |

`scr_test_snapshot_state()` сохраняет в `global.__test_state_snapshot` клоны `flag`, `entity_state`, `inventory`, статов `stat_*`, экипировки, `player_name`, `current_save_slot` и экспорт Chatterbox (`ChatterboxVariablesExport`); `scr_test_restore_state()` возвращает всё обратно, дёргает `scr_stats_recalc()` и удаляет тестовые файлы `save_test_v3.txt`/`save99.txt`.

### Каталог тестов

`scr_test_catalog()` возвращает 123 записи. Категории собираются в меню динамически: новая категория появляется сама.

??? note "Полный каталог по категориям (123 теста)"
    | Категория | Кол-во | Тесты (`id`) |
    |-----------|--------|--------------|
    | `movement` | 11 | `move_basic`, `move_relative`, `move_direct`, `move_collision`, `move_path`, `move_rel_dir`, `jump`, `halt`, `set_position`, `set_position_relative`, `legacy_movement` |
    | `camera` | 7 | `camera_track`, `camera_pan`, `camera_center`, `camera_shake`, `camera_pan_obj`, `camera_pan_speed`, `camera_track_until_stop` |
    | `actors` | 8 | `actor_create`, `spawn_entity`, `flip`, `spin`, `emote`, `set_emotion`, `attach_detach`, `legacy_actors` |
    | `state` | 19 | `animate`, `set_animation_frame`, `auto_facing`, `auto_walk`, `set_facing`, `set_depth`, `set_visible`, `set_property`, `tween`, `tween_camera`, `fade_in`, `fade_out`, `shake_object`, `legacy_animation`, `set_flag`, `set_plot`, `checkpoint_restore`, `room_change`, `partial_control` |
    | `dialogue` | 14 | `dialogue`, `dialogue_speed`, `portrait_next`, `portrait_now`, `clear_dialogue`, `wait_for_dialogue`, `wait_typing`, `dialogue_control`, `dialogue_prevent_skip`, `dialogue_skip_typing`, `dialogue_stay_open`, `dialogue_auto_advance`, `mark_node`, `legacy_dialogue` |
    | `composite` | 12 | `sequence`, `parallel`, `branch_true`, `branch_false`, `guard_global`, `guard_wait_until_true`, `guard_timeout`, `guard_global_var_end`, `guard_node_reached`, `schedule_action`, `wait_for_interact`, `set_instant` |
    | `edge` | 6 | `empty_sequence`, `invalid_target`, `missing_json` (`expect_fail`), `rapid_restart`, `skippable_flag`, `zero_wait` |
    | `music` | 9 | `play_music`, `stop_music`, `music_volume`, `music_duck_unduck`, `music_pitch`, `music_pause_resume`, `play_boss_music`, `crossfade_music`, `play_sfx` |
    | `stress_saveload` | 10 | `stress_save_shake`, `stress_save_move`, `stress_save_globals`, `stress_restore_missing`, `stress_multi_cp`, `stress_cleanup_trans`, `stress_save_v3_cycle`, `stress_branch_flag`, `stress_save_load_basic`, `stress_entity_state` |
    | `stress_interact` | 9 | `stress_par_4way`, `stress_wfi_abort`, `stress_wfi_timeout`, `stress_nested_par`, `stress_sched_block`, `stress_branch_par`, `stress_attach_move`, `stress_goto_guard`, `stress_partial_control` |
    | `stress_params` | 9 | `stress_instant_all`, `stress_move_zero_spd`, `stress_move_neg_coords`, `stress_move_large_coords`, `stress_wait_zero`, `stress_tween_zero`, `stress_shake_zero_mag`, `stress_spin_zero_spd`, `stress_lerp_factor` |
    | `stress_lifecycle` | 5 | `stress_rapid_restart`, `stress_abort_mid`, `stress_instant_toggle`, `stress_create_destroy`, `stress_finish_cleanup` |
    | `stress_skip` | 2 | `stress_skip_back`, `stress_prevent_skip` |
    | `stress_dialogue` | 1 | `stress_dialogue_nonblocking` |
    | `stress_gameplay` | 1 | `stress_inventory_stats` |

JSON-тесты лежат в `datafiles/cutscenes/tests/` (стресс-кейсы: `tests/stress/`); ассерты внутри JSON вызываются действием `run_function` с именем `scr_test_assert_*`.

## `obj_cutsceneTest`: меню тестов (`F10`)

Инстанс размещён в `rm_cutsceneTest` и `DevRoom1` (там меню открывается по `confirm` в радиусе `interact_radius = 50`, подсказка `SPACE`); `F10` переключает `menu_open` у существующего или создаёт объект в любой комнате, при открытом меню игрок замораживается (`can_move = false`).

**Меню** (ввод `scr_ui_read_actions`): `←`/`→`: категория (`ALL` + все из каталога); `↑`/`↓`: пункт с прокруткой; `confirm`: запуск; `back`: закрыть. Первый пункт — `▶ Run All Tests` / `▶ Run Category Tests` по выбранной категории.

**Одиночный запуск**: `scr_test_results_clear()` → `scr_test_snapshot_state()` → запись `global.__cutscene_test_return = { room, x, y, facing, active: true }` → `scr_test_init(item.id)` → старт JSON-катсцены или `fn`. После `!global.cutscene_active`: `scr_test_restore_state()` и возврат игрока в исходную точку (через dev-спавн при смене комнаты) + уведомление `"Returned to origin"`.

**Run All**: снапшот → очередь `scr_test_runner_build_all()`/`build_category()` → последовательный `scr_test_runner_start_test`, переход к следующему по `!global.cutscene_active`. Watchdog: `menu_run_all_timeout_frames = 60 * game_get_speed(gamespeed_fps)` кадров на тест: по таймауту катсцена прерывается `finish_cutscene()` и тест фейлится. `expect_fail: true` инвертирует ожидание. По окончании: `scr_test_print_summary()`, возврат по `__cutscene_test_return` и **`game_end()` с кодом `0` (все прошли) или `1` (есть фейлы)**: режим пригоден для CI-прогона. `back` во время прогона: досрочный abort с restore и возвратом.

Стресс-тесты симулируют ввод через очередь `__inject_key_queue`: клавиши жмутся `keyboard_key_press` в начале Step `obj_cutsceneTest` и удерживаются 4 кадра (`__inject_held_keys`), `__inject_self_guard` глушит собственные обработчики `back`, чтобы симуляция не срывала меню/прогон. Отложенные skip-ассерты — `__inject_expect_*` (режимы `finish`/`survive` с дедлайном).

## Как добавить свой тест

1. JSON-тест: положите файл в `datafiles/cutscenes/tests/` и добавьте запись в массив `scr_test_catalog()`:

```gml title="scripts/scr_test_catalog/scr_test_catalog.gml"
{ id: "my_test", label: "My test", json: "cutscenes/tests/my_test.json",
  category: "movement", desc: "Что проверяет" },
```

2. GML-стресс-тест: напишите функцию `my_stress_fn()` в `scr_stress_tests.gml` (создаёт менеджер, возвращает его) и зарегистрируйте через `fn` вместо `json`:

```gml
{ id: "stress_my", label: "Stress: My case", fn: my_stress_fn,
  category: "stress_lifecycle", desc: "Описание кейса" },
```

`scr_test_init` внутри `fn` вызывать не нужно: оба входных пути (Run All и одиночный запуск) уже инициализируют тест по `id` каталога. Провалы пишите через `scr_test_assert*`; если тест обязан упасть: `expect_fail: true`.

## См. также

- [Система сохранений](save-system.md) — `F7` quicksave, `__next_spawn_*` из сейва
- [Игрок](player.md) — `ghost_mode`, `can_move`, `facing_direction`
- [Ввод](input.md) — `scr_input_pressed`, `scr_ui_read_actions`
- [Комнаты](../architecture/rooms.md) — `rm_devLoad`, `SCREENSHOTS`, room order
- [Инициализация](../architecture/initialization.md) — `obj_Init`, дефолты debug-глобалов
- [JSON-формат катсцен](../cutscenes/json-actions.md) — `run_function`, действия тестов
- [UI и меню](ui-and-menus.md) — пункт `DEV-LOAD` в меню слотов

<!-- sources: scripts/scr_debug_activation_check/scr_debug_activation_check.gml; scripts/scr_toggle_debug_flag/scr_toggle_debug_flag.gml; scripts/scr_global_debug_hotkeys/scr_global_debug_hotkeys.gml; scripts/scr_player_debug_ghost/scr_player_debug_ghost.gml; scripts/scr_global_handle_dev_spawn/scr_global_handle_dev_spawn.gml; scripts/scr_get_next_game_room/scr_get_next_game_room.gml; scripts/scr_global_quick_save/scr_global_quick_save.gml; scripts/scr_debug_draw_helpers/scr_debug_draw_helpers.gml; scripts/scr_global_transition_safety/scr_global_transition_safety.gml:1-30; scripts/scr_global_toggle_fullscreen/scr_global_toggle_fullscreen.gml; scripts/scr_global_on_room_change/scr_global_on_room_change.gml:60-78; scripts/scr_test_framework/scr_test_framework.gml; scripts/scr_test_asserts/scr_test_asserts.gml; scripts/scr_test_runner/scr_test_runner.gml; scripts/scr_test_catalog/scr_test_catalog.gml; scripts/scr_stress_tests/scr_stress_tests.gml:1-11; objects/obj_globalManager/Step_0.gml:30-45; objects/obj_globalManager/Draw_64.gml:62-101; objects/obj_devLoader/Create_0.gml; objects/obj_devLoader/Step_0.gml; objects/obj_devLoader/Draw_64.gml; objects/screenshot/Create_0.gml; objects/screenshot/Step_0.gml; objects/screenshot/Draw_64.gml; objects/screenshot/CleanUp_0.gml; objects/screenshot/screenshot.yy; objects/obj_cutsceneTest/Create_0.gml; objects/obj_cutsceneTest/Step_0.gml; objects/obj_cutsceneTest/Draw_0.gml; objects/obj_cutsceneTest/Draw_64.gml; objects/obj_Init/Create_0.gml:39-143,176-209; objects/obj_saveManager/Step_0.gml:155-157; objects/obj_settingsManager/Create_0.gml:135-143; objects/obj_music_ctrl/Draw_64.gml:1-4; objects/obj_player/Create_0.gml:242-251; rooms/rm_devLoad/RoomCreationCode.gml; rooms/SCREENSHOTS/RoomCreationCode.gml; datafiles/cutscenes/tests/move_basic.json -->
