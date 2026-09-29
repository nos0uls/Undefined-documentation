---
title: Глобальное состояние
tags:
  - architecture
  - globals
  - initialization
  - persistence
  - save-system
---

# Глобальное состояние

Реестр всех `global.*` проекта — 187 уникальных имён (`_meta/globals.txt`). Большинство инициализируется в `obj_Init/Create_0.gml` и его вызовах (`scr_constants`, `scr_music_init`, `scr_inventory_init`); порядок и пайплайн описаны в [Инициализации](initialization.md). Здесь собран только справочник имён.

## Как читать таблицы { #how-to-read }

- **Инициализация**: место, где глобал получает первое осмысленное значение (не первое присваивание в алфавитном порядке файлов). `function` в колонке «Тип» означает, что глобал хранит метод (`global.play_music(...)`, `global.is_menu_room(...)`).
- **В сейве**: попадает ли значение в персистентные файлы. `слот`: сериализуется `scr_saveSave` в `<slot>.txt` (раскладка: [Форматы данных](data-formats.md)); `game_state.dat` / `player_settings.dat`: соответствующие файлы; `—`: живёт только в сессии.
- Имена с `__` — внутреннее состояние подсистем (см. [Приватные глобалы](#private-globals)).

## Константы и конфигурация { #constants }

Read-only по соглашению: `scr_constants` прямо запрещает запись в поля `DIR`/`SETTINGS_STATE`, остальные таблицы пишутся один раз при инициализации.

| Имя | Тип | Инициализация | Пишет | Читает | В сейве |
|-----|-----|---------------|-------|--------|---------|
| `global.DIR` | struct `{RIGHT:0, LEFT:1, UP:2, DOWN:3}` | `scr_constants.gml:14` | — (константа) | весь код с `facing` (спавн, меню, катсцены) | — |
| `global.SETTINGS_STATE` | struct `{ROOT, CATEGORY, REBIND, CONFIRM_RESET}` | `scr_constants.gml:21` | — (константа) | `obj_settingsManager`, `scr_settings_step_*` | — |
| `global.P3R_COLORS` | struct (палитра цветов) | `scr_p3r_palette.gml:6` | `scr_p3r_palette()` (лениво, один раз) | `obj_p3r_*` (Draw) | — |
| `global.default_settings` | struct | `scr_settingsManager.gml:11`: выполняется при загрузке скрипта, до `obj_Init` | top-level код скрипта | `scr_loadSettings`, `scr_resetGameToDefault` | — |
| `global.input_repeater_defaults` | struct `{delay, interval}` | `obj_Init/Create_0.gml:97` | `obj_Init` | `scr_inputApi` (дефолты повтора) | — |
| `global.ui_snd_select` | sound | `obj_Init/Create_0.gml:103` | `obj_Init` | `obj_devLoader`, меню (`scr_SFXPlay`) | — |
| `global.ui_sfx_map` | struct (ключ действия → sound) | `obj_Init/Create_0.gml:108` | `obj_Init` | `scr_SFXPlay` (строковый ключ) | — |
| `global.__service_menu_rooms` | array (имена комнат) | `obj_Init/Create_0.gml:181` | `obj_Init` | `global.is_menu_room()` | — |
| `global.rooms_by_name` | struct `{имя: room_id}` | `obj_Init/Create_0.gml:202` | `obj_Init` | `obj_devLoader` (список DEV-LOAD) | — |
| `global.game_state_file` | string | `obj_Init/Create_0.gml:69` | `obj_Init` | `scr_game_state_load/save`, `scr_resetGameToDefault` | — |
| `global.settings_file` | string | `obj_Init/Create_0.gml:35` | `obj_Init` | `scr_loadSettings`, `scr_saveSettings`, `obj_Init` (first launch) | — |
| `global.menu_particle_color_1/2/3` | colour | `scr_p3r_particles.gml:9-11` | `scr_p3r_particles` (лениво) | `scr_p3r_particles` (типы частиц меню) | — |
| `global.TGMX` | struct | `TGMX_System.gml:121` | библиотека TweenGMS | макросы TweenGMS (`global.TGMX.*`), tween-колбэки | — |
| `global._scribble_debug` | struct | `__scribble_system.gml:233` | Scribble (только `GM_build_type == "run"`) | Scribble internal | — |

## Ввод { #input }

| Имя | Тип | Инициализация | Пишет | Читает | В сейве |
|-----|-----|---------------|-------|--------|---------|
| `global.input_map` | struct `{action: [keys]}` | `obj_Init/Create_0.gml:94` (`scr_buildInputMap`) | `obj_Init`; пересборка при ребинде: `scr_inputApi:472,560`, `scr_settingsManager:336` | `scr_inputApi` (проверки ввода) | — (выводится из `player_settings`) |
| `global.__input_repeat_state` | struct (состояние повторов по action) | `obj_Init/Create_0.gml:98` | `scr_inputApi:390-395` | `scr_inputApi`, `scr_settings_step_rebind` (сброс при ребинде) | — |
| `global.__gamepad_axis_prev` | struct `{up,down,left,right}` | `obj_Init/Create_0.gml:99` | `scr_inputApi:143,173` | `scr_inputApi` (edge-детект осей) | — |
| `global.__gamepad_axis_pressed` | struct | `obj_Init/Create_0.gml:100` | `scr_inputApi:144,172` | `scr_inputApi:262-264` | — |

## Игрок, статы и инвентарь { #player }

| Имя | Тип | Инициализация | Пишет | Читает | В сейве |
|-----|-----|---------------|-------|--------|---------|
| `global.obj_player` | instance | `obj_Init/Create_0.gml:126` (`noone`) | `obj_player/Create_0.gml:235`, `CleanUp_0.gml:11` | `__get_player_instance` (катсцены), `interactionWithNPCsOrObjects`, `obj_save`, `obj_sound_test` | — |
| `global.inventory` | array[8] | `scr_inventory_init.gml:5` | `inventory_add`, `scr_saveLoad:222`, `obj_inGameMenu` (drop/use) | `obj_inGameMenu`, `scr_saveSave:66` | слот (JSON, строка 6) |
| `global.equipped_weapon` | struct / `undefined` | `scr_inventory_init.gml:16` | `scr_item_apply_use:17`, `obj_inGameMenu:175`, `scr_saveLoad:228-229` | `scr_stats_recalc`, `scr_saveSave` (индекс), `obj_inGameMenu` | слот (индекс слота, строка 7) |
| `global.equipped_armor` | struct / `undefined` | `scr_inventory_init.gml:17` | `scr_item_apply_use:24`, `obj_inGameMenu:178`, `scr_saveLoad:230-231` | `scr_stats_recalc`, `scr_saveSave` (индекс), `obj_inGameMenu` | слот (индекс слота, строка 8) |
| `global.stat_hp` | real | `scr_inventory_init.gml:23` | `scr_saveLoad:240`, `scr_item_apply_use:36` (лечение едой), тесты | меню STAT, `scr_item_apply_use` (cap по maxhp), `scr_saveSave` | слот (`stats.hp`) |
| `global.stat_maxhp` | real | `scr_inventory_init.gml:24` | `scr_saveLoad:241` | меню STAT, `scr_saveSave` | слот (`stats.maxhp`) |
| `global.stat_base_atk` | real | `scr_inventory_init.gml:25` | `scr_saveLoad:252` | `scr_stats_recalc` | слот (`stats.base_atk`) |
| `global.stat_base_def` | real | `scr_inventory_init.gml:26` | `scr_saveLoad:254` | `scr_stats_recalc` | слот (`stats.base_def`) |
| `global.stat_atk` | real | `scr_stats_recalc` (`scr_inventory_init.gml:72`) | `scr_stats_recalc`, `scr_saveLoad:242` | меню STAT, `scr_saveSave` | слот (`stats.atk`; при загрузке пересчитывается) |
| `global.stat_def` | real | `scr_stats_recalc` (`scr_inventory_init.gml:73`) | `scr_stats_recalc`, `scr_saveLoad:243` | меню STAT, `scr_saveSave` | слот (`stats.def`; то же) |
| `global.stat_lv` | real | `scr_inventory_init.gml:27` | `scr_saveLoad:244` | меню STAT, `scr_saveSave` | слот (`stats.lv`) |
| `global.stat_gold` | real | `scr_inventory_init.gml:28` | `scr_saveLoad:245` | меню STAT, `scr_saveSave` | слот (`stats.gold`) |
| `global.player_name` | string | `scr_inventory_init.gml:32` (`"CHARA"`) | `scr_saveLoad:246` | меню STAT, `scr_saveSave` | слот (`stats.name`) |
| `global.item_count` | real | `obj_inGameMenu/Create_0.gml:38` (пересчёт из массива) | `obj_inGameMenu`, `script_items.gml:78`, тесты | `obj_inGameMenu` (Step/Draw) | — (производная `inventory`) |
| `global.__item_database_registry` | struct `{имя: factory}` | `script_items.gml:12` (лениво) | `item_database_register` | `item_database` | — |

## Мир, сюжет и диалоги { #world }

| Имя | Тип | Инициализация | Пишет | Читает | В сейве |
|-----|-----|---------------|-------|--------|---------|
| `global.flag` | struct (произвольные ключи) | `obj_Init/Create_0.gml:330` | `ActionSetFlag` (`scr_cutscene_classes:4608`), `scr_saveLoad:232`; сброс: `scr_defaultLoad:27` | `ActionBranchFlag` / `__cutscene_resolve_state_value`, `scr_saveSave` | слот (JSON, строка 9) |
| `global.plot` | real | `obj_Init/Create_0.gml:331` | `ActionSetPlot` (`scr_cutscene_classes:4626`), `scr_saveLoad:233`; сброс: `scr_defaultLoad:28` | `__cutscene_resolve_state_value("plot")`, `scr_saveSave` | слот (real, строка 10) |
| `global.entity_state` | struct `"room:eid" → record` | `obj_Init/Create_0.gml:339` | `scr_entity_state_set` (вызывает `par_interactable`), `scr_saveLoad:234`; сброс: `scr_defaultLoad:29` | `scr_entity_state_get`, restore в `par_interactable`, `scr_saveSave` | слот (JSON, строка 11) |
| `global.room_flags` | struct | `obj_Init/Create_0.gml:29` | только сброс: `obj_Init`, `scr_saveLoad:326`, `scr_defaultLoad:31` | нет (подсистема мертва: `scr_room_entry_check` является заглушкой) | — |
| `global.global_emote_system` | struct `{active_emotes: []}` | `obj_Init/Create_0.gml:262` | `scr_emote_system` (push/delete) | `scr_emote_system`, `scr_test_asserts` | — |
| `global.current_sprite` | sprite | `scr_inventory_init.gml:57` | `textboxTest_scribble` (Step_0:71, Step_1:16), `obj_face/Step_2:4`, `scr_cutscene_classes:2885` | `textboxTest_scribble` (Draw_64) | — |
| `global.current_voice` | sound | `scr_inventory_init.gml:58` | `textboxTest_scribble/Step_0:72`, `scr_cutscene_classes:2886` | `textboxTest_scribble` (Create_0) | — |
| `global.camera_x` | real | `scr_inventory_init.gml:43-47` | `obj_globalManager/Step_2:8` (каждый кадр), camera-действия катсцен, `obj_cutsceneManager:732-737` | `scr_test_asserts:211` | — |
| `global.camera_y` | real | `scr_inventory_init.gml:44-47` | `obj_globalManager/Step_2:9`, те же | `scr_test_asserts:212` | — |

## Сейвы и сессия { #save }

| Имя | Тип | Инициализация | Пишет | Читает | В сейве |
|-----|-----|---------------|-------|--------|---------|
| `global.game_state` | struct | `obj_Init/Create_0.gml:71` (`scr_game_state_load`) | `obj_saveManager`, `scr_global_quick_save`, `obj_globalManager/Other_3` | `obj_Init` (`:79`, `:218`) | game_state.dat (целиком) |
| `global.current_save_slot` | string | `obj_Init/Create_0.gml:222` | `obj_saveManager`, `scr_global_quick_save:21`, `scr_resetGameToDefault:27` | `scr_saveSave:16`, `scr_saveLoad:23` | — (указатель на слот) |
| `global.last_played_save_slot` | string | `obj_Init/Create_0.gml:219` | `obj_saveManager`, `scr_global_quick_save:26` | `obj_Init` (выбор слота на старте) | game_state.dat |
| `global.__save_slot_names` | array | `obj_Init/Create_0.gml:234` (`scr_save_slot_names()`) | `obj_Init` | `obj_Init` (цикл), `obj_saveManager/Create_0.gml:5-6` | — |
| `global.__save_slot_metadata_cache` | struct `{slot: meta}` | `obj_Init/Create_0.gml:235` | `obj_Init` (цикл `:237-258`); обновление после записи: `obj_saveManager:104,195`, `scr_global_quick_save:38` | `obj_saveManager/Create_0.gml:36-38` | — |
| `global.__save_playtime_seconds` | real | `obj_Init/Create_0.gml:75` | `obj_globalManager/Step_0:68` (тик), `scr_saveLoad:220`, `scr_defaultLoad:26` | `scr_saveSave:62` (и debug-лог `:145`): `scr_save_read_metadata` читает шапку файла, не глобал | слот (строка 5) |
| `global.__total_playtime_seconds` | real | `obj_Init/Create_0.gml:78-80` | `obj_globalManager/Step_0:69` (тик) | `obj_globalManager/Other_3` (→ `game_state`), `obj_settingsManager` | game_state.dat |
| `global.player_settings` | struct | `obj_Init/Create_0.gml:85` (`scr_loadSettings`) | `scr_settingsManager:393`, `obj_settingsManager:211`, `scr_resetGameToDefault:23`, `scr_global_toggle_fullscreen`, `scr_debug_activation_check` | `scr_applySettings`, `scr_buildInputMap`, меню настроек | player_settings.dat |
| `global.clean_state` | bool | `obj_Init/Create_0.gml:23` | `scr_resetGameToDefault:20` | `obj_globalManager/Other_3:4` (не писать game_state после wipe), `obj_settingsManager` | — |
| `global.__init_done` | bool | `obj_Init/Create_0.gml:354` | `obj_Init` | `obj_Init:8` (реентерабельность), `obj_globalManager/Step_0:7` | — |

## Спавн и переходы комнат { #spawn }

| Имя | Тип | Инициализация | Пишет | Читает | В сейве |
|-----|-----|---------------|-------|--------|---------|
| `global.__dev_spawn` | bool | `obj_Init/Create_0.gml:119` | `obj_devLoader`, `scr_global_debug_hotkeys` (F5/F6), `scr_saveLoad:344`, `scr_defaultLoad:64`, `obj_cutsceneTest` | `scr_global_handle_dev_spawn` | — |
| `global.__dev_spawn_x` / `__dev_spawn_y` | real / `undefined` | `obj_Init/Create_0.gml:120-121` | те же (`undefined` означает «центр комнаты»: `obj_devLoader:29-30`, `scr_global_debug_hotkeys:17-18`) | `scr_global_handle_dev_spawn` | — |
| `global.__dev_spawn_facing` | real | не инициализируется в `obj_Init` намеренно (`Create_0.gml:122-125`); первая запись: `obj_cutsceneTest/Step_0.gml:71` | `obj_devLoader:31`, `scr_global_debug_hotkeys:19`, `scr_saveLoad:347`, `scr_defaultLoad:67` | `scr_global_handle_dev_spawn:16` | — |
| `global.__next_spawn_x` / `__next_spawn_y` / `__next_spawn_facing` | real / `undefined` | `obj_Init/Create_0.gml:129-131` | `scr_saveLoad:289-291`, `scr_defaultLoad:44-46` (и сброс `:71-73`) | `obj_player/Create_0.gml:37-48,197-220` (consume-once) | — (канал «сейв → спавн») |
| `global.__transition_safety_frames` | real | `obj_Init/Create_0.gml:134` | `scr_global_on_room_change:78` (`16`), `scr_global_transition_safety` (декремент) | `scr_global_transition_safety` | — |
| `global.is_menu_room` | function | `obj_Init/Create_0.gml:189` | `obj_Init` | `obj_globalManager/Step_0:66` (пауза playtime), `scr_global_on_room_change`, `scr_global_quick_save`, `scr_callMenuInit` | — |

## UI и меню { #ui }

| Имя | Тип | Инициализация | Пишет | Читает | В сейве |
|-----|-----|---------------|-------|--------|---------|
| `global.menu_return_focus` | real | `obj_Init/Create_0.gml:166` | `scr_settings_step_root:42`, `obj_settingsManager:259` | `obj_menu/Create_0.gml:3-5` (consume-once) | — |
| `global.ingame_menu_return_index` | real | `obj_Init/Create_0.gml:167` | `obj_settingsManager:242` | `obj_inGameMenu/Create_0.gml:20-23` (consume-once) | — |
| `global.__ui_blocking_cache` | bool | `obj_Init/Create_0.gml:171` | `obj_globalManager` (dirty каждый Step), `scr_checkUIBlocking` | `scr_checkUIBlocking` | — |
| `global.__ui_blocking_dirty` | bool | `obj_Init/Create_0.gml:172` | `obj_globalManager`, `scr_checkUIBlocking` | `scr_checkUIBlocking` | — |
| `global.__ui_blocking_cache_no_cutscene` | bool | `obj_Init/Create_0.gml:173` | те же | `scr_checkUIBlocking` | — |
| `global.__ui_blocking_dirty_no_cutscene` | bool | `obj_Init/Create_0.gml:174` | те же | `scr_checkUIBlocking` | — |
| `global.__menu_shader_depth` | real | `obj_Init/Create_0.gml:146` | `scr_menu_shader_guard` (push/pop) | `scr_menu_shader_guard` | — |
| `global.__menu_shader_prev_enabled` | bool / `undefined` | `obj_Init/Create_0.gml:147` | `scr_menu_shader_guard` | `scr_menu_shader_guard` | — |
| `global.__menu_volume_depth` | real | `scr_music_init.gml:130` | `scr_menu_volume_guard` (push/pop) | `scr_menu_volume_guard` | — |
| `global.__window_prev_x` / `__window_prev_y` / `__window_prev_w` / `__window_prev_h` | real | `obj_Init/Create_0.gml:60-63` | `scr_settingsManager:277-280` | `scr_settingsManager` (восстановление окна) | — |
| `global.__window_borderless_active` | bool | `obj_Init/Create_0.gml:64` | `scr_settingsManager:293,305` | `scr_settingsManager` | — |
| `global.show_notification` | function | `obj_Init/Create_0.gml:284` | `obj_Init` | вызывают `inventory_add` и др.; рендер: `obj_globalManager/Draw_64` | — |

## Катсцены { #cutscenes }

| Имя | Тип | Инициализация | Пишет | Читает | В сейве |
|-----|-----|---------------|-------|--------|---------|
| `global.cutscene_active` | bool | `obj_Init/Create_0.gml:151` | `obj_cutsceneManager` (`:644`/`701`), `scr_saveLoad:310`, `obj_cutsceneTest` | `scr_checkUIBlocking`, `scr_inputApi`, `scr_global_on_room_change` | — |
| `global.active_cutscene_id` | string | `obj_Init/Create_0.gml:152` | `obj_cutsceneManager:643` (id при старте) / `:699` (`""` при финале), `scr_saveLoad:312` | `obj_cutsceneManager`, `obj_cutsceneTest` | — |
| `global.active_cutscene_manager` | instance | `obj_Init/Create_0.gml:153` | `obj_cutsceneManager:613` (`id`) / `:700` (`noone`) | `c_play`, `scr_inputApi:90`, тесты | — |
| `global.cutscene_camera_override` | bool | `obj_Init/Create_0.gml:154` | `obj_cutsceneManager:664,724`, `screenshot` (Create_0:68,308 / CleanUp_0:5); сброс: `scr_saveLoad:311` | `scr_checkUIBlocking`, `obj_cutsceneManager`, `obj_player/Step_2:3` | — |
| `global.__cutscene_build_mgr` | instance | `obj_Init/Create_0.gml:155` | `c_begin:30`, `c_end`, `scr_saveLoad:316-320` | `c_cmd`, `c_play`, `scr_saveLoad`, `obj_cutsceneManager:618-619` | — |
| `global.__cutscene_action_factory` | struct / `undefined` | `obj_Init/Create_0.gml:156` (лениво: `cutscene_action_factory.gml:1243`) | `cutscene_action_factory` | `cutscene_load_json:211-212` | — |
| `global.__interacted_targets` | array (instance id) | `obj_Init/Create_0.gml:157` | `interactionWithNPCsOrObjects:93`, `obj_save/Step_0:30`; сброс: `scr_saveLoad:323`, `scr_defaultLoad:32` | `ActionWaitForInteract` (`scr_cutscene_classes:4574-4597`), `scr_test_asserts` | — |
| `global.__cutscene_checkpoints` | struct | `obj_Init/Create_0.gml:162` | `ActionCheckpointState` (`scr_cutscene_classes:4880`); сброс: `obj_cutsceneManager:751`, `__cutscene_cleanup_old_checkpoints` | `ActionRestoreState` (`:4936`) | — |
| `global.__cutscene_attachments` | array | `obj_Init/Create_0.gml:163` | attach-действия катсцен; сброс: `obj_cutsceneManager:297` | `__cutscene_update_attachments` (`scr_cutscene_classes:3703`), `obj_cutsceneManager` | — |
| `global.__cutscene_chatterbox_registered` | bool | `obj_Init/Create_0.gml:269` | `c_cmd.gml:211` (один раз) | `c_cmd:145` | — |
| `global.__actor_forced_emotion` | struct `{actor: emotion}` | лениво — `scr_cutscene_classes:2828,3241` | `ActionSetPortraitNext` (`:2815`), `ActionSetEmotion` (`:3216`); сброс: `obj_cutsceneManager:722` | `textboxTest_scribble/Step_0:46-49` (consume-once), `scr_test_asserts:627` | — |
| `global.music_persist_track` | sound / `noone` | `scr_music_init.gml:35` | `scr_cutscene_music:51`; сброс: `obj_cutsceneManager:757` | `scr_global_on_room_change:39-43` | — |

## Музыка { #music }

Инициализация: `scr_music_init()` (вызывается из `obj_Init`); покадровое обновление: `obj_music_ctrl/Step_0` через `scr_global_music_update_current` и `scr_global_music_fade_previous`. Два пространства имён не пересекаются: `__music_volume`/`__sfx_volume`/`__current_master_volume` — снимки настроек, а `music_*` без `__` — живое состояние движка.

??? note "Состояние музыкального движка (45 глобалов)"
    | Имя | Тип | Инициализация | Пишет | Читает | В сейве |
    |-----|-----|---------------|-------|--------|---------|
    | `global.music_current` | sound / `noone` | `scr_music_init.gml:30` | `play_music_*`, `stop_music`, restore снапшотов | `scr_global_on_room_change`, `scr_global_music_update_current`, снапшоты катсцен | — |
    | `global.music_instance` | sound instance | `obj_Init/Create_0.gml:54` (placeholder `-1`), `scr_music_init.gml:31` | `play_music_*`, `__music_handoff_to_prev` | вся music-API, `scr_global_music_update_current` | — |
    | `global.music_volume` | real 0..1 | `scr_music_init.gml:45` | fade-логика, `scr_global_music_update_current` | аудио-gain, снапшоты | — |
    | `global.music_volume_target` | real | `scr_music_init.gml:46,124` | `set_music_volume_fade`, `duck_music`, `stop_music` | `scr_global_music_update_current` | — |
    | `global.music_fade_duration` | real | `scr_music_init.gml:49` | `play_music_*`, `set_music_volume_fade` | `scr_global_music_update_current` | — |
    | `global.music_fade_timer` | real | `scr_music_init.gml:50` | те же + update (декремент) | `scr_global_music_update_current` | — |
    | `global.music_fade_from` | real | `scr_music_init.gml:51` | `play_music_*`, `duck_music`, `stop_music` | `__music_fade_lerp` | — |
    | `global.music_volume_override` | real (`-1` = из настроек) | `scr_music_init.gml:52` | `set_music_volume_fade`, сброс в `play_*`/`stop_*` | `__music_get_settings_volume` | — |
    | `global.music_pitch` | real | `scr_music_init.gml:55` | `set_music_pitch` | `play_music_*`, снапшоты | — |
    | `global.music_paused` | bool | `scr_music_init.gml:76` | `pause_music`, `resume_music` | `scr_global_music_update_current` (заморозка тика) | — |
    | `global.music_prev_instance` | sound instance | `scr_music_init.gml:58` | `__music_handoff_to_prev`, `stop_*` | `scr_global_music_fade_previous`, `pause/resume` | — |
    | `global.music_prev_volume` | real | `scr_music_init.gml:59` | `__music_handoff_to_prev`, fade_previous | `scr_global_music_fade_previous` | — |
    | `global.music_prev_fade_duration` | real | `scr_music_init.gml:60` | `__music_handoff_to_prev` | `scr_global_music_fade_previous` | — |
    | `global.music_prev_fade_timer` | real | `scr_music_init.gml:61` | `__music_handoff_to_prev`, fade_previous, `stop_*` | `scr_global_music_fade_previous` | — |
    | `global.music_prev_fade_from` | real | `scr_music_init.gml:62` | `__music_handoff_to_prev` | `__music_fade_lerp` | — |
    | `global.music_prev_layer2_instance` | sound instance | `scr_music_init.gml:63` | `__music_handoff_to_prev`, `stop_*` | `scr_global_music_fade_previous`, `pause/resume` | — |
    | `global.music_prev_layer2_volume` | real | `scr_music_init.gml:64` | `__music_handoff_to_prev`, fade_previous | `scr_global_music_fade_previous` | — |
    | `global.music_prev_layer2_fade_from` | real | `scr_music_init.gml:65` | `__music_handoff_to_prev` | `__music_fade_lerp` | — |
    | `global.music_intro_instance` | sound instance | `scr_music_init.gml:68` | `play_music_intro_*`, `__music_stop_intro` | update (переход intro→loop), `pause/resume`, `set_music_pitch` | — |
    | `global.music_loop_asset` | sound / `noone` | `scr_music_init.gml:69` | `play_music_intro_loop`, `__music_stop_intro` | update (запуск loop после intro) | — |
    | `global.music_intro_layered_mode` | bool | `scr_music_init.gml:70` | `play_music_intro_layered`, `__music_stop_intro` | update (переход intro→layered) | — |
    | `global.music_intro_layered_calm_asset` | sound / `noone` | `scr_music_init.gml:71` | `play_music_intro_layered` | update | — |
    | `global.music_intro_layered_battle_asset` | sound / `noone` | `scr_music_init.gml:72` | `play_music_intro_layered` | update | — |
    | `global.music_intro_layered_intensity` | real | `scr_music_init.gml:73` | `play_music_intro_layered` | update | — |
    | `global.music_duck_multiplier` | real | `scr_music_init.gml:91` | `duck_music`, update (интерполяция) | `__music_get_settings_volume`, снапшоты | — |
    | `global.music_duck_target` | real | `scr_music_init.gml:92` | `duck_music` | update | — |
    | `global.music_duck_fade_duration` | real | `scr_music_init.gml:93` | `duck_music` | update | — |
    | `global.music_duck_fade_timer` | real | `scr_music_init.gml:94` | `duck_music`, update | update | — |
    | `global.music_duck_fade_from` | real | `scr_music_init.gml:95` | `duck_music` | `__music_fade_lerp` | — |
    | `global.music_layer2_instance` | sound instance | `scr_music_init.gml:100` | `play_music_layered`, `__music_stop_layer2`, `__music_handoff_to_prev` | update, `pause/resume`, `set_music_pitch` | — |
    | `global.music_layer2_asset` | sound / `noone` | `scr_music_init.gml:101` | `play_music_layered`, `__music_stop_layer2` | `play_music_layered` (фильтр «те же слои»), снапшоты | — |
    | `global.music_layered_mode` | bool | `scr_music_init.gml:102` | `play_music_layered`, `__music_stop_layer2`, `__music_handoff_to_prev` | `play_music_fade`, `stop_layered_music`, снапшоты | — |
    | `global.music_layer_intensity` | real 0..1 | `scr_music_init.gml:103` | `set_music_layer_intensity`, update | update (баланс слоёв), снапшоты | — |
    | `global.music_layer_intensity_target` | real | `scr_music_init.gml:104` | `set_music_layer_intensity` | update | — |
    | `global.music_layer_fade_duration` | real | `scr_music_init.gml:105` | `set_music_layer_intensity` | update | — |
    | `global.music_layer_fade_timer` | real | `scr_music_init.gml:106` | `set_music_layer_intensity`, `play_music_layered`, update | update | — |
    | `global.music_layer_fade_from` | real | `scr_music_init.gml:107` | `set_music_layer_intensity` | `__music_fade_lerp` | — |
    | `global.music_phase_manager` | struct с методами (`clear`, `set_sequence`, `play_index`, `play`, `next`, `set_intensity`, `stop`) | `scr_music_init.gml:793` | `play_music_phase_sequence`, собственные методы | `obj_music_ctrl`, вызывающий код | — |
    | `global.music_default_fade` | real | `scr_music_init.gml:79` | `scr_music_init` | `play_music` | — |
    | `global.music_crossfade_lead` | real | `scr_music_init.gml:80` | `scr_music_init` | `play_music_fade`, `play_music_intro_loop`, `play_music_layered` | — |
    | `global.music_phase_fade_default` | real | `scr_music_init.gml:82` | `scr_music_init` | методы `music_phase_manager` | — |
    | `global.music_phase_stop_fade` | real | `scr_music_init.gml:84` | `scr_music_init` | `music_phase_manager.stop/set_intensity` | — |
    | `global.music_autorestart_fade` | real | `scr_music_init.gml:86` | `scr_music_init` | `scr_global_music_update_current` (рестарт при подъёме громкости с 0) | — |
    | `global.music_default_game_track` | sound | `scr_music_init.gml:114` | `scr_music_init` | `scr_global_on_room_change` | — |
    | `global.room_music_override` | `undefined` | `scr_music_init.gml:117` | `scr_music_init` | нет (мёртвое имя, зарезервировано) | — |

### API-функции (глобалы-методы) { #music-api }

Все определены в `scr_music_init.gml`; сигнатуры и поведение — на странице музыкальной системы. В таблице приведены только точки вызова.

Катсценные действия вызывают API по строковому имени через `__cutscene_music_call` (`scr_cutscene_music.gml:11-21`), поэтому в таблице указан класс действия, а не место вызова.

| Имя | Инициализация | Вызывают |
|-----|---------------|----------|
| `global.play_music(snd)` | `scr_music_init.gml:177` | `scr_global_on_room_change:54`, `obj_p3r_title:65`, `obj_menu:18` |
| `global.play_music_fade(snd, sec)` | `scr_music_init.gml:190` | `play_music`, `ActionMusicPlay`, `music_phase_manager.play_index` |
| `global.play_music_immediate(snd)` | `scr_music_init.gml:274` | `scr_global_on_room_change:51`, `ActionMusicPlay` (fade `0`), restore снапшотов |
| `global.play_music_intro_layered(intro, calm, battle, fade, intensity)` | `scr_music_init.gml:251` | `ActionMusicIntroLayered`, `music_phase_manager.play_index` |
| `global.play_music_intro_loop(intro, loop, fade)` | `scr_music_init.gml:457` | `ActionMusicIntroLoop`, `play_music_intro_layered` |
| `global.play_music_layered(calm, battle, fade)` | `scr_music_init.gml:644` | `ActionMusicPlayLayered`, `music_phase_manager.play_index` |
| `global.stop_music(fade)` | `scr_music_init.gml:325` | `ActionMusicStop`, `stop_layered_music` (fallback), `music_phase_manager.stop`, `scr_test_runner`, `obj_sound_test` |
| `global.stop_layered_music(fade)` | `scr_music_init.gml:738` | `ActionMusicStop` (layered), `music_phase_manager.stop` |
| `global.pause_music()` / `global.resume_music()` | `scr_music_init.gml:513` / `:539` | `ActionMusicPause` / `ActionMusicResume`; внутри — `stop_music`, `stop_layered_music` |
| `global.duck_music(mult, fade)` / `global.unduck_music(fade)` | `scr_music_init.gml:569` / `:617` | `ActionMusicDuck` / `ActionMusicUnduck`; `obj_cutsceneManager:743` (cleanup-unduck) |
| `global.set_music_pitch(pitch)` | `scr_music_init.gml:382` | `ActionMusicPitch` |
| `global.set_music_volume_fade(vol, fade)` | `scr_music_init.gml:404` | `ActionMusicVolume`, `ActionMusicPlay` (аргумент volume), `scr_applySettings:331`, `obj_settingsManager:195` (слайдер громкости) |
| `global.set_music_layer_intensity(i, fade)` | `scr_music_init.gml:718` | `ActionMusicSetIntensity`, `music_phase_manager.set_intensity` |
| `global.play_music_phase_sequence(phases, fade)` | `scr_music_init.gml:909` | `ActionMusicPhaseSequence`, `obj_sound_test` |
| `global.music_phase_next(fade)` | `scr_music_init.gml:918` | `obj_sound_test`, контент |
| `global.__music_get_settings_volume()` | placeholder `obj_Init/Create_0.gml:51` → реализация `scr_music_init.gml:142` | вся music-API (целевая громкость с учётом override и duck) |
| `global.__music_stop_intro()` | `scr_music_init.gml:157` | `play_music_*`, `stop_*` |
| `global.__music_stop_layer2()` | `scr_music_init.gml:625` | `play_music_immediate`, `stop_*` |

### Громкость (настройки ↔ движок) { #volume }

| Имя | Тип | Инициализация | Пишет | Читает | В сейве |
|-----|-----|---------------|-------|--------|---------|
| `global.__current_master_volume` | real | `obj_Init/Create_0.gml:45` | `scr_applySettings`, `scr_menu_volume_guard`, `obj_settingsManager` | `scr_menu_volume_guard`, `scr_music_init` (в `audio_master_gain`) | — (источник: `player_settings.master_volume`) |
| `global.__music_volume` | real | `obj_Init/Create_0.gml:46` | `scr_applySettings:319`, `obj_settingsManager:189` | `__music_get_settings_volume`, `scr_music_init:124-125` | — (источник: `player_settings.music_volume`) |
| `global.__sfx_volume` | real | `obj_Init/Create_0.gml:47` | `scr_applySettings:320`, `obj_settingsManager:203` | `scr_SFXPlay:44` | — (источник: `player_settings.sfx_volume`) |

## Debug и тесты { #debug }

| Имя | Тип | Инициализация | Пишет | Читает | В сейве |
|-----|-----|---------------|-------|--------|---------|
| `global.debug` | bool | `obj_Init/Create_0.gml:39,89` | `scr_applySettings:269`, `scr_debug_activation_check` (F12×5), `scr_resetGameToDefault:21` | весь проект (логи, оверлеи, hotkeys) | — (косвенно: `player_settings.debug_enabled`) |
| `global.debug_show_info` | bool | `obj_Init/Create_0.gml:138` | `scr_global_debug_hotkeys` (F1, через `scr_toggle_debug_flag`) | `obj_globalManager/Draw_64:63` | — |
| `global.debug_show_colliders` | bool | `obj_Init/Create_0.gml:139` | F2 | `obj_globalManager/Draw_64:94` | — |
| `global.debug_show_hitbox` | bool | `obj_Init/Create_0.gml:140` | F3 | `obj_globalManager/Draw_64:101` | — |
| `global.debug_show_music` | bool | `obj_Init/Create_0.gml:40` | F9 (`scr_global_debug_hotkeys:67`) | `obj_music_ctrl/Draw_64:3` | — |
| `global.__debug_activation_count` | real | `obj_Init/Create_0.gml:142` | `scr_debug_activation_check` | `scr_debug_activation_check` | — |
| `global.__debug_activation_timer` | real | `obj_Init/Create_0.gml:143` | `scr_debug_activation_check` | `scr_debug_activation_check` | — |
| `global.__cutscene_test_return` | struct | `obj_cutsceneTest/Step_0.gml:298,334` | `obj_cutsceneTest` | `obj_cutsceneTest` (внутренний тест-драйвер) | — |
| `global.__test_results` | array | `scr_test_framework.gml:6` | тест-фреймворк | тест-фреймворк | — |
| `global.__test_current_name` | string | `scr_test_framework.gml:9` | тест-фреймворк | тест-фреймворк | — |
| `global.__test_current_failed` | bool | `scr_test_framework.gml:12` | тест-фреймворк | тест-фреймворк | — |
| `global.__test_state_snapshot` | struct | `scr_test_framework.gml:94` | `__test_state_save/restore` | тест-фреймворк | — |
| `global.__test_positions` | struct `{target: {x,y}}` | `scr_test_asserts.gml:43` | `scr_test_asserts` | `scr_test_asserts` | — |
| `global.__test_guard_var` | any | `scr_test_asserts.gml:268` | `scr_test_asserts` | `scr_test_asserts` | — |
| `global.__test_stress_global` | any | `scr_stress_tests.gml:137` | `scr_stress_tests` | `scr_stress_tests` | — |
| `global.__test_flag_branch_passed` | bool | `scr_stress_tests.gml:669` | `scr_stress_tests` | `scr_stress_tests` | — |
| `global.__test_dot_guard_passed` | bool | `scr_stress_tests.gml:670` | `scr_stress_tests` | `scr_stress_tests` | — |
| `global.__test_goto_skipped_action` | bool | `scr_stress_tests.gml:873` | `scr_stress_tests` | `scr_stress_tests` | — |
| `global.__test_goto_target_reached` | bool | `scr_stress_tests.gml:874` | `scr_stress_tests` | `scr_stress_tests` | — |

## Приватные глобалы (`__`) { #private-globals }

Префикс `__` — конвенция «внутреннее состояние подсистемы»: контент (катсцены, yarn, комнаты) их не трогает, ни читает, ни пишет. Исключения, где `__`-глобал — часть публичного канала: `__next_spawn_*` (писатели: `scr_saveLoad`/`scr_defaultLoad`, читатель: `obj_player`), `__dev_spawn*` (DEV-LOAD), `__interacted_targets` (его пишет `interactionWithNPCsOrObjects`).

Полный список (детали см. в таблицах выше):

??? note "Все `__`-имена по подсистемам"
    - **init:** `__init_done`
    - **ввод:** `__input_repeat_state`, `__gamepad_axis_prev`, `__gamepad_axis_pressed`
    - **инвентарь:** `__item_database_registry`
    - **сейвы:** `__save_slot_names`, `__save_slot_metadata_cache`, `__save_playtime_seconds`, `__total_playtime_seconds`
    - **спавн/переходы:** `__dev_spawn`, `__dev_spawn_x`, `__dev_spawn_y`, `__dev_spawn_facing`, `__next_spawn_x`, `__next_spawn_y`, `__next_spawn_facing`, `__transition_safety_frames`, `__service_menu_rooms`
    - **UI:** `__ui_blocking_cache`, `__ui_blocking_dirty`, `__ui_blocking_cache_no_cutscene`, `__ui_blocking_dirty_no_cutscene`, `__menu_shader_depth`, `__menu_shader_prev_enabled`, `__menu_volume_depth`, `__window_prev_x`, `__window_prev_y`, `__window_prev_w`, `__window_prev_h`, `__window_borderless_active`
    - **музыка:** `__current_master_volume`, `__music_volume`, `__sfx_volume`, `__music_get_settings_volume`, `__music_stop_intro`, `__music_stop_layer2`
    - **катсцены:** `__cutscene_build_mgr`, `__cutscene_action_factory`, `__interacted_targets`, `__cutscene_checkpoints`, `__cutscene_attachments`, `__cutscene_chatterbox_registered`, `__actor_forced_emotion`
    - **debug/тесты:** `__debug_activation_count`, `__debug_activation_timer`, `__cutscene_test_return`, `__test_*` (11 имён)
    - **сторонние библиотеки:** `_scribble_debug` (Scribble)

## Динамические и мёртвые имена { #dynamic }

Часть обращений к глобалам идёт по строковому имени, поэтому в `globals.txt` есть записи без `first_write`: это не отдельные переменные, а артефакты сканирования:

- **`variable_global_get` / `variable_global_set`**: checkpoint-снапшоты катсцен (`include_globals` в `scr_cutscene_classes.gml:859-868`, restore `:1083-1094`) снимают и восстанавливают произвольные глобалы по имени из JSON.
- **dot-пути состояния**: `__cutscene_resolve_state_value` (`scr_cutscene_classes.gml:4067-4127`) разрешает `"flag.x"` → `global.flag[$ "x"]`, `"entity_state.<room:eid>.<field>"` → запись реестра, `"stat.hp"` / `"stat_hp"` → `global.stat_hp`, `"<struct>.<field>"` → `global[$ struct][$ field]`.
- **`global[$ flag_name]`**: `scr_toggle_debug_flag` (`scr_toggle_debug_flag.gml:11-12`) инвертирует `debug_show_*` по имени строкой.
- **`variable_global_get(_fn_name)`**: `cutscene_action_factory.gml:103-104` и `__cutscene_music_call` (`scr_cutscene_music.gml:11-21`) вызывают глобалы-функции (`play_music` и др.) по имени из JSON-поля.

| Запись в `globals.txt` | Что это на самом деле |
|------------------------|------------------------|
| `global.__next_spawn_`, `global.stat_`, `global.equipped_` | упоминания префиксов семейств в комментариях (`obj_player/Create_0.gml:35`, `scr_saveSave.gml:6,109`, `obj_inGameMenu/Step_0.gml:172`); не отдельные переменные |
| `global.json` | ложное срабатывание на имени файла `guard_global.json` (`scr_test_catalog.gml:81`) |
| `global.name` | комментарий `scr_inventory_init.gml:30` (объяснение, почему имя взято как `player_name`) |
| `global.thing`, `global.value` | комментарии в библиотеке TweenGMS (`TGMX_7_Properties.gml:891,992`) |
| `global.settings` | устаревший doc-комментарий `scr_inputApi.gml:452`: код использует `global.player_settings` |
| `global.settings_closing` | удалённый флаг; осталась пометка в `scr_global_reset_settings_flag.gml:1` |
| `global.roomNeed` | удалённый канал результата загрузки (F-583); упоминания только в комментариях (`scr_saveLoad.gml:292`, `scr_defaultLoad.gml:8`, `obj_saveManager/Step_0.gml:135`) |

## См. также

- [Инициализация](initialization.md) — `obj_Init`, порядок создания глобалов, `__init_done`
- [Форматы данных](data-formats.md) — раскладка сейва, `game_state.dat`, `player_settings.dat`
- [Система сохранений](../systems/save-system.md) — `scr_saveSave`/`scr_saveLoad`, слоты, жизненный цикл
- [Инвентарь и статы](../systems/inventory-and-stats.md) — `global.inventory`, `stat_*`, экипировка
- [Ввод](../systems/input.md) — `input_map`, повторы, геймпад

<!-- sources: docs_new/_meta/globals.txt; objects/obj_Init/Create_0.gml; scripts/scr_saveSave/scr_saveSave.gml; scripts/scr_saveLoad/scr_saveLoad.gml:220-347; scripts/scr_inventory_init/scr_inventory_init.gml; scripts/scr_constants/scr_constants.gml; scripts/scr_music_init/scr_music_init.gml; scripts/scr_menu_volume_guard/scr_menu_volume_guard.gml; scripts/scr_menu_shader_guard/scr_menu_shader_guard.gml; scripts/scr_settingsManager/scr_settingsManager.gml:11-50,269-336,393-399; scripts/script_items/script_items.gml:1-87; scripts/scr_p3r_palette/scr_p3r_palette.gml; scripts/scr_p3r_particles/scr_p3r_particles.gml; scripts/scr_entity_state/scr_entity_state.gml; scripts/scr_inputApi/scr_inputApi.gml:12-16,142-173,262-264,351-395,452-473,560; scripts/scr_cutscene_classes/scr_cutscene_classes.gml:820-899,2817-2835,3238-3243,3990-4130,4527-4626,4849-4960; scripts/cutscene_action_factory/cutscene_action_factory.gml:103-104,1044-1243; scripts/interactionWithNPCsOrObjects/interactionWithNPCsOrObjects.gml:27-93; scripts/scr_global_on_room_change/scr_global_on_room_change.gml; scripts/scr_global_transition_safety/scr_global_transition_safety.gml; scripts/scr_global_handle_dev_spawn/scr_global_handle_dev_spawn.gml; scripts/scr_global_debug_hotkeys/scr_global_debug_hotkeys.gml; scripts/scr_debug_activation_check/scr_debug_activation_check.gml; scripts/scr_toggle_debug_flag/scr_toggle_debug_flag.gml; scripts/scr_defaultLoad/scr_defaultLoad.gml; scripts/scr_resetGameToDefault/scr_resetGameToDefault.gml; scripts/scr_global_quick_save/scr_global_quick_save.gml; scripts/scr_cutscene_music/scr_cutscene_music.gml:51; scripts/scr_SFXPlay/scr_SFXPlay.gml; scripts/c_begin/c_begin.gml; scripts/c_end/c_end.gml; scripts/c_cmd/c_cmd.gml:3-4,145-211; scripts/c_play/c_play.gml; scripts/scr_test_framework/scr_test_framework.gml; scripts/scr_test_asserts/scr_test_asserts.gml:43,211-212,268,478-511,598-763; scripts/scr_stress_tests/scr_stress_tests.gml; scripts/__scribble_system/__scribble_system.gml:231-234; scripts/TGMX_System/TGMX_System.gml:21-121; objects/obj_cutsceneManager/Create_0.gml:257-287,613-757; objects/obj_cutsceneTest/Step_0.gml:64-334; objects/obj_globalManager/Step_0.gml:7-69, Step_2.gml, Draw_64.gml, Other_3.gml; objects/obj_player/Create_0.gml:35-48,193-235; objects/obj_player/CleanUp_0.gml; objects/obj_inGameMenu/Create_0.gml, Step_0.gml:170-280, Draw_64.gml; objects/obj_saveManager/Create_0.gml, Step_0.gml; objects/obj_settingsManager/Create_0.gml, Draw_64.gml; objects/obj_devLoader/Create_0.gml, Step_0.gml; objects/obj_music_ctrl/Step_0.gml, Draw_64.gml; objects/obj_menu/Create_0.gml; objects/obj_p3r_title/Create_0.gml:65; objects/obj_sound_test/Step_0.gml; objects/textboxTest_scribble/Step_0.gml:46-72, Step_1.gml; objects/screenshot/Create_0.gml:67-68; objects/obj_save/Step_0.gml:12-30 -->
