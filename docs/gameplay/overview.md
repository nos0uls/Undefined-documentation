---
tags:
  - gameplay
---

# Геймплей: Обзор

Описание игрового слоя: управление игроком, взаимодействие с миром, структура игрового цикла.

## Что входит в gameplay

- Перемещение игрока по локациям.
- Взаимодействие с NPC и объектами через `confirm`.
- Навигация по меню и интерфейсу.
- Debug-управление.

## Связанные разделы

<div class="grid cards" markdown>

-   :material-keyboard: **Управление**
    ---
    Горячие клавиши, debug-режим (F1–F12).
    [:material-arrow-right: Подробнее](controls.md)

-   :material-cog: **Механики**
    ---
    Перемещение, взаимодействие, диалоги, катсцены.
    [:material-arrow-right: Подробнее](mechanics.md)

-   :material-gamepad: **Система ввода**
    ---
    `scr_input_pressed()`, `scr_buildInputMap()`, переназначение клавиш.
    [:material-arrow-right: Подробнее](../systems/input.md)

-   :material-cursor-default-click: **Взаимодействие**
    ---
    `scr_interaction()`, `obj_pointMarker`, Yarn-диалоги.
    [:material-arrow-right: Подробнее](../systems/interaction.md)

-   :material-movie-open: **Undefscene**
    ---
    Визуальный редактор катсцен: Room Visual Editor, Tutorial, Templates.
    [:material-arrow-right: Подробнее](../systems/cutscenes/undefscene/overview.md)

</div>

## Ключевая идея

Gameplay-логика опирается на единый input API, проверку UI-blocking и объектный подход GameMaker: игрок, маркер взаимодействия, глобальные менеджеры и комнатные объекты работают как отдельные, но согласованные части одной runtime-системы.

---

## См. также

- [Управление](controls.md) — горячие клавиши, debug-режим
- [Механики](mechanics.md) — перемещение, взаимодействие, диалоги, катсцены
- [Система ввода](../systems/input.md) — `scr_input_pressed()`, `scr_buildInputMap()`
- [Система взаимодействия](../systems/interaction.md) — `scr_interaction()`, `obj_pointMarker`
- [Система катсцен](../systems/cutscenes/overview.md) — `obj_cutsceneManager`, camera override