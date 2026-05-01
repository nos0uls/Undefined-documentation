---
tags:
  - undefscene
  - editor
  - electron
  - react-flow
---

# Undefscene: Обзор

Undefscene — это desktop app на Electron и React Flow для визуального создания, редактирования и тестирования катсцен проекта Undefinedtale-888.

Редактор позволяет собирать катсцены как граф из нод и связей, не редактируя вручную JSON-файлы для каждого изменения.

## Где находится редактор

Редактор находится в репозитории `Undefscene`, в папке `editor-app`.

## Запуск в режиме разработки

1. Перейдите в папку `editor-app`.
2. Установите зависимости: `npm install`.
3. Запустите приложение: `npm run dev`.

## Сборка

1. Перейдите в папку `editor-app`.
2. Запустите нужный билд-скрипт, например `npm run build:win` для Windows.
3. Готовый бинарный файл появится в папке `dist`.

## Что умеет редактор

- Визуально собирать граф катсцены из нод и рёбер.
- Редактировать параметры выбранной ноды через Inspector.
- Показывать editor-side preview для `follow_path` прямо в Inspector.
- Загружать `.yyp` проект GameMaker для автокомплита и валидации.
- Работать с Yarn-диалогами через `Yarn Preview`.
- Сохранять рабочую сцену в формате `.usc.json`.
- Экспортировать runtime-формат `.json` для движка.

## Поддерживаемые ноды
Основные типы нод катсцены: Start, Move, Wait, Dialogue, CameraPan, CameraTrack, ActorCreate, ActorDestroy, SetProperty, FollowPath, Parallel, Branch.

Дополнительно поддерживаются:
- `CameraShakeNode` — тряска камеры
- `AutoFacingNode` — включение/выключение авто-поворота актёра
- `AutoWalkNode` — включение/выключение авто-движения актёра

## Состав документации

- [Интерфейс и Preferences](./ui.md)
- [Базовый workflow](./workflow.md)
- [Интеграция с проектом](./integration.md)
- [Room Screenshot Pipeline](./room-screenshot-pipeline.md)
- [Форматы, импорт и экспорт](./formats.md)
- [FAQ и troubleshooting](./faq.md)

---

## См. также

- [Интерфейс и Preferences](ui.md) — панели, Visual Editing, Preferences
- [Базовый workflow](workflow.md) — пошаговый процесс работы
- [Интеграция с проектом](integration.md) — загрузка `.yyp`, cache, screenshot paths
- [Форматы, импорт и экспорт](formats.md) — `.usc.json`, engine `.json`, Export for Engine
- [Room Screenshot Pipeline](room-screenshot-pipeline.md) — mini runner, `obj_roomScreenshotBuilder`
- [Архитектура катсцен](../architecture.md) — `obj_cutsceneManager`, `action_queue`
- [Катсцены: обзор](../overview.md) — JSON-загрузка, Action-классы
