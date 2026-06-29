---
tags:
  - undefscene
  - editor
---

# Undefscene: Визуальный редактор катсцен

Инструмент для создания игровых сцен через граф нод. Позволяет настраивать движение персонажей, диалоги и камеру без прямого редактирования JSON-кода.

## Ключевые возможности
- Визуальное редактирование графа на базе React Flow.
- Инспектор параметров для настройки каждой ноды.
- Автоматическая проверка на ошибки перед экспортом.
- Прямой экспорт в формат движка (`datafiles/cutscenes/`).
- **Room Visual Editor** — расстановка актёров и рисование путей поверх скриншота комнаты.
- **Template Library** — сохранение и вставка часто используемых фрагментов графа.
- **Bookmarks** и **Notes** — навигация и заметки режиссёра прямо на сцене.

## Быстрый старт
1. Скачайте последнюю версию с [GitHub Releases](https://github.com/nos0uls/Undefscene/releases/latest).
2. Подключите проект GameMaker (`.yyp`) в настройках для активации автозаполнения ассетов.
3. Создайте новую сцену (**New Scene**).
4. Добавьте ноды, соедините их и настройте параметры.
5. Экспортируйте результат: **Export for Engine** → сохраните в `datafiles/cutscenes/`.

## Сборка и запуск
=== "Из исходников"
    1. Перейдите в папку `editor-app`.
    2. Установите зависимости: `pnpm install`.
    3. Запустите dev-сервер: `pnpm dev`.

=== "Готовый билд"
Просто скачайте и запустите нужный .exe файл. В зависимости от выбранной версии будет открыт установщик.
## Разделы документации

<div class="grid cards" markdown>

-   :material-cube-outline: **Справочник нод**

    ---

    Все 83 нод с параметрами и примерами

    [:material-arrow-right: nodes.md](nodes.md)

-   :material-lightbulb: **How-to карточки**

    ---

    Короткие рецепты: «как добавить диалог», «как настроить камеру»

    [:material-arrow-right: how-to.md](how-to.md)

-   :material-monitor-dashboard: **Интерфейс**

    ---

    Где что находится, как управлять холстом, Preferences

    [:material-arrow-right: ui.md](ui.md)

-   :material-playlist-check: **Workflow**

    ---

    Пошаговый процесс создания катсцены

    [:material-arrow-right: workflow.md](workflow.md)

-   :material-file-export: **Сохранение и экспорт**

    ---

    Разница между Save и Export, форматы файлов

    [:material-arrow-right: formats.md](formats.md)

-   :material-alert-decagram: **Проверки и ошибки**

    ---

    Что означают warnings, частые ошибки

    [:material-arrow-right: validation.md](validation.md)

-   :material-help-circle: **FAQ**

    ---

    Частые вопросы и проблемы

    [:material-arrow-right: faq.md](faq.md)

-   :material-book: **Глоссарий**

    ---

    Термины и определения

    [:material-arrow-right: glossary.md](glossary.md)

</div>

---

## См. также

- [Катсцены: обзор](../overview.md) — как катсцены работают в игре
- [Архитектура катсцен](../architecture.md) — для разработчиков
