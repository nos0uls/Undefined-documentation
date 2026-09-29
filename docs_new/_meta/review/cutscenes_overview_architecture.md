# Фактчек `cutscenes/overview.md` + `cutscenes/architecture.md` — ревизия кода 7ee444a

Код: `$P` (только чтение), редактор `$E` (только чтение). Страницы: `docs_new/cutscenes/overview.md`, `docs_new/cutscenes/architecture.md`. Ссылки проверены по `_meta/nav_plan.md` — все целевые файлы существуют.

## overview.md

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 12 | Катсцена — очередь action-struct с контрактом `start`/`update`/`cleanup`, исполняет persistent `obj_cutsceneManager`, управляет актёрами/камерой/музыкой/диалогами, забирает контроль | OK (`obj_cutsceneManager.yy:21` `persistent:true`; `Create_0.gml:5-8, 68-247, 645-665`) |
| 18-20 | `cutscene_load_json(_path)` читает через `buffer_load`+`json_parse`, создаёт менеджер, заполняет `action_queue` через фабрику; возвращает менеджер или `noone` | OK (`cutscene_load_json.gml:7-191`; фабрика — `cutscene_init_action_factory`/`__cutscene_json_action_from_struct`, строки 176, 199-221) |
| 21 | `cutscene_play_json(_path)` — то же + `start_cutscene` | OK (`c_cmd.gml:114-120`) |
| 22 | Путь от рабочей директории; префиксы `./` и `datafiles/` срезаются; пример `cutscene_play_json("cutscenes/cutscene1.json")` | OK (`cutscene_load_json.gml:21-33`) |
| 23 | `settings.fps` — пер-файловый FPS для конвертации `seconds`→кадры; `settings.skippable` — пропуск по `back` | OK (`cutscene_load_json.gml:94-113`; `__cutscene_json_get_frames` 388-404; `Step_0.gml:7-12`) |
| 27 | `cutscene_add(_mgr,_action)` нормализует флаг `started`, отбрасывает не-struct с логом только при `global.debug` | OK (`cutscene_add.gml:6-24`; также reject при `!instance_exists(_mgr)` — тоже под `global.debug`) |
| 29-30 | `scr_cutscene_make` — `DELETE_CANDIDATE`, тело зачищено, всегда `noone`, вызовов нет; фабрика менеджера для кода — `c_begin()` | OK (`scr_cutscene_make.gml:1-10`; grep по `$P` — только упоминание в комментарии `Create_0.gml:251`; `c_begin.gml:28-31`) |
| 34-37 | `c_begin(_id)` создаёт build-менеджер в `global.__cutscene_build_mgr`; команды пушат action через `cutscene_add`; `c_play()` запускает; `c_end()` закрывает билдер или останавливает играющую | OK (`c_begin.gml:1-32`; `__cutscene_builder_add` `c_cmd.gml:9-15`; `c_play.gml:1-22`; `c_end.gml:4-54`) |
| 37 | Команды зарегистрированы в Chatterbox из `obj_Init`; примеры `<<c_wait(60)>>`, `<<c_play_json(...)>>` | OK (`obj_Init/Create_0.gml:269-270`; `c_cmd.gml:149-153`) |
| 50-56 | Глобалы: `cutscene_active`, `active_cutscene_manager`, `active_cutscene_id`, `cutscene_camera_override`, `__cutscene_build_mgr` | OK — все инициализируются в `obj_Init/Create_0.gml:151-155` |
| 60 | Undefscene экспортирует JSON того же формата; каноничное расположение `datafiles/cutscenes/` | OK (`$E` `ipc.ts:1293-1296` — комментарий «Каноничное расположение (как читает рантайм GM) — datafiles/cutscenes/»; `export.save` `ipc.ts:1387-1397` — диалог сохранения, путь выбирает пользователь). Формат совпадает: editor `compiler/core.ts:221,374` эмитит `mark_node`, `nodeRegistry.ts:1232` — `goto` |
| 64 | `mark_node` используется для навигации `goto_node` и `stop_when: "node_reached"` | **WRONG** — тип действия в фабрике называется `goto`, не `goto_node` (`cutscene_action_factory.gml:149`; алиасов нет — `__cutscene_json_normalize_action_type` `cutscene_load_json.gml:223-235`; в редакторе тоже `goto` — `nodeRegistry.ts:1232`). `stop_when:"node_reached"` — поле `guard_global` (`scr_cutscene_classes.gml:4183-4228`) — верно |
| 66-79 | JSON-пример = `datafiles/cutscenes/cutscene1.json` | OK по содержимому, **расходится по форматированию**: в файле `"settings"` расписан на 3 строки (`cutscene1.json:4-6`), на странице свёрнут в одну. Исправлено на дословную копию |
| 81 | Менеджер ставит `global.cutscene_active`, фризит игрока при `partial_control_type == 0`, возвращает управление после очереди | OK (`Create_0.gml:644, 646-658, 703-712`) |
| 83-93 | Ссылки «См. также» | OK — все файлы есть в `docs_new/` и в `nav_plan.md` |

## architecture.md

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 17 | `obj_cutsceneManager` — persistent, без спрайта и родителя; `finish_cutscene` завершает и уничтожает | OK (`obj_cutsceneManager.yy:20-21, 38`; `Create_0.gml:933`) |
| 21-29 | Карта событий: Create/Step/Draw/Draw GUI/Room Start/Room End/Clean Up с указанными ролями | OK — ровно 7 событий в `.yy` (eventType 0, 3, 8/num 0, 8/num 64, 7/num 4, 7/num 5, 12); роли совпадают (`Step_0.gml:1-26`, `Draw_0.gml:1-49`, `Draw_64.gml:1-30`, `Other_4.gml`, `Other_5.gml`, `CleanUp_0.gml`) |
| 33 | Поля очереди: `action_queue`, `current_action_index`, `is_running`, `instant_mode`, гард `__cutscene_finished` | OK (`Create_0.gml:5-11`) |
| 34 | Watchdog-поля `debug_current_action_*`, `debug_stuck_warning_sent` | OK (`Create_0.gml:14-16`) |
| 35 | Пороги: `debug_stuck_warning_frames=600`, `debug_max_preview=10`, `instant_guard_limit=1024`, `reached_nodes_limit=50` | OK (`Create_0.gml:21-24`) |
| 36 | `skippable=true` по умолчанию; `actor_map`, `actor_specs`, `dialogue_controller`, `background_actions`, `scheduled_actions` | OK (`Create_0.gml:34, 59-61, 262, 290-293`) |
| 37 | `cutscene_engine_settings` — кэш из `cutscene_load_engine_settings()`; `debug_enabled`/`debug_extended_log` из него; `"debug"` в start-action переопределяет оверлей | OK (`Create_0.gml:64, 274-285`; `cutscene_load_json.gml:151-157`) |
| 38 | `partial_control_*`, `prev_cutscene_camera_override`, `prev_camera_view_x/y`, `prev_player_can_move` | OK (`Create_0.gml:287-289, 308, 312-316`) |
| 39 | `__goto_back_jumps`; ленивая инициализация `global.__cutscene_attachments`/`__cutscene_checkpoints` | OK (`Create_0.gml:296-306, 318`) |
| 43 | Порядок `Step_0`: `!is_running` → пропуск по `back` → `frame_counter++` → `__cutscene_update_attachments()` → `cutscene_step_tick()` | OK (`Step_0.gml:2-25`) |
| 45-49 | `cutscene_step_tick`: три потока (background → scheduled → основная очередь), контракт `start`/`update`/`cleanup`, не-struct пропуск со сбросом watchdog, `instant_mode` до `instant_guard_limit` с warning | OK (`Create_0.gml:68-247`; guard-warning 242-245) |
| 51 | Каждая фаза проверяет `__cutscene_finished` (реентерабельный finish) | OK (`Create_0.gml:74, 87, 92, 103, 121, 132, 138, 148, 203, 216, 230`) |
| 53 | `cutscene_runtime_step()` каждый кадр в `obj_globalManager/Step_0`; рантайм tween/fade/jump/spin/shake с `owner_id`; `finish` гасит через `cutscene_runtime_cleanup_owner(id)` | OK (`obj_globalManager/Step_0.gml:49`; `scr_cutscene_classes.gml:1442-1485, 1518+`; `Create_0.gml:816-820`) |
| 57-61 | `start_cutscene`: сброс `__cutscene_finished`/`__parallel_stack`/`__goto_back_jumps`/watchdog; finish предыдущей сцены; закрытие протёкшего билдера; глобалы; фриз игрока при type 0; захват камеры | OK (`Create_0.gml:586-665`) |
| 65-69 | `finish_cutscene`: идемпотентность, гард владения, три региона | OK по содержимому; **порядок регионов неточен** — в коде `cutscene_runtime_cleanup_owner` идёт между background и scheduled cleanup (`Create_0.gml:800-837`), а attach-записи с мёртвыми ссылками дочищаются в регионе 3 (`Create_0.gml:899-920`). Исправлено |
| 71-73 | `skippable` default `true`, `settings.skippable` в JSON, `back` → полный `finish_cutscene` | OK (`Create_0.gml:34`; `cutscene_load_json.gml:111, 132`; `Step_0.gml:7-12`) |
| 77 | `ActionGoToNode`: метка в основной очереди (parallel/sequence недостижимы — warning), назад — сброс `started`/`__cleanup_done`/таймеров + `reset()`, самопрыжок — no-op, лимит обратных прыжков 1024 | OK (`scr_cutscene_classes.gml:1802-1870`; лимит — литерал 1024 в строке 1841, не `instant_guard_limit` — в тексте страницы об этом корректно) |
| 79 | `__parallel_stack`: push/pop при обходе, `insert_actions` → `__cutscene_parallel_splice`, `__cutscene_parallel_request_abort`; сброс в `start_cutscene` и первой строкой `finish_cutscene` | OK (`scr_cutscene_classes.gml:136-234`; `Create_0.gml:545-582, 599, 676`) |
| 85 | `ActionRoomChange`/`room_change`: `start` пишет `__room_change_*` в менеджер, создаёт `obj_changingRoomsController` с фейдом, `__player_pos_by_manager` гасит дубль записи позиции в `scr_room_fade_update`; `update` ждёт смерти контроллера, иначе параметры инвалидируются с warning | OK (`scr_cutscene_classes.gml:4716-4805`; `scr_room_fade_update.gml:50-53`; фабрика `cutscene_action_factory.gml:1200-1240`) |
| 86-88 | Внешний переход не обрывает сцену; `Other_5` пишет `__transition_actor_snapshot` `{x,y,was_persistent,persist_marked}`, актёры со spec получают переходный `persistent`, комнатные NPC без spec не помечаются | OK (`Other_5.gml:15-29`; `Other_4.gml:38-93`) |
| 90-93 | `Other_4`: безусловный `dialogue_controller=noone`; ветки внешнего перехода и `ActionRoomChange` | OK (`Other_4.gml:36, 47-93, 96-160`) |
| 97 | `checkpoint_state`+`include_music` снимает `music`-секцию: `current_track`,`volume`,`pitch`,`paused`,`duck_multiplier`,`layered_mode`,`layer2_asset`,`layer_intensity`,`persist_track` | OK — все 9 полей (`scr_cutscene_classes.gml:821-836`) |
| 99 | `restore_state` → `__cutscene_restore_music_state`: `music_current` (только валидный asset), `music_volume`, `play_music_immediate`, layered `play_music_layered`+`set_music_layer_intensity`, `set_music_pitch`, `duck_music`, `music_persist_track`, `set_music_volume_fade`, `pause_music` | OK (`scr_cutscene_classes.gml:1011-1073, 5001`; нюанс: строковые имена треков тоже резолвятся через `asset_get_index`, 1034-1040 — допустимое упрощение) |
| 101 | Финал: `music_persist_track=noone` → следующая смена комнаты выберет трек комнаты (`scr_global_on_room_change`); `unduck_music(0)` под try/catch | OK (`Create_0.gml:741-758`; `scr_global_on_room_change.gml:33-43`) |
| 105 | `cutscene_load_engine_settings()`: кэш static + `_force_reload`, файл `cutscenes/cutscene_engine_settings.json`, дефолты `__cutscene_default_engine_settings()` (`default_fps=60` с валидацией 1–240, `default_actor_object`, `default_emote_sprite`, `whitelist.*`, `debug.*`) | OK (`cutscene_load_engine_settings.gml:12-180`; файл `datafiles/cutscenes/cutscene_engine_settings.json` существует и совпадает со схемой) |
| 109-112 | Ошибки загрузки `[CUTSCENE] ОШИБКА` + `noone` + destroy недособранного менеджера; фабрика `WARNING`+пропуск; stuck-watchdog 600 кадров одноразово при `debug_enabled‖debug_extended_log`; пути завершения сломанной сцены | OK (`cutscene_load_json.gml:10-188`; фабрика логирует `ПРЕДУПРЕЖДЕНИЕ`/`FACTORY: ... rejected` — семантика та же; `Create_0.gml:189-193`; `CleanUp_0.gml:1-21`) |
| 116-127 | Mermaid stateDiagram: Built → Running → Tick → RoomEnd → RoomStart → Tick → Finishing → [*] | OK — соответствует коду (одно состояние на событие; `RoomEnd`/`RoomStart` — метки перехода комнаты) |
| 129-138 | Ссылки «См. также» | OK — все файлы есть в `docs_new/` и в `nav_plan.md` |

## Итог

- `overview.md`: 1 фактическая ошибка (`goto_node` → `goto`), 1 расхождение форматирования в JSON-примере (исправлено на дословную копию), 1 уточнение имени фабрики (`cutscene_action_factory` → `cutscene_init_action_factory`).
- `architecture.md`: 1 неточность порядка cleanup-шагов в регионе 2 `finish_cutscene` + пропущенный проход чистки dead-attach-записей в регионе 3. Исправлено.
- `MISSING`/`UNVERIFIABLE`: нет.
