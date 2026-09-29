---
title: Система сохранений
tags:
  - save-system
  - persistence
  - data-formats
  - ui
---

# Система сохранений

Слотовые сейвы в текстовых файлах: три слота `save1`–`save3` в `working_directory`, UI выбора слота (`obj_saveManager`), атомарная запись (`scr_saveSave`), версионируемый разбор (`scr_saveLoad`) и общий счётчик времени (`game_state.dat`).

## Обзор

- **Слоты** — фиксированный список `["save1", "save2", "save3"]`, единый источник — `scr_save_slot_names()` в `scr_saveLoad.gml`. Файл слота: `working_directory + <slot> + ".txt"`.
- **`global.current_save_slot`** — слот, в который сессия реально сохранена. **`global.last_played_save_slot`** — последний использованный, персистится в `game_state.dat`.
- **Точки входа**: сейвпоинт `obj_save` в игровых комнатах (запись), комната `rm_savesSelect` с инстансом `obj_saveManager` (загрузка из главного меню), быстрый сейв по `F7` (только debug).
- **Полный сброс**: `scr_resetGameToDefault()` удаляет все `save*.txt`, `game_state.dat`, выставляет `global.clean_state = true` и завершает игру через `game_end()`.

## UI слотов: `obj_save` и `obj_saveManager`

### `obj_save` — сейвпоинт в мире

Наследник `par_interactable`. В `Step_0` при нажатии `confirm`, когда маркер игрока (`global.obj_player.marker_id`) внутри bbox объекта и UI не заблокирован (`scr_checkUIBlocking`), регистрирует взаимодействие в `global.__interacted_targets` (лимит 32 записей) и при заполненных `dialogue_filename`/`dialogue_node` запускает Yarn-диалог через `readDialogue`. После закрытия текстового окна (`__waiting_dialogue_close`) создаёт `obj_saveManager` с `mode = SAVEMENU_MODE.SAVE`. Без диалога меню открывается в том же кадре.

### `obj_saveManager` — меню слотов

Режим — enum `SAVEMENU_MODE` (`LOAD`/`SAVE`), объявленный в `scr_saveLoad.gml`. Инстанс `inst_saveManager` лежит в `rm_savesSelect` и работает в режиме `LOAD` (дефолт в `Create_0`); режим `SAVE` выставляет `obj_save` уже после Create, поэтому стартовый фокус вычисляется отложенно на первом Step (`__focus_pending`).

**Ввод** — через `scr_ui_read_actions` + `scr_ui_nav_vertical` (круговая навигация):

| Действие | Клавиша по умолчанию | Поведение |
|----------|----------------------|-----------|
| `up`/`down` | стрелки | выбор слота, звук `move` |
| `confirm` | `Enter`/`Z` | `SAVE` → `scr_saveSave()` в выбранный слот; `LOAD` → `scr_saveLoad()` для занятого слота или `scr_defaultLoad()` для пустого |
| `delete` | `B` (геймпад: Select) | только в `LOAD`: удаляет файл слота без подтверждения |
| `back` | `X`/`Shift` (геймпад: B/Circle) | закрывает меню; в `LOAD` дополнительно `room_goto(rm_roomMenu)` |

!!! warning "Подтверждений нет"
    Ни перезапись занятого слота, ни удаление не требуют подтверждения — операции выполняются сразу по `confirm`/`delete`.

!!! note "Подсказка в игре"
    `Draw_64` выводит подсказку «Esc/X - назад», но действие `back` по умолчанию привязано к `X`/`Shift`, а `Esc` назначен на `menu` — `actions.menu` менеджер не обрабатывает, поэтому `Esc` меню не закрывает.

**Стартовый фокус** (`Step_0`): в `SAVE` — `global.current_save_slot` или первый слот; в `LOAD` — по приоритету: dev-load (только `global.debug` и настройка `devload_focus`) → `current_save_slot` → `last_played_save_slot` → первый существующий сейв.

**Дополнительное поведение:**

- Пустой слот в `LOAD` запускает «новую игру»: `scr_defaultLoad()` сбрасывает сессию и ведёт в `rm_uphill_school` (377, 187, `DIR.DOWN`).
- При неудаче сейва/загрузки `current_save_slot` откатывается к прежнему значению, играется звук `back`, показывается уведомление `"Save failed"`/`"Load failed"`.
- Удаление слота перекидывает `current_save_slot`/`last_played_save_slot` на первый существующий слот (либо первый слот списка, если сейвов не осталось), если они указывали на удалённый.
- В `debug` под списком появляется пункт `DEV-LOAD` → `room_goto(rm_devLoad)`; у существующих сейвов у нижней границы рамки слота рисуются координаты `x`, `y`.
- Отрисовка — в `Draw GUI` (`Draw_64`): Scribble-текст, рамка `spr_saveUI`, имя комнаты из метаданных или «Сейв N», кэшированная строка playtime (`playtime_labels`, настройки `playtime_*` в `Create_0`).

**Кэш метаданных.** `obj_Init` при старте прогревает `global.__save_slot_metadata_cache` «шапками» всех слотов через `scr_save_read_metadata`. Меню берёт данные из кэша (`variable_clone`, чтобы не мутировать кэш) с fallback на чтение файла; после записи/удаления слота кэш синхронизируется явно.

## Запись: `scr_saveSave()`

Пишет состояние сессии в `global.current_save_slot`. Возвращает `false` без побочных эффектов, если слот пустой или нет живого `obj_player`.

**Атомарная запись.** Файл пишется в `<slot>.txt.tmp`; старый сейв удаляется только после `file_text_close`, затем `file_rename` поверх (fallback — `file_copy` + `file_delete`). При исключении внутри записи `.tmp` удаляется — битый файл никогда не попадает на место рабочего.

**Формат** — позиционный, строго append-only: новые поля добавляются только перед строкой версии. `#macro SAVE_FORMAT_VERSION 3` пишется последней строкой.

| Строка | Содержимое |
|--------|------------|
| 1–3 | `x`, `y`, `facing_direction` игрока |
| 4 | имя комнаты |
| 5 | `global.__save_playtime_seconds` |
| 6 | JSON инвентаря (`inventory_serialize(global.inventory)`) |
| 7–8 | индексы экипировки в инвентаре (`-1` = пусто), сравнение по `name`+`itemType` |
| 9 | JSON `global.flag` |
| 10 | `global.plot` |
| 11 | JSON `global.entity_state` |
| 12 | JSON статов: `hp`, `maxhp`, `atk`, `def`, `base_atk`, `base_def`, `lv`, `gold`, `name` (`player_name`) `[v3]` |
| 13 | строка `ChatterboxVariablesExport()` `[v3]` |
| 14 | `SAVE_FORMAT_VERSION` |

Подробный разбор построчного формата — в [Форматы данных](../architecture/data-formats.md).

## Загрузка: `scr_saveLoad(_change_room = true)`

Читает файл целиком в локальные переменные, валидирует и только потом применяет глобалы — битый сейв не оставляет сессию в полузагруженном состоянии.

**Детект версии** по строке после `entity_state`: начинается с `{` → stats_json формата v3 (затем строка Chatterbox и номер версии); число → v2; EOF → v1. Сейв с `_save_version > SAVE_FORMAT_VERSION` отклоняется с ошибкой в логе — раскладка полей новее текущей неизвестна.

**Миграция v1/v2.** Секции статов в старых сейвах нет — применяются стартовые дефолты: `stat_hp = 99`, `stat_maxhp = 99`, `stat_base_atk = 0`, `stat_base_def = 0`, `stat_lv = 20`, `stat_gold = 99`, `player_name = "CHARA"`. Для сейвов v3 без `base_atk`/`base_def` база выводится вычитанием бонуса экипировки из сохранённых `atk`/`def`. Эффективные `stat_atk`/`stat_def` всегда пересчитываются `scr_stats_recalc()` — сохранённым значениям не доверяют.

**Chatterbox.** При непустой JSON-строке — `ChatterboxVariablesImport`; при отсутствии данных (v1/v2 или пустая строка) — `ChatterboxVariablesResetAll()` + `ChatterboxVariablesClearVisitedAll()`, чтобы переменные и visited-метки прошлой сессии не утекли в загруженную.

**Применение.** Заполняются `__save_playtime_seconds`, `inventory` (или `scr_inventory_init()` при битой секции), `equipped_weapon`/`equipped_armor` по индексам, `flag`, `plot`, `entity_state`, `stat_*`, `player_name`; координаты уходят в `global.__next_spawn_*`.

**Режим `_change_room = true`** (дефолт) дополнительно сбрасывает runtime-состояние и меняет комнату:

1. Активная катсцена завершается штатно через `finish_cutscene()` менеджера (флаги-сироты снимаются вручную, если менеджер уже мёртв); брошенный сборщик `__cutscene_build_mgr` уничтожается.
2. `global.__interacted_targets` и `global.room_flags` очищаются — это сессионное состояние.
3. `obj_player` и `obj_changingRoomsController` уничтожаются, выполняется `room_goto(_room)`.
4. Выставляется `global.__dev_spawn` с координатами сейва — игрока создаёт `obj_globalManager` в новой комнате.

**Режим `_change_room = false`** применяет только глобалы (инвентарь, флаги, статы, spawn-override) без сброса runtime-состояния, уничтожения инстансов и `room_goto` — используется внутренними стресс-тестами.

**Вспомогательные функции** (все в `scr_saveLoad.gml`): `scr_save_slot_names()` — список слотов; `scr_save_metadata_defaults(slot, path)` — дефолтная метаструктура пустого/битого слота; `scr_save_read_metadata(slot_path)` — позиционный парсер «шапки» (`x`, `y`, `facing`, `room`, `playtime`) для кэша и меню.

## Быстрый сейв: `scr_global_quick_save()`

Вызывается по `F7` из `scr_global_debug_hotkeys` — только при включённом `global.debug`. Отказывается, если открыт UI или идёт катсцена (`scr_checkUIBlocking`) и в служебных/menu-комнатах (`global.is_menu_room`). При пустом `current_save_slot` молча берёт первый слот списка. После успешного `scr_saveSave()` обновляет `last_played_save_slot`, `game_state` (включая `total_playtime_seconds`) и запись слота в `__save_slot_metadata_cache`, затем показывает уведомление `"Saved"`.

## Playtime

- **`global.__save_playtime_seconds`** — время текущего сейва, пишется строкой 5 файла слота.
- **`global.__total_playtime_seconds`** — суммарное время через все сессии, персистится в `game_state.dat`.
- Накопление — `obj_globalManager/Step_0`: `delta_time / 1000000` прибавляется к обоим счётчикам, только вне menu-комнат.
- `obj_globalManager/Other_3` (Game End) копирует `__total_playtime_seconds` в `global.game_state.total_playtime_seconds` и пишет `scr_game_state_save` — но пропускает запись при `global.clean_state == true`, чтобы не воскрешать `game_state.dat` после `scr_resetGameToDefault`.
- Форматирование — `scr_format_playtime(seconds)` → строка `H:MM:SS`; используется в меню слотов и в настройках.

## `game_state.dat`

Построчный `key=value` файл (`scr_game_state_load`/`scr_game_state_save`): хранит `last_played_save_slot` и `total_playtime_seconds`. Запись атомарная через `.tmp`, как у сейвов; при чтении значения нормализуются (`true`/`false`, числа). Подробнее — [Форматы данных](../architecture/data-formats.md).

## `entity_state` и мировые флаги в сейве

`global.entity_state` — реестр состояний сущностей с ключами `"room_name:entity_id"` (`scr_entity_state_get/set/clear`), сериализуется в сейв целиком (строка 11). Персистентные комнатные флаги живут в том же реестре под зарезервированной сущностью `"_room"` — `scr_world_flag_set`/`scr_world_flag_get`. Сессионные `global.room_flags` в сейв не входят и сбрасываются при загрузке/новой игре. См. [Глобальное состояние](../architecture/global-state.md).

## Что сохраняется / что нет

| Данные | В сейве |
|--------|---------|
| Позиция игрока (`x`, `y`, `facing`), комната | да |
| `__save_playtime_seconds` | да |
| Инвентарь + экипировка | да (JSON + индексы) |
| `global.flag`, `global.plot` | да |
| `global.entity_state`, world-флаги (`_room`) | да (JSON) |
| Статы `stat_*`, `player_name` | да (v3; для v1/v2 — дефолты) |
| Переменные и visited-метки Chatterbox | да (v3; иначе сброс) |
| `last_played_save_slot`, `total_playtime_seconds` | в `game_state.dat` |
| `global.room_flags`, `__interacted_targets`, состояние катсцен | нет — сессионные, сбрасываются |
| Настройки (`player_settings.dat`) | нет — отдельный файл |

## См. также

- [Форматы данных](../architecture/data-formats.md) — построчный формат сейва и `game_state.dat`
- [Глобальное состояние](../architecture/global-state.md) — `entity_state`, `flag`, `plot`, слоты
- [Инициализация](../architecture/initialization.md) — `obj_Init`, прогрев кэша метаданных
- [Инвентарь и статы](inventory-and-stats.md) — `inventory_serialize`, `scr_stats_recalc`, дефолты `stat_*`
- [Ввод](input.md) — действия `confirm`/`back`/`delete`, ребиндинг
- [UI и меню](ui-and-menus.md) — `scr_ui_read_actions`, `scr_ui_nav_vertical`
- [Отладка и тестирование](debug-and-testing.md) — горячие клавиши `F7`, `DEV-LOAD`

<!-- sources: scripts/scr_saveSave/scr_saveSave.gml; scripts/scr_saveLoad/scr_saveLoad.gml; scripts/scr_global_quick_save/scr_global_quick_save.gml; scripts/scr_game_state/scr_game_state.gml; scripts/scr_format_playtime/scr_format_playtime.gml; scripts/scr_defaultLoad/scr_defaultLoad.gml; scripts/scr_resetGameToDefault/scr_resetGameToDefault.gml; scripts/scr_entity_state/scr_entity_state.gml; scripts/scr_global_debug_hotkeys/scr_global_debug_hotkeys.gml:58-62; scripts/scr_ui_read_actions/scr_ui_read_actions.gml; objects/obj_save/Create_0.gml; objects/obj_save/Step_0.gml; objects/obj_save/obj_save.yy; objects/obj_saveManager/Create_0.gml; objects/obj_saveManager/Step_0.gml; objects/obj_saveManager/Draw_64.gml; objects/obj_globalManager/Step_0.gml:63-70; objects/obj_globalManager/Other_3.gml; objects/obj_Init/Create_0.gml:67-90,213-259; rooms/rm_savesSelect/rm_savesSelect.yy -->
