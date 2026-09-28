---
tags:
  - save
  - runtime
  - persistent-objects
---

# Система сохранений (Save System)

Текстовые save-файлы по слотам, хранящие позицию игрока, комнату, инвентарь, флаги сюжета и состояние сущностей. UI-менеджер управляется `obj_saveManager`.

## Обзор

Сохранения используют три слота: `save1`, `save2`, `save3`. Файлы пишутся в `working_directory` с расширением `.txt`. Формат смешанный: первые строки содержат plain-значения (координаты, комната, playtime), а инвентарь, флаги и `entity_state` хранятся как JSON-строки. Это позволяет `scr_saveLoad` загружать как новые, так и более ранние сейвы без поломки.

Глобальный `game_state` (`game_state.dat`) хранит мета-информацию: `last_played_save_slot` и `total_playtime_seconds`. Он загружается при старте и обновляется при сохранении/загрузке.

## Архитектура / API

### Основные скрипты

| Скрипт | Описание |
|--------|----------|
| `scr_saveSave` | Записывает текущий слот `global.current_save_slot`. Сохраняет позицию, комнату, playtime, инвентарь, индексы экипировки, `global.flag`, `global.plot`, `global.entity_state`. |
| `scr_saveLoad` | Читает текущий слот, проверяет версию схемы (сейвы новее `SAVE_FORMAT_VERSION` отклоняются), парсит JSON-блоки, восстанавливает инвентарь и экипировку, сбрасывает runtime-состояние сессии (катсцена через `finish_cutscene`, очередь взаимодействий, `room_flags`, диалоговые флаги), переходит в комнату и создаёт игрока через dev-spawn. |
| `scr_defaultLoad` | Загружает дефолтную стартовую позицию (`rm_uphill_school`, 377, 187, facing down). |
| `scr_resetGameToDefault` | Удаляет все сейвы, настройки и `game_state.dat`, сбрасывает настройки и закрывает игру. |
| `scr_global_quick_save` | Быстрое сохранение в текущий слот по клавише F7. |

### Объекты

| Объект | Описание |
|--------|----------|
| `obj_saveManager` | UI-менеджер экрана выбора/сохранения слотов. Режимы задаются enum `SAVEMENU_MODE` (`LOAD`/`SAVE`, объявлен в `scr_saveLoad`), удаление слота, dev-load в debug-режиме. |
| `obj_save` | Интерактивный объект-сейвпоинт в мире. При взаимодействии запускает Yarn-диалог, заданный в `dialogue_filename` и `dialogue_node`. |

### Формат save-файла

| Строка | Значение | Пример |
|--------|----------|--------|
| 1 | `x` | `377` |
| 2 | `y` | `187` |
| 3 | `facing_direction` | `2` |
| 4 | `room_name` | `rm_uphill_school` |
| 5 | `playtime` | `123.45` |
| 6 | JSON инвентаря | `[{ __type: "weapon", ... }]` |
| 7 | Индекс экипированного оружия | `0` |
| 8 | Индекс экипированной брони | `2` |
| 9 | JSON флагов | `{ "met_asher": true }` |
| 10 | `plot` | `1` |
| 11 | JSON `entity_state` | `{ "rm_uphill_school:door_1": { ... } }` |
| 12 | JSON статов игрока (`global.stat_*`) | `{ "hp": 20, "maxhp": 20, "atk": 10, "def": 10, "lv": 1, "gold": 0, "name": "HUMAN" }` |
| 13 | JSON состояния Chatterbox | `ChatterboxVariablesExport()` строка |
| 14 | версия схемы | `3` |

Строка версии — всегда последняя в файле (`#macro SAVE_FORMAT_VERSION` в `scr_saveSave`). Формат строго append-only: новые поля добавляются только перед строкой версии, вставку в середину позиционные читатели (`obj_Init`, `load_save_metadata`) не переживают. Сейвы без строки версии трактуются как легаси v1; сейвы v2 (12 строк) корректно мигрируют на v3 с дефолтными статами; сейв с версией выше поддерживаемой отклоняется с ошибкой в логе.

### Ограничения `entity_state`

`global.entity_state` — инфраструктура без контентных писателей: `scr_entity_state_set` и `__entity_state_save` (`par_interactable`) существуют, но ни одна комната не задаёт `entity_id`, и метод сохранения никто не вызывает. У инстансов без `entity_id` используется fallback `"entity_" + string(id)` — он нестабилен между заходами в комнату (instance id переиспользуются), поэтому на практике реестр в реальной игре остаётся пустым, а строка 11 в сейве сериализует `{}`.

### Персист `game_state.dat` при выходе

При завершении игры `obj_globalManager.Other_3` (Game End) копирует `global.__total_playtime_seconds` в `global.game_state.total_playtime_seconds` и пишет файл через `scr_game_state_save`. Guard `global.clean_state == true` пропускает запись: `scr_resetGameToDefault` уже удалил `game_state.dat`, и без этой проверки Game End воскрешал бы файл сразу после wipe.

## Примеры

### Сохранение вручную

```gml title="scr_saveSave"
global.current_save_slot = "save2";
var _ok = scr_saveSave();
if (_ok) {
    global.show_notification("Saved");
}
```

### Загрузка последнего слота

```gml title="scr_saveLoad"
global.current_save_slot = global.last_played_save_slot;
scr_saveLoad();
```

### Быстрое сохранение

```gml title="scr_global_quick_save"
scr_global_quick_save(); // F7
```

### Сброс игры

```gml title="scr_resetGameToDefault"
scr_resetGameToDefault(); // Удаляет все сейвы и закрывает игру
```

## Troubleshooting

!!! warning "Слот не найден"
    `scr_saveLoad` возвращает `false`, если `global.current_save_slot == ""` или файл отсутствует. Убедитесь, что слот задан до вызова.

!!! warning "Игрок не создаётся после загрузки"
    `scr_saveLoad` уничтожает существующего `obj_player` и переходит в целевую комнату. Спавн выполняется через `global.__dev_spawn` и `global.__next_spawn_*`. Если в целевой комнате нет логики обработки `__dev_spawn`, игрок не появится.

!!! note "Инвентарь и флаги отсутствуют в сейве"
    `scr_saveLoad` пропускает JSON-блоки, если они не найдены или не парсятся. Игра продолжится с текущим инвентарём и флагами.

## См. также

- [Инвентарь](inventory.md) — сериализация предметов
- [Глобальное состояние](../architecture/global-state.md) — `game_state`, `flag`, `plot`, `entity_state`
- [GML-скрипты](../code-reference/gml-scripts.md) — полный список скриптов
- [Архитектура: объекты](../architecture/objects.md) — `obj_saveManager`, `obj_save`, `obj_Init`
