---
title: Документация Undefinedtale-888
hide:
  - navigation
  - toc
---

# Документация Undefinedtale-888

**Undefinedtale-888** — сюжетно-ориентированная RPG с пазлами на GameMaker (GML 2.3+). Документация описывает архитектуру проекта, игровые системы, движок катсцен и визуальный редактор **Undefscene**.

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Начало работы**
    ---
    Установка GameMaker, клонирование репозитория, первый запуск и сборка проекта.
    [:material-arrow-right: Setup](getting-started/setup.md)

-   :material-family-tree:{ .lg .middle } **Архитектура**
    ---
    Инициализация, persistent-объекты, иерархия `par_*`, глобальное состояние, комнаты и форматы данных.
    [:material-arrow-right: Обзор](architecture/overview.md)

-   :material-cog:{ .lg .middle } **Системы**
    ---
    Ввод и геймпад, игрок, переходы комнат, диалоги, взаимодействия, инвентарь, сохранения, музыка, UI.
    [:material-arrow-right: Ввод](systems/input.md)

-   :material-movie-open:{ .lg .middle } **Катсцены**
    ---
    Движок катсцен: JSON-действия, Action-классы, акторы, камера, `partial_control`.
    [:material-arrow-right: Обзор](cutscenes/overview.md)

-   :material-monitor-edit:{ .lg .middle } **Undefscene**
    ---
    Визуальный редактор катсцен: ноды, инспектор, экспорт сценариев в JSON.
    [:material-arrow-right: Обзор](undefscene/overview.md)

-   :material-code-tags:{ .lg .middle } **Справочник**
    ---
    Таблицы всех GML-скриптов, объектов и событий; глоссарий терминов проекта.
    [:material-arrow-right: GML-скрипты](reference/gml-scripts.md)

</div>

## С чего начать

=== "Новичок в проекте"

    1. [Настройка окружения](getting-started/setup.md): IDE, runtime, первый запуск.
    2. [Структура проекта](getting-started/project-structure.md): что где лежит.
    3. [Обзор архитектуры](architecture/overview.md): как связаны подсистемы.

=== "Контент-мейкер катсцен"

    1. [Обзор катсцен](cutscenes/overview.md): способы задать сцену (JSON, GML, `c_*`-функции).
    2. [Undefscene](undefscene/overview.md): визуальный редактор сценариев.
    3. [JSON-действия](cutscenes/json-actions.md): все типы действий и их поля.

=== "Разработчик кода"

    1. [Архитектура](architecture/overview.md) → [инициализация](architecture/initialization.md) → [глобальное состояние](architecture/global-state.md).
    2. [Системы](systems/input.md): ввод, игрок, сохранения, музыка.
    3. [Справочник GML-скриптов](reference/gml-scripts.md): сигнатуры функций.

!!! info "В разработке"
    Документация обновляется параллельно с развитием проекта. Источник истины — код на ветке `audit-fixes-2026-09` (ревизия `7ee444a`).

## См. также

- [Глоссарий](reference/glossary.md) — термины проекта: `persistent`, `entity_state`, `mark_node` и др.
- [Соглашения по коду](getting-started/conventions.md) — именование `obj_`/`par_`/`scr_`, стиль GML.
- [Отладка и тестирование](systems/debug-and-testing.md) — debug-флаг, хоткеи, тест-фреймворк.
- [FAQ Undefscene](undefscene/faq.md) — частые вопросы по редактору.

<!-- sources: audit_2026-09/08_DOCS_REWRITE_SWARM.md (структура разделов nav); docs_new/_meta/CODE_REV.txt (ревизия кода 7ee444a); Undefinedtale888/README.md; Undefinedtale888/Undefinedtale888.yyp -->
