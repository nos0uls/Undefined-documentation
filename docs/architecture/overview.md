---
tags:
  - init
  - runtime
  - persistent-objects
---

# Обзор Архитектуры (Architecture Overview)

Архитектурная схема разделения ответственности между системами инициализации, игрового цикла и контента.

## Диаграмма Архитектуры

```mermaid
graph TD
    subgraph Core [Ядро / Core]
        Init[obj_Init]
        GlobalMgr[obj_globalManager]
        Input[Input System]
        Settings[Settings Manager]
    end

    subgraph Content [Контент / Content]
        Rooms[Комнаты / Rooms]
        Actors[NPC & Игрок]
        Dialogues[Диалоги (Yarn)]
    end

    subgraph Systems [Подсистемы / Subsystems]
        Cutscenes[Cutscene Engine]
        UI[UI Blocking]
        Audio[Audio Manager]
    end

    Init -->|Создает| GlobalMgr
    Init -->|Загружает| Settings
    GlobalMgr -->|Управляет| Audio
    GlobalMgr -->|Мониторит| UI

    Rooms -->|Содержит| Actors
    Actors -->|Используют| Input
    Actors -->|Запускают| Dialogues
    Dialogues -->|Могут вызывать| Cutscenes
```

## Основные Принципы

1.  **Централизованная Инициализация**: Все глобальные переменные объявляются в одном месте (`obj_Init`).
2.  **Менеджеры-Одиночки**: Системы (катсцены, сохранения, настройки) управляются через объекты-менеджеры, существующие в единственном экземпляре.
3.  **Data-Driven Диалоги**: Весь текст и ветвления диалогов вынесены в файлы `.yarn` и не зашиты в код.
4. **UI Blocking**: Блокировка ввода через `scr_checkUIBlocking(exclude_self = false, include_cutscene = true)` — проверяет существование ключевых UI-объектов (`textboxTest_scribble`, `obj_settingsManager`, `obj_menu`, `obj_saveManager`, `obj_inGameMenu`, `obj_p3r_title`, `obj_p3r_pause`, `obj_p3r_settings`), а также флаг `global.settings_closing`. Если `include_cutscene` — учитываются `global.active_cutscene_id` и `global.cutscene_camera_override`. `obj_sound_test` проверяется отдельно по флагу `is_open`. Это не полноценный стек, а hardcoded список, который гарантирует что игрок не сможет ходить, пока открыто меню или идёт катсцена.

## Структура Папок

*   **`objects/`**: Игровая логика.
*   **`scripts/`**: Библиотеки и глобальные функции.
*   **`rooms/`**: Уровни и меню.
*   **`datafiles/`**: Внешние ресурсы (диалоги, локализация).

## Разделы архитектуры

<div class="grid cards" markdown>

-   :material-play: **Инициализация**
    ---
    Стартовая цепочка `obj_Init` → `obj_globalManager` → `rm_roomMenu`
    [:material-arrow-right: Подробнее](initialization.md)

-   :material-database: **Глобальное состояние**
    ---
    `global.*` переменные, UI blocking, инвентарь, статы
    [:material-arrow-right: Подробнее](global-state.md)

-   :material-cube-outline: **Объекты системы**
    ---
    `obj_Init`, `obj_globalManager`, `obj_music_ctrl`, `obj_menu`
    [:material-arrow-right: Подробнее](objects.md)

-   :material-door-open: **Комнаты**
    ---
    `rm_init`, `rm_roomMenu`, `rm_savesSelect`, room-to-track mapping
    [:material-arrow-right: Подробнее](rooms.md)

</div>

---

## См. также

- [Инициализация](initialization.md) — `obj_Init`, `global.__init_done`
- [Глобальное состояние](global-state.md) — `global.input_map`, UI blocking
- [Комнаты](rooms.md) — `rm_init`, `global.rooms_by_name`
- [Объекты системы](objects.md) — `obj_Init`, `obj_globalManager`, `obj_music_ctrl`
- [Система ввода](../systems/input.md) — `scr_buildInputMap()`, `scr_input_pressed()`
- [Катсцены: обзор](../systems/cutscenes/overview.md) — runtime катсцен
