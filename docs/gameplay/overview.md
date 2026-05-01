---
tags:
  - gameplay
---

# Геймплей: Обзор

Этот раздел описывает игровой слой проекта: базовое управление игроком, взаимодействие с миром, поведение меню и общую структуру повседневного gameplay.

## Что входит в gameplay

- перемещение игрока по комнатам
- взаимодействие с NPC и объектами через `confirm`
- работа меню и базового UI
- debug-управление во время разработки

## Связанные разделы

<div class="grid cards" markdown>

-   :fontawesome-solid-keyboard:{ .lg .middle } **Управление**
    ---
    Горячие клавиши, debug-режим (F1–F12)
    ---
    [:octicons-arrow-right-24: Подробнее](controls.md)

-   :fontawesome-solid-gears:{ .lg .middle } **Механики**
    ---
    Перемещение, взаимодействие, диалоги, катсцены
    ---
    [:octicons-arrow-right-24: Подробнее](mechanics.md)

-   :fontawesome-solid-gamepad:{ .lg .middle } **Система ввода**
    ---
    `scr_input_pressed()`, `scr_buildInputMap()`, rebind
    ---
    [:octicons-arrow-right-24: Подробнее](../systems/input.md)

-   :fontawesome-solid-hand-pointer:{ .lg .middle } **Взаимодействие**
    ---
    `scr_interaction()`, `obj_pointMarker`, Yarn-диалоги
    ---
    [:octicons-arrow-right-24: Подробнее](../systems/interaction.md)

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