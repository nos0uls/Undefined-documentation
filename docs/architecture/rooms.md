---
tags:
  - runtime
---

# Комнаты (Rooms)

Список основных комнат проекта и их назначение.

???+ note "Список основных комнат"
    | Комната | Назначение |
    |---------|------------|
    | `rm_init` | **Точка входа**. Пустая комната, где создаётся `obj_Init`. Сразу переключает на `rm_roomMenu` через `room_goto()`. |
    | `rm_roomMenu` | **Главное меню**. Содержит `obj_menu`. Запускает музыку меню (`global.play_music(music_menu)`). |
    | `rm_savesSelect` | Экран выбора сохранения. Содержит `obj_saveManager`. Использует кэш метаданных `global.__save_slot_metadata_cache` для быстрого отображения слотов без дискового I/O. |
    | `rm_settings` | **Меню настроек** (отдельная комната). Содержит `obj_settingsManager`. Не overlay — полноценная комната. |
    | `rm_devLoad` | **DEV-LOAD**. Техническая комната для быстрого перехода на уровни при разработке. Доступна из меню выбора сейвов при `global.debug == true` и `player_settings.devload_focus == true`. |
    | `rm_*` | Игровые уровни (школа, город и т.д.). Каждый уровень может содержать `obj_player`, NPC, триггеры перехода (`obj_roomchanger`). |

## См. также

- [Объекты системы](objects.md) — `obj_Init`, `obj_menu`, `obj_saveManager`
- [Инициализация](initialization.md) — `global.rooms_by_name`
- [Геймплей: обзор](../gameplay/overview.md) — игровые уровни и переходы

## Организация

Комнаты загружаются по имени через глобальную карту `global.rooms_by_name` (`ds_map`), которая строится в `obj_Init.Create` циклом от `room_first` до `room_last`. Это избавляет от жёстких ссылок на asset index при загрузке сохранений и DEV-LOAD переходах.

```gml
global.rooms_by_name = ds_map_create();
var _r = room_first;
while (true) {
    var _r_name = room_get_name(_r);
    ds_map_set(global.rooms_by_name, _r_name, _r);
    if (_r == room_last) break;
    _r = room_next(_r);
}
```
