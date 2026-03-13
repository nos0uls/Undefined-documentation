# События Объектов (Object Events)

Эта страница кратко описывает основные GameMaker events, которые чаще всего встречаются в архитектуре проекта.

## Основные events

- **Create** — первичная инициализация инстанса.
- **Step** — игровая логика, обновление состояния, ввод, проверки переходов.
- **Draw / Draw GUI** — обычная и GUI-отрисовка.
- **Clean Up / Destroy** — освобождение ссылок, завершение временного состояния.
- **Room Creation Code / GlobalRoomCreationCode** — страховка и room-level setup для запуска систем.

## Как это используется в проекте

- `obj_Init/Create` отвечает за стартовую инициализацию.
- `obj_globalManager/Step` поддерживает runtime-состояние между комнатами.
- `obj_player/Step` и связанные скрипты управляют движением, facing и interaction flow.
- `obj_cutsceneManager/Step` двигает катсценный runtime и синхронизирует экшены.
- `Draw GUI` применяется для глобальных уведомлений и части UI.

## Связанные документы

- [Обзор архитектуры](../architecture/overview.md)
- [Инициализация](../architecture/initialization.md)
- [Глобальное состояние](../architecture/global-state.md)
- [Катсцены: Отладка](../systems/cutscenes/debugging.md)