---
title: "Undefscene: Tutorial — быстрый старт"
tags:
  - undefscene
  - editor
---

# Tutorial: быстрый старт

Пошаговый тур по первой катсцене в Undefscene: от пустой сцены до экспорта в игру — `Start` → `Dialogue` → `End`, добавление актёра и визуальная расстановка позиций.

## Шаг 1: подготовка проекта

1. Запустите Undefscene.
2. При первом запуске на экране приветствия выберите язык, тему и акцентный цвет.
3. Откройте проект GameMaker: **File → Open Project (.yyp)**.
4. Создайте новую сцену: **File → New Scene**. На холсте появится нода `Start`.

!!! tip "Приветствие можно пропустить"
    Нажмите **Esc** на экране приветствия, чтобы сразу открыть редактор.

## Шаг 2: первая цепочка

1. Кликните средней кнопкой мыши по пустому месту холста — появится нода `Dialogue`. Тот же результат даёт перетаскивание `Dialogue` из палитры слева.
2. Соедините выход `Start` со входом `Dialogue`.
3. Выберите `Dialogue` — в Inspector укажите `File` (`datafiles/Dialogues/testDialogue.yarn`) и `Node` (`Cutscene-Bridge-Demo`).
4. Добавьте ноду `End` и соедините её с `Dialogue`.

## Шаг 3: добавление актёра

1. Добавьте ноду `Actor Create` между `Start` и `Dialogue`.
2. В Inspector задайте уникальный `Actor Name`, например `asher`.
3. Выберите `Actor Sprite` (Sprite / Object) из списка ассетов проекта.
4. Откройте **Room Visual Editor** и разместите актёра на сцене.
5. Нажмите **Импорт актёров** — координаты заполнят поля `x` и `y`.

## Шаг 4: движение

1. Добавьте ноду `Follow Path` после `Dialogue`.
2. В RVE нарисуйте путь инструментом **Карандаш**.
3. Нажмите **Импорт пути** — точки попадут в ноду.
4. В `Follow Path` укажите `Target` = `asher` и `Speed (px/sec)`.

## Шаг 5: экспорт

1. Нажмите **File → Export to Game** («Экспорт в игру»).
2. Выберите папку `datafiles/cutscenes/` в проекте GameMaker.
3. Если в логах нет ошибок, файл готов к использованию в игре.

## Что дальше

- Добавьте камеру через `Camera Pan` или `Camera Track`.
- Используйте `Parallel` / `Parallel Join` для одновременных действий.
- Сохраняйте часто используемые фрагменты в панель **Templates** (Шаблоны).

## См. также

- [Room Visual Editor](room-visual-editor.md) — подробнее про визуальное редактирование
- [How-to: типовые задачи](how-to.md) — рецепты для распространённых сцен
- [Справочник нод](nodes.md) — все ноды и параметры

<!-- sources: editor-app/src/renderer/src/editor/useNodeOperations.ts:336-342; editor-app/src/renderer/src/editor/runtimeTypes.ts:137; editor-app/src/renderer/src/editor/nodes/nodeRegistry.ts -->
