---
tags:
  - getting-started
  - project-structure
---

# Структура Проекта (Project Structure)

Этот документ описывает основные папки и ключевые объекты проекта **Undefinedtale-888**.

## Основные Папки (Folders)

### 1. Объекты (Objects)
*   **Системные объекты**: Управляющие игрой singleton-объекты.
    *   `obj_Init`: Точка входа. Холодный старт всех глобальных систем.
    *   `obj_globalManager`: Runtime-менеджер: смена комнат, debug, уведомления, катсцены runtime.
    *   `obj_music_ctrl`: Музыкальный контроллер. Time-based fade, intro→loop. Создаётся из `obj_Init`.
    *   `obj_menu`: Главное меню игры.
    *   `obj_settingsManager`: Меню настроек (отдельная комната или overlay).
    *   `obj_saveManager`: Экран выбора сохранения / DEV-LOAD.
    *   `obj_inGameMenu`: Внутриигровое меню (Inventory, Status, Settings).
    *   `obj_devLoader`: UI-экран dev-load для быстрого перехода между комнатами.
    *   `obj_changingRoomsController`: Контроллер fade-перехода между комнатами.
*   **Игровые объекты**:
    *   `obj_player`: Объект игрока. Движение, коллизии, взаимодействие.
    *   `obj_actor`: Базовый объект для NPC и персонажей катсцен.
    *   `obj_pointMarker`: Невидимый маркер взаимодействия перед игроком.
    *   `obj_save`: Интерактивный сейвпоинт в мире.
    *   `objRoomChanger`: Триггер смены комнаты.
*   **Родительские объекты** (иерархия):
    *   `par_depth` → `par_actor` → `obj_player` / `obj_actor`
    *   `par_depth` → `par_decor` / `par_interactable` / `par_entity` → `obj_collider`

### 2. Скрипты (Scripts)
Скрипты сгруппированы по функционалу.
*   `scr_constants`: Глобальные константы (`global.DIR`, `global.SETTINGS_STATE`).
*   `scr_player_...`: Логика игрока (движение, анимация, facing, marker).
*   `scr_input...`: API ввода (`scr_input_pressed`, `scr_input_down`, rebind).
*   `scr_settingsManager`: Загрузка/сохранение/применение настроек.
*   `scr_cutscene_...`: Система катсцен (builder API `c_*`, action API `cutscene_*`).
*   `scr_interaction`: Единая точка взаимодействия с NPC и объектами.
*   `scr_saveSave` / `scr_saveLoad`: Сохранение и загрузка игры.
*   `scr_emote_show` / `scr_parse_emote`: Emote-система.
*   `scr_inventory_init`: Инициализация инвентаря и предметов.
*   `scr_room_fade_update`: Fade-переходы между комнатами.
*   `scr_entity_state`: Сохранение и восстановление состояния сущностей.
*   `scr_music_init`: Инициализация музыкальной системы.

### 3. Комнаты (Rooms)
*   `rm_init`: Первая комната при запуске (пустая, только для загрузки).
*   `rm_roomMenu`: Главное меню.
*   `rm_savesSelect`: Экран выбора сохранения.
*   `rm_settings`: Меню настроек (отдельная комната).
*   `rm_devLoad`: DEV-LOAD экран.
*   `rm_*`: Игровые локации. Каждый уровень может содержать `obj_player`, NPC, триггеры перехода (`objRoomChanger`).

## Ключевые Объекты (Key Objects)

### `obj_Init`
Создается один раз в самом начале (Persistent, singleton).
*   Загружает `global.player_settings` и `global.game_state`.
*   Инициализирует константы, аудио-дефолты, input map, кэш сейвов.
*   Вызывает `scr_music_init()` и создаёт `obj_music_ctrl`.
*   Инициализирует инвентарь, статы, диалог face-систему, emote-систему.
*   Создаёт `obj_globalManager` как runtime-менеджер.

### `obj_globalManager`
Существует всегда (Persistent, singleton).
*   **Смена комнат**: `current_room` + `scr_global_on_room_change()`.
*   **Debug**: F1–F12 hotkeys, ghost mode, quick save (F7).
*   **Уведомления**: `notification_active`, `notification_text`.
*   **Катсцены runtime**: tweens, emotes, shakes, spins, jumps, fade.
*   **UI Blocking**: `scr_checkUIBlocking()` — блокирует ввод при открытых меню, диалогах, катсценах.

!!! warning "Музыка — не здесь"
    Музыкальная система управляется отдельным объектом `obj_music_ctrl`, который создаётся из `obj_Init`. `obj_globalManager` НЕ управляет музыкой напрямую.

### `obj_music_ctrl`
Persistent-объект, обновляющий музыку каждый кадр.
*   Time-based fade громкости (`scr_global_music_update_current`).
*   Fade-out предыдущего трека (`scr_global_music_fade_previous`).
*   Intro→loop переход.
*   Debug overlay (F9).

---

## См. также

- [Установка и настройка](setup.md) — клонирование, запуск проекта, стандарты разработки
- [Первый запуск](first-run.md) — что ожидать при запуске, решение проблем
- [Архитектура: объекты](../architecture/objects.md) — `obj_Init`, `obj_globalManager`, `obj_music_ctrl`
- [Архитектура: комнаты](../architecture/rooms.md) — `rm_init`, `global.rooms_by_name`
- [Глобальное состояние](../architecture/global-state.md) — `global.input_map`, UI blocking
