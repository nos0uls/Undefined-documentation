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
- **Draw / Draw GUI**: рендеринг игрового мира и интерфейса.
- **Clean Up / Destroy**: освобождение памяти и ссылок.
- **Room Creation Code**: инициализация на уровне комнаты.

## Использование в проекте

- `obj_Init/Create`: первичный холодный старт систем.
- `obj_globalManager/Step`: поддержка рантайм-состояния.
- `obj_player/Step`: движение и взаимодействие.
- `obj_cutsceneManager/Step`: выполнение очереди экшенов катсцены.
- `Draw GUI`: отрисовка уведомлений и системных оверлеев.

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