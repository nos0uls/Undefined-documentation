---
title: Глоссарий
tags:
  - reference
  - glossary
---

# Глоссарий

Термины Undefinedtale-888 в том виде, в каком они встречаются в коде: имена объектов, глобалов, форматов и механик. Каждая статья ссылается на страницу с подробным описанием.

## Архитектура и комнаты

### Persistent-объект

Объект с `"persistent": true` в `.yy`: инстанс не уничтожается при `room_goto` и переживает смену комнат. Persistent в проекте: `obj_Init`, `obj_globalManager`, `obj_changingRoomsController`, `obj_cutsceneManager`, `obj_music_ctrl`, `obj_player`, `obj_pointMarker`, `o_SharedTweener`, `screenshot`.

Подробнее: [Архитектура — persistent-объекты](../architecture/overview.md#persistent)

### Комната инициализации (`rm_init`)

Первая комната при запуске. Содержит единственный инстанс `obj_Init`, который строит всё глобальное состояние и завершает работу переходом `room_goto(rm_roomMenu)`.

Подробнее: [Инициализация](../architecture/initialization.md)

### Слой `Instances`

Instance layer (`GMRInstanceLayer`) в `.yy` комнаты, на котором лежат инстансы объектов. Имена слоёв не регламентированы: в игровых комнатах встречаются `Instances`, `Instances_1`, `depth`, `collis`, `tree` и др.

Подробнее: [Комнаты](../architecture/rooms.md)

### Instance Creation Code

Код, выполняемый для конкретного инстанса после его `Create`: файлы `InstanceCreationCode_*.gml` в каталоге комнаты. Через него задают `entity_id` и параметры интерактивов и триггеров перехода.

Подробнее: [Комнаты](../architecture/rooms.md)

### Меню-комната

Комната из списка `global.__service_menu_rooms` (`rm_roomMenu`, `rm_savesSelect`, `rm_settings`, `rm_devLoad`). Проверка — функция `global.is_menu_room()`; в меню-комнатах отключены быстрый сейв и накопление playtime.

Подробнее: [Комнаты](../architecture/rooms.md), [Система сохранений](../systems/save-system.md)

### `datafiles` / Included Files

Каталог Included Files проекта: `Dialogues/*.yarn`, `cutscenes/**/*.json` (включая `cutscenes/cutscene_engine_settings.json`), `cutscenes/*.yarn`, `scribble_license.txt`. В рантайме файлы доступны из `working_directory` без префикса `datafiles/`: загрузчик `cutscene_load_json` срезает префиксы `./` и `datafiles/`.

Подробнее: [Структура проекта](../getting-started/project-structure.md#datafiles), [Форматы данных](../architecture/data-formats.md#file-map)

## Игрок, глубина и взаимодействие

### Дедупликация игрока

Логика в `obj_player/Create_0`: persistent-игрок переживает `room_goto`, поэтому расставленный в редакторе дубль в той же комнате уничтожается. Выжившим считается перенесённый инстанс (его `__room_born` указывает на прошлую комнату); он помечается `__dedup_survivor`, а дубль выходит из Create без полной инициализации: `global.obj_player` и маркер не перезаписываются.

Подробнее: [Игрок](../systems/player.md)

### Маркер (`obj_pointMarker`)

Невидимый persistent-инстанс, созданный в Create игрока и хранимый в `global.obj_player.marker_id`: точка перед лицом персонажа, попадание которой в `bbox` интерактива считается наведением. Позицию каждый кадр ставит `scr_player_marker_update()` по `facing_direction`; инвариант «ровно один маркер» держит страховка в его Create.

Подробнее: [Взаимодействие и интерактивные объекты](../systems/interaction.md)

### `par_depth` и depth-режимы

Корень иерархии Z-сортировки (`depth = -y`, чем ниже объект — тем ближе к камере). Режим `depth_mode` принимает два значения: `"auto"` (пересчёт каждый Step по dirty-flag) и `"manual"` (глубину ставит внешний код: `ActionSetDepth`, `c_depth`). Заморозка и привязка — отдельные поля: `is_static` (глубина вычисляется один раз, декорации) и `attached_target` (глубина копируется из цели).

Подробнее: [Иерархия объектов — `par_depth`](../architecture/object-hierarchy.md#par-depth)

### `facing_direction` и `global.DIR`

Направление взгляда игрока и актёров. Константы: struct `global.DIR` (`RIGHT:0`, `LEFT:1`, `UP:2`, `DOWN:3`) из `scr_constants()`; маппинг направления в спрайт делает `scr_sprite_for_facing`.

Подробнее: [Игрок](../systems/player.md), [Соглашения](../getting-started/conventions.md)

### `scr_interaction`

Единая проверка взаимодействия: нажатие `confirm`, маркер в `bbox`/маске, `is_interactable`, отсутствие UI-блокировки. При срабатывании регистрирует id интерактива в `global.__interacted_targets` и запускает диалог через `readDialogue`. Файл скрипта называется `interactionWithNPCsOrObjects.gml` по историческим причинам, рабочая функция — `scr_interaction`.

Подробнее: [Взаимодействие и интерактивные объекты](../systems/interaction.md)

## Состояние мира и сохранения

### `global.entity_state`

Реестр состояний сущностей мира: struct с ключами `"room_name:entity_id"` (`scr_entity_state_get`/`set`/`clear`). Сериализуется в файл сейва целиком и восстанавливается при загрузке; сессионные данные в него не пишутся.

Подробнее: [Форматы данных — `entity_state`](../architecture/data-formats.md#entity-state), [Система сохранений](../systems/save-system.md)

### `entity_id`

Уникальный идентификатор сущности в комнате — поле наследников `par_interactable`. Задаётся в Instance Creation Code или vars-struct `instance_create_*`; fallback детерминированный: `"объект:xstart:ystart"`. Два инстанса одного объекта в одной точке получат один id, поэтому в таких случаях `entity_id` назначают явно.

Подробнее: [Иерархия объектов — `par_interactable`](../architecture/object-hierarchy.md#par-interactable)

### World flags

Персистентные комнатные флаги поверх `entity_state`: `scr_world_flag_set(room, flag, value)` / `scr_world_flag_get(room, flag)` пишут в зарезервированную сущность `"_room"`. Отличать от сессионных `global.room_flags`: они в сейв не входят и сбрасываются при загрузке.

Подробнее: [Глобальное состояние](../architecture/global-state.md#world), [Система сохранений](../systems/save-system.md)

### `global.flag` и `global.plot`

Сюжетное состояние: `global.flag` — struct с произвольными ключами (ставит `ActionSetFlag`), `global.plot` — числовой прогресс сюжета (`ActionSetPlot`). Обе величины входят в сейв.

Подробнее: [Глобальное состояние](../architecture/global-state.md#world)

### Слот сейва

Один из трёх слотов `save1`–`save3` (единый список: `scr_save_slot_names()`); файл слота: `working_directory + <slot> + ".txt"`. Активный слот сессии: `global.current_save_slot`, последний использованный: `global.last_played_save_slot`; метаданные слотов кэшируются в `global.__save_slot_metadata_cache`.

Подробнее: [Система сохранений](../systems/save-system.md)

### `game_state.dat`

Файл межсессионного состояния в формате построчный `key=value`: хранит `last_played_save_slot` и `total_playtime_seconds`. Чтение/запись: `scr_game_state_load`/`scr_game_state_save`, запись атомарная через `.tmp`; путь можно переопределить через `global.game_state_file`.

Подробнее: [Форматы данных — `game_state.dat`](../architecture/data-formats.md#game-state)

### `player_settings.dat`

Файл настроек игрока (громкости, бинды, `debug_enabled`), путь: `global.settings_file`. В сейв не входит и живёт отдельно от слотов.

Подробнее: [Форматы данных — `player_settings.dat`](../architecture/data-formats.md#settings-file)

### `global.__next_spawn_*`

Spawn-override: `__next_spawn_x`, `__next_spawn_y`, `__next_spawn_facing` — точка, в которую игрока поставит переход/загрузка; применяется и сбрасывается при спавне. Писатели: `scr_saveLoad`, `scr_defaultLoad`, дедупликация игрока.

Подробнее: [Переходы между комнатами](../systems/room-transitions.md)

### `global.clean_state`

Флаг полного сброса: `scr_resetGameToDefault()` удаляет все `save*.txt` и `game_state.dat`, выставляет `clean_state = true` и завершает игру: `obj_globalManager/Other_3` по флагу пропускает запись `game_state.dat`, чтобы не воскрешать файл.

Подробнее: [Система сохранений](../systems/save-system.md)

## Ввод и UI

### Input map

Таблица `действие → [клавиши]` в `global.input_map`, собираемая `scr_buildInputMap()` из настроек. Проверки ввода идут по именам действий (`confirm`, `back`, `up`…), а не по кодам клавиш: раскладка отделена от логики.

Подробнее: [Система ввода](../systems/input.md)

### Ребинд

Переназначение клавиши действия через меню настроек (состояние `SETTINGS_STATE.REBIND`).

Подробнее: [Система ввода](../systems/input.md#rebind)

### Блокировка UI

Проверка `scr_checkUIBlocking(exclude_self, include_cutscene)`: `true`, когда ввод занят меню, диалогом, настройками или катсценой. Результат кэшируется в пределах кадра по dirty-флагам `global.__ui_blocking_dirty*`, которые каждый Step выставляет `obj_globalManager`.

Подробнее: [UI и меню](../systems/ui-and-menus.md), [Глобальное состояние](../architecture/global-state.md#ui)

### Инвентарь

`global.inventory` — массив из 8 слотов (`scr_inventory_init()`); экипировка — ссылки на item-struct'ы в `global.equipped_weapon`/`global.equipped_armor` (индексы слотов вычисляются только при сериализации в сейв). Инвентарь пишется в сейв строкой JSON.

Подробнее: [Инвентарь и статы](../systems/inventory-and-stats.md)

## Диалоги

### Yarn

Формат диалогов (Yarn Spinner): файлы `.yarn` в `datafiles/Dialogues/` и `datafiles/cutscenes/`. Runtime-парсинг — библиотека Chatterbox.

Подробнее: [Форматы данных — Yarn](../architecture/data-formats.md#yarn)

### Yarn-узел

Именованная секция `.yarn`-файла: заголовок `title: <имя>`, тело между `---` и `===`. Запускается `readDialogue(file, node)`; у интерактивов узел задают поля `dialogue_filename`/`dialogue_node`, в катсценах: `ActionDialogue`/`c_dialogue`.

Подробнее: [Диалоги](../systems/dialogue.md)

### Chatterbox

Библиотека runtime-парсинга Yarn. Переменные и visited-метки экспортируются в сейв (`ChatterboxVariablesExport`/`Import`); команды `<<c_*(...)>>` регистрируются через `cutscene_register_chatterbox_functions()` и мостят диалоги в катсценную систему.

Подробнее: [Диалоги](../systems/dialogue.md), [GML-DSL катсцен](../cutscenes/gml-dsl.md)

### Face system

Портреты персонажей в диалогах: `map_emotions()` сопоставляет пару actor/emotion ресурсам (`mouth_closed`, `mouth_open`, `sound`, `idle_sprite`), `obj_face` читает portrait-state и рисует спрайт в Draw GUI.

Подробнее: [Диалоги](../systems/dialogue.md)

### Emote

Всплывающая иконка-эмоция над инстансом: `emote_show(target, sprite, duration, ...)`, реестр: `global.global_emote_system.active_emotes`. Единицы времени — кадры игры; вызовы из катсцен: `c_emote`/`ActionEmote`/JSON `show_emote`.

Подробнее: [Диалоги](../systems/dialogue.md)

## Катсцены

### `obj_cutsceneManager`

Persistent-менеджер катсцен: очередь `action_queue`, курсор `current_action_index`, флаги `is_running`/`instant_mode`, история `reached_nodes`, камера и реестры актёров. Ссылка на активный менеджер: `global.active_cutscene_manager`.

Подробнее: [Архитектура катсцен](../cutscenes/architecture.md)

### Action и очередь действий

Action — инстанс конструктора `CutsceneAction` или наследника (`ActionMove`, `ActionWait`, `ActionDialogue`…) с методами `start()` → `update()` → `cleanup()`. Очередь `manager.action_queue` исполняется по порядку; `update()` возвращает `true`, когда действие завершено.

Подробнее: [Классы действий](../cutscenes/action-classes.md)

### `is_blocking`

Поле `ActionScheduleAction` (JSON `schedule_action`, ключ `blocking`): при `true` действие дотикивает вложенный `inner.update()` и держит очередь до его завершения; при `false` вложенное действие уходит в `manager.scheduled_actions` (fire-and-forget), а `schedule_action` завершается в том же кадре. Общего флага блокировки у `CutsceneAction` нет.

Подробнее: [JSON-действия](../cutscenes/json-actions.md)

### Фабрика действий

`global.__cutscene_action_factory` — struct «тип → конструктор», строится лениво через `cutscene_init_action_factory()` в `cutscene_action_factory.gml` (~80 записей с алиасами). Запись вида `f[$ "move"] = function(_map, _fps)` разбирает JSON-action и возвращает `ActionMove` или `noone` при отказе валидации.

Подробнее: [JSON-действия](../cutscenes/json-actions.md)

### Актёр (actor)

Персонаж под управлением катсцены: `obj_actor` (наследник `par_actor` → `par_depth`), игрок или созданный действием `actor_create` инстанс. Движение: поля `target_x`/`target_y`/`move_active`, адресация в действиях: по `target`.

Подробнее: [Актёры и камера](../cutscenes/actors-and-camera.md)

### `mark_node` / `goto`

Пара JSON-действий для ветвления очереди. `mark_node` ставит именованную отметку: `manager.mark_node_reached()` пишет её в историю `reached_nodes` (лимит 50); `goto` переводит курсор выполнения на отметку в основной очереди (пустая цель отклоняется фабрикой). Отметки читают также условия вида `stop_when = "node_reached"`.

Подробнее: [JSON-действия](../cutscenes/json-actions.md)

### Partial control

Частичный контроль игрока во время катсцены. JSON-действие `partial_control` выставляет `manager.partial_control_*`: режим `control_type` по enum `INTERACT_PARTIAL_CONTROL` (`LOCKED`: полный запрет, `WHITELIST`: только объекты из `whitelist` и действия `allowed_actions`, `FREE`: полная свобода).

Подробнее: [Частичный контроль](../cutscenes/partial-control.md)

### `global.__interacted_targets`

Очередь instance id интерактивов, с которыми игрок взаимодействовал (лимит 32 записи, FIFO). Пишет `scr_interaction`, читает `ActionWaitForInteract`; при загрузке сейва очищается как сессионное состояние.

Подробнее: [Взаимодействие и интерактивные объекты](../systems/interaction.md)

### GML-DSL (`c_*`)

Набор функций `c_move`, `c_dialogue`, `c_emote` и др. (~40 штук), зарегистрированных в Chatterbox через `ChatterboxAddFunction`: мост из yarn-команд `<<c_*(...)>>` в катсценную систему. Сборку очереди между `c_begin`/`c_end` ведёт `global.__cutscene_build_mgr`.

Подробнее: [GML-DSL катсцен](../cutscenes/gml-dsl.md)

## Переходы, отладка и разработка

### Переход комнат (room transition)

Смена игровой комнаты с фейдом: триггер `objRoomChanger` при касании игрока снимает свои параметры и создаёт persistent `obj_changingRoomsController`, который затемняет экран, делает `room_goto` и ставит игрока в целевую точку.

Подробнее: [Переходы между комнатами](../systems/room-transitions.md)

### `delta_time`-фейд

Принцип `scr_room_fade_update()`: скорости фейда заданы в долях экрана за секунду и умножаются на `delta_time / 1000000`: затемнение/осветление не зависит от FPS. Тот же приём используют накопление playtime и таймер активации debug-режима.

Подробнее: [Переходы между комнатами](../systems/room-transitions.md)

### Debug mode

Режим отладки `global.debug`: включается пятью нажатиями `F12` за 2 секунды (`scr_debug_activation_check()`) или настройкой `debug_enabled`. Даёт оверлеи `debug_show_colliders`/`debug_show_hitbox`/`debug_show_info`/`debug_show_music`, хоткеи `F1`–`F10` (`F8`: ghost-mode, отдельно в `scr_player_debug_ghost`), пункт `DEV-LOAD` в меню слотов и быстрый сейв по `F7`.

Подробнее: [Отладка и тестирование](../systems/debug-and-testing.md)

### Ghost-mode

Режим прохождения игрока сквозь стены: `ghost_mode = debug_ghost || transition_ghost`. `debug_ghost` переключается по `F8` (`scr_player_debug_ghost`); `transition_ghost` — антизастревание, включаемое `scr_global_on_room_change` на время после перехода. В `ghost_mode` движение идёт без `scr_collision_resolve`.

Подробнее: [Отладка и тестирование](../systems/debug-and-testing.md)

### `global.__dev_spawn`

Канал спавна игрока по глобалам: `__dev_spawn` (флаг) + `__dev_spawn_x`/`__dev_spawn_y`/`__dev_spawn_facing`. Читает `scr_global_handle_dev_spawn()` из `obj_globalManager/Step_0`: при живом игроке переставляет его, иначе создаёт новый инстанс. Писатели: `obj_devLoader`, переходы `F5`/`F6`, `scr_saveLoad`, `scr_defaultLoad`.

Подробнее: [Отладка и тестирование](../systems/debug-and-testing.md), [Система сохранений](../systems/save-system.md)

### DEV-LOAD

Экран `rm_devLoad` с `obj_devLoader`: список игровых комнат из `global.rooms_by_name` (фильтр `scr_room_is_dev_navigation_excluded`), выбор комнаты выставляет `__dev_spawn_*` и ведёт к спавну игрока в целевой комнате.

Подробнее: [Отладка и тестирование](../systems/debug-and-testing.md)

## Undefscene

### Undefscene

Визуальный редактор катсцен — отдельное приложение, экспортирует граф катсцены в JSON формата `cutscenes/*.json`, который загружает `cutscene_load_json` и исполняет фабрика действий.

Подробнее: [Undefscene — обзор](../undefscene/overview.md)

### Нода и ребро (edge)

Элементы графа катсцены в редакторе: нода — вершина с типом и параметрами действия (`start`, `move`, `dialogue`, `camera_pan`, `end` и др.), ребро — направленная связь между нодами, может нести условие (поля `conditionEnabled`/`conditionVar`/`conditionEquals`/`conditionIfFalse`).

Подробнее: [Справочник нод](../undefscene/nodes.md), [Валидация](../undefscene/validation.md)

## Сборка

### Igor

Консольный движок сборки GameMaker: headless-компиляция проекта в IFF-пакет (`.zip`) без запуска IDE и игры.

Подробнее: [Сборка](../getting-started/build.md)

## См. также

- [Скрипты и функции](gml-scripts.md) — сигнатуры `scr_*`, `c_*`, `emote_show` и других функций
- [Объекты и события](objects-and-events.md) — таблица объектов, родителей и событий
- [Глобальное состояние](../architecture/global-state.md) — полный реестр `global.*`
- [Форматы данных](../architecture/data-formats.md) — сейв, `game_state.dat`, Cutscene JSON, Yarn

<!-- sources: objects/obj_Init/Create_0.gml:23-30,115-135,151-163,181-205,262-270,325-355; objects/obj_player/Create_0.gml:10-70; objects/obj_player/Step_1.gml:11; objects/obj_pointMarker/Create_0.gml; objects/par_depth/Create_0.gml; objects/par_interactable/Create_0.gml:1-40; objects/obj_actor/Create_0.gml; objects/obj_face/Create_0.gml; objects/obj_cutsceneManager/Create_0.gml:1-60; objects/obj_devLoader/Create_0.gml; objects/objRoomChanger/Create_0.gml; objects/*/obj_*.yy (persistent); scripts/scr_constants/scr_constants.gml:1-30; scripts/scr_entity_state/scr_entity_state.gml; scripts/scr_game_state/scr_game_state.gml; scripts/scr_checkUIBlocking/scr_checkUIBlocking.gml; scripts/scr_debug_activation_check/scr_debug_activation_check.gml; scripts/scr_player_debug_ghost/scr_player_debug_ghost.gml; scripts/scr_global_handle_dev_spawn/scr_global_handle_dev_spawn.gml; scripts/scr_global_on_room_change/scr_global_on_room_change.gml:59-66; scripts/scr_player_movement/scr_player_movement.gml:100-115; scripts/scr_room_fade_update/scr_room_fade_update.gml; scripts/scr_inventory_init/scr_inventory_init.gml:4-12; scripts/scr_emote_system/scr_emote_system.gml:1-30; scripts/interactionWithNPCsOrObjects/interactionWithNPCsOrObjects.gml:1-15,85-93; scripts/cutscene_action_factory/cutscene_action_factory.gml:1-60,144-153,985-1010; scripts/scr_cutscene_classes/scr_cutscene_classes.gml:64-69,1776-1820,4527-4575,4820-4824; scripts/readDialogue/readDialogue.gml; rooms/rm_init/rm_init.yy; datafiles/Dialogues/fountain.yarn; docs_new/_meta/globals.txt -->
