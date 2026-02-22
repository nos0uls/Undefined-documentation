# Обзор Архитектуры (Architecture Overview)

Undefinedtale-888 построен на базе GameMaker Studio 2 (GML). Архитектура проекта стремится к разделению ответственности между системами инициализации, игрового цикла и контента.

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
        UI[UI Stack]
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
4.  **UI Stack**: Система блокировки ввода через стек открытых окон гарантирует, что игрок не сможет ходить, пока открыто меню.

## Структура Папок

*   **`objects/`**: Игровая логика.
*   **`scripts/`**: Библиотеки и глобальные функции.
*   **`rooms/`**: Уровни и меню.
*   **`datafiles/`**: Внешние ресурсы (диалоги, локализация).
