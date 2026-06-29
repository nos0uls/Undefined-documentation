---
tags:
  - code-reference
  - events
---

# События Объектов (Object Events)

Описание основных GameMaker-событий, используемых в архитектуре проекта.

## Основные события

- **Create**: инициализация инстанса.
- **Step**: игровая логика, обновление состояния, ввод, переходы.
- **Alarm**: отложенные действия (например, ожидание завершения диалога в `obj_save`).
- **Collision**: проверка столкновения (например, `objRoomChanger` с игроком).
- **Key Press / Key Release**: обработка однократных нажатий (debug hotkeys).
- **Draw / Draw GUI**: рендеринг игрового мира и интерфейса.
- **Draw_64**: оверлей в GUI-координатах (debug info, коллайдеры, хитбокс, уведомления).
- **Room Start**: логика при входе в комнату (DEV-LOAD спавн, `scr_global_on_room_change`).
- **Room End**: очистка при выходе из комнаты.
- **Clean Up / Destroy**: освобождение памяти и ссылок.
- **Room Creation Code**: инициализация на уровне комнаты.
- **Global Room Creation Code**: fallback холодный старт, если `obj_Init` не создался.

## Использование в проекте

- `obj_Init/Create`: первичный холодный старт систем.
- `obj_globalManager/Step`: поддержка рантайм-состояния.
- `obj_globalManager/Draw_64`: debug-оверлеи, уведомления, эмоции, runtime катсцен.
- `obj_player/Step`: движение и взаимодействие.
- `obj_player/Create`: создание `obj_pointMarker` и применение spawn-оверрайдов.
- `obj_cutsceneManager/Step`: выполнение очереди экшенов катсцены.
- `obj_saveManager/Step`: UI-навигация по save-слотам.
- `obj_changingRoomsController/Step`: обновление fade-перехода.
- `objRoomChanger/Collision`: запуск перехода в другую комнату.
- `Room Start`: вызов `scr_global_on_room_change` и `scr_global_handle_dev_spawn`.

## Связанные документы

- [Обзор архитектуры](../architecture/overview.md)
- [Инициализация](../architecture/initialization.md)
- [Глобальное состояние](../architecture/global-state.md)
- [Катсцены: Отладка](../systems/cutscenes/debugging.md)

---

## См. также

- [GML Скрипты](gml-scripts.md) — `scr_*` функции, `global.*` helpers
- [Глобальные функции](functions.md) — точка входа в справочник по функциям
- [Архитектура: объекты](../architecture/objects.md) — `obj_Init`, `obj_globalManager`, `obj_player`
- [Архитектура: инициализация](../architecture/initialization.md) — `obj_Init/Create`, `GlobalRoomCreationCode`
- [Катсцены: архитектура](../systems/cutscenes/architecture.md) — `obj_cutsceneManager/Step`, `action_queue`