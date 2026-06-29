---
tags:
  - gameplay
  - mechanics
---

# Игровые Механики (Mechanics)

Основные игровые механики проекта.

## Текущие механики верхнего уровня

- **Перемещение игрока**: перемещение, бег и дебаг-команды описаны в [управлении](./controls.md).
- **Взаимодействие с миром**: запуск через `confirm`, проверка вектора взгляда и `obj_pointMarker` описаны в [системе взаимодействия](../systems/interaction.md).
- **Диалоги и Yarn**: интеграция Yarn и рантайм-логика описаны в системных разделах и гайдах по катсценам.
- **Катсцены**: временный перехват управления вводом, камерой и потоком диалогов.

## Документировано частично

В проекте есть связанные gameplay-аспекты, которые пока лучше раскрыты через системные документы, а не через отдельную gameplay-страницу:

- UI blocking (`scr_checkUIBlocking`, `scr_player_ui_blocking`) — блокировка ввода при открытых меню, диалогах и катсценах
- музыка и переходы между состояниями
- катсценная интеграция игрока
- защита при смене комнаты (`scr_global_transition_safety`) — выталкивание из коллайдеров и отключение ghost_mode после перехода
- [Инвентарь](../systems/inventory.md) — 8 слотов, оружие и броня
- [Emote-система](../systems/emote.md) — эмоции над персонажами и объектами
- [Система сохранений](../systems/save-system.md) — 3 слота, DEV-LOAD, quick save
- [Debug-инструменты](../systems/debug-tools.md) — оверлеи, ghost mode, быстрые переходы
- [Переходы между комнатами](../systems/room-transitions.md) — fade, триггеры, безопасность
- [NPC и диалоги](../systems/npc-dialogue.md) — взаимодействие, Yarn, условия диалогов

## Куда смотреть дальше

- [Управление](./controls.md)
- [Система ввода](../systems/input.md)
- [Система взаимодействия](../systems/interaction.md)
- [Катсцены: Обзор](../systems/cutscenes/overview.md)

---

## См. также

- [Управление](controls.md) — горячие клавиши, debug-режим
- [Геймплей: обзор](overview.md) — игровой слой, связанные разделы
- [Система ввода](../systems/input.md) — `scr_input_pressed()`, `scr_buildInputMap()`
- [Система взаимодействия](../systems/interaction.md) — `scr_interaction()`, `obj_pointMarker`
- [Система катсцен](../systems/cutscenes/overview.md) — `obj_cutsceneManager`, camera override