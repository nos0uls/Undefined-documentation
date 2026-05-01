---
tags:
  - undefscene
  - editor
---

# Undefscene: Визуальный редактор катсцен

Undefscene — программа для создания катсцен без программирования. Вы собираете катсцену из блоков (нод), соединяете их линиями, настраиваете параметры — и готово.

Катсцена — это управляемая сцена в игре, где персонажи двигаются, разговаривают, камера перемещается, а игрок не может свободно ходить. Примеры: вступление перед боем, разговор NPC, заставка после победы.
Редактор позволяет собирать катсцены как граф из нод и связей, не редактируя вручную JSON-файлы для каждого изменения.

## Установка
-Зайдите на [GITHUB проекта](https://github.com/nos0uls/Undefscene/releases/latest) и скачайте нужную версию, где portable - не требует установки.
-После загрузки запустите редактор, опционально укажите путь к проекту Gamemaker.

## Что умеет редактор

- Собирать катсцену из нод и связей на визуальном холсте
- Настраивать параметры каждой ноды через Inspector
- Показывать превью пути и диалогов прямо в редакторе
- Проверять катсцену на ошибки перед экспортом
- Экспортировать готовый файл для игры

## Как начать

1. Скачайте или соберите редактор (см. ниже)
2. Откройте проект GameMaker (файл `.yyp`) — это включит автокомплит и проверки
3. Создайте новую сцену: **New Scene**
4. Добавляйте ноды из палитры слева, соединяйте их, настраивайте в Inspector справа
5. Экспортируйте: **Export for Engine** → сохраните в `datafiles/cutscenes/`

## Установка и запуск

=== "Из исходников"

    1. Откройте папку `editor-app`
    2. Установите зависимости: `npm install`
    3. Запустите: `npm run dev`

=== "Готовый билд"

    1. Соберите: `npm run build:win` (в папке `editor-app`)
    2. Запустите файл из папки `dist`

## Навигация по документации

<div class="grid cards" markdown>

-   :fontawesome-solid-cubes:{ .lg .middle } **Справочник нод**

    ---

    Все 30 нод с параметрами и примерами

    [:material-arrow-right: nodes.md](nodes.md)

-   :fontawesome-solid-lightbulb:{ .lg .middle } **How-to карточки**

    ---

    Короткие рецепты: «как добавить диалог», «как настроить камеру»

    [:material-arrow-right: how-to.md](how-to.md)

-   :fontawesome-solid-desktop:{ .lg .middle } **Интерфейс**

    ---

    Где что находится, как управлять холстом, Preferences

    [:material-arrow-right: ui.md](ui.md)

-   :fontawesome-solid-list-check:{ .lg .middle } **Workflow**

    ---

    Пошаговый процесс создания катсцены

    [:material-arrow-right: workflow.md](workflow.md)

-   :fontawesome-solid-file-export:{ .lg .middle } **Сохранение и экспорт**

    ---

    Разница между Save и Export, форматы файлов

    [:material-arrow-right: formats.md](formats.md)

-   :fontawesome-solid-triangle-exclamation:{ .lg .middle } **Проверки и ошибки**

    ---

    Что означают warnings, частые ошибки

    [:material-arrow-right: validation.md](validation.md)

-   :fontawesome-solid-circle-question:{ .lg .middle } **FAQ**

    ---

    Частые вопросы и проблемы

    [:material-arrow-right: faq.md](faq.md)

-   :fontawesome-solid-book:{ .lg .middle } **Глоссарий**

    ---

    Термины и определения

    [:material-arrow-right: glossary.md](glossary.md)

</div>

---

## См. также

- [Катсцены: обзор](../overview.md) — как катсцены работают в игре
- [Архитектура катсцен](../architecture.md) — для разработчиков
